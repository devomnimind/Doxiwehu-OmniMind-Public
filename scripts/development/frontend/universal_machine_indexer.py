#!/usr/bin/env python3
"""
OmniMind Complete System Indexer

Indexa TODA a máquina: arquivos, documentos, configurações, software, etc.
Inclui HD externo e detecta automaticamente tipos de conteúdo.

Funcionalidades:
- Indexação completa de disco (como chkdsk /f no Windows)
- Detecção automática de tipos de arquivo
- Suporte a HD externo
- Estatísticas detalhadas
- Busca semântica universal
"""

import os
import sys
import logging
import hashlib
import mimetypes
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

import psutil
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

# Forçar CPU para evitar problemas de memória
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

logger = logging.getLogger(__name__)


class UniversalContentType(Enum):
    """Tipos de conteúdo universais para indexação completa."""

    CODE = "code"
    DOCUMENTATION = "documentation"
    CONFIG = "config"
    DATA = "data"
    BINARY = "binary"
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    ARCHIVE = "archive"
    SYSTEM = "system"
    UNKNOWN = "unknown"


@dataclass
class UniversalContentChunk:
    """Chunk universal de qualquer tipo de conteúdo."""

    file_path: str
    content: str
    content_type: UniversalContentType
    mime_type: str
    size_bytes: int
    is_text: bool
    encoding: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UniversalEmbeddingsIndexer:
    """
    Indexador universal que pode processar QUALQUER arquivo na máquina.

    Similar ao "chkdsk /f" do Windows, mas para embeddings semânticos.
    """

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "universal_machine_embeddings",
        model_name: str = "all-MiniLM-L6-v2",
        max_file_size_mb: int = 10,  # Máximo 10MB por arquivo
        chunk_size: int = 1000,  # Caracteres por chunk
        max_workers: int = 4,  # Processamento paralelo
    ):
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.model_name = model_name
        self.max_file_size_mb = max_file_size_mb
        self.chunk_size = chunk_size
        self.max_workers = max_workers

        # Inicializar modelo
        logger.info(f"Carregando modelo universal: {model_name}")
        self.model = SentenceTransformer(model_name, device="cpu")
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        # Inicializar Qdrant
        self.client = QdrantClient(qdrant_url)
        self._ensure_collection()

        # Estatísticas
        self.stats = {
            "files_processed": 0,
            "files_indexed": 0,
            "chunks_created": 0,
            "bytes_processed": 0,
            "errors": 0,
            "by_type": {},
            "by_extension": {},
        }

        # Cache de tipos MIME
        mimetypes.init()

        logger.info("🤖 Universal Embeddings Indexer inicializado")
        logger.info(f"📊 Modelo: {model_name} (dim={self.embedding_dim})")
        logger.info(f"🎯 Máximo por arquivo: {max_file_size_mb}MB")
        logger.info(f"⚡ Workers paralelos: {max_workers}")

    def _ensure_collection(self):
        """Cria coleção universal se não existir."""
        try:
            collections = self.client.get_collections().collections or []
            collection_names = [info.name for info in collections]

            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=self.embedding_dim, distance=qmodels.Distance.COSINE
                    ),
                )
                logger.info(f"📁 Coleção universal criada: {self.collection_name}")
        except Exception as exc:
            logger.error(f"❌ Erro ao criar coleção: {exc}")
            raise

    def detect_content_type(self, file_path: str) -> UniversalContentType:
        """Detecta tipo de conteúdo baseado em MIME type e extensão."""
        path = Path(file_path)
        ext = path.suffix.lower()

        # Detectar por MIME type
        mime_type, _ = mimetypes.guess_type(str(path))

        if mime_type:
            if mime_type.startswith("text/"):
                # Arquivos de código
                code_exts = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".php", ".rb", ".sh", ".sql"}
                if ext in code_exts:
                    return UniversalContentType.CODE

                # Documentação
                doc_exts = {".md", ".txt", ".rst", ".adoc", ".pdf"}
                if ext in doc_exts:
                    return UniversalContentType.DOCUMENTATION

                # Configurações
                config_exts = {".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".conf"}
                if ext in config_exts:
                    return UniversalContentType.CONFIG

                return UniversalContentType.TEXT

            elif mime_type.startswith("image/"):
                return UniversalContentType.IMAGE
            elif mime_type.startswith("audio/"):
                return UniversalContentType.AUDIO
            elif mime_type.startswith("video/"):
                return UniversalContentType.VIDEO
            elif mime_type in ["application/zip", "application/x-tar", "application/gzip"]:
                return UniversalContentType.ARCHIVE
            elif mime_type.startswith("application/"):
                return UniversalContentType.BINARY

        # Detectar por extensão (fallback)
        if ext in [".db", ".sqlite", ".csv", ".xlsx", ".xls"]:
            return UniversalContentType.DATA
        elif ext in [".exe", ".dll", ".so", ".dylib"]:
            return UniversalContentType.BINARY
        elif ext in [".log", ".out", ".err"]:
            return UniversalContentType.SYSTEM

        return UniversalContentType.UNKNOWN

    def can_process_file(self, file_path: str) -> bool:
        """Verifica se arquivo pode ser processado."""
        try:
            path = Path(file_path)

            # Verificar tamanho
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > self.max_file_size_mb:
                return False

            # Verificar se é arquivo regular
            if not path.is_file():
                return False

            # Verificar permissões
            if not os.access(path, os.R_OK):
                return False

            return True

        except Exception:
            return False

    def extract_text_content(self, file_path: str) -> Optional[str]:
        """Extrai conteúdo textual de qualquer arquivo."""
        try:
            path = Path(file_path)
            content_type = self.detect_content_type(file_path)

            # Arquivos de texto direto
            if content_type in [UniversalContentType.CODE, UniversalContentType.TEXT,
                              UniversalContentType.CONFIG, UniversalContentType.DOCUMENTATION]:

                # Tentar diferentes encodings
                encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
                for encoding in encodings:
                    try:
                        with open(path, "r", encoding=encoding) as f:
                            content = f.read()
                            # Limitar tamanho para evitar problemas de memória
                            if len(content) > 100000:  # 100KB max
                                content = content[:100000] + "...[TRUNCATED]"
                            return content
                    except UnicodeDecodeError:
                        continue

            # Arquivos PDF (se pdftotext estiver disponível)
            elif path.suffix.lower() == ".pdf":
                try:
                    result = subprocess.run(
                        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
                        capture_output=True, text=True, timeout=30
                    )
                    if result.returncode == 0:
                        return result.stdout
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

            # Arquivos binários - extrair metadados
            else:
                # Para arquivos binários, criar descrição baseada em metadados
                stat = path.stat()
                mime_type, _ = mimetypes.guess_type(str(path))

                metadata = f"""
Arquivo: {path.name}
Tamanho: {stat.st_size} bytes
Tipo MIME: {mime_type or 'desconhecido'}
Modificado: {stat.st_mtime}
Permissões: {oct(stat.st_mode)}
Localização: {path.parent}
"""

                return metadata.strip()

        except Exception as e:
            logger.debug(f"Erro ao extrair conteúdo de {file_path}: {e}")

        return None

    def chunk_content(self, file_path: str) -> List[UniversalContentChunk]:
        """Divide arquivo em chunks processáveis."""
        content = self.extract_text_content(file_path)
        if not content:
            return []

        content_type = self.detect_content_type(file_path)
        path = Path(file_path)
        mime_type, _ = mimetypes.guess_type(str(path))

        # Para arquivos pequenos, um chunk só
        if len(content) <= self.chunk_size:
            return [UniversalContentChunk(
                file_path=file_path,
                content=content,
                content_type=content_type,
                mime_type=mime_type or "unknown",
                size_bytes=path.stat().st_size,
                is_text=True,
                metadata={"chunk_index": 0, "total_chunks": 1}
            )]

        # Dividir em chunks com sobreposição
        chunks = []
        overlap = min(200, self.chunk_size // 4)  # 25% de sobreposição

        i = 0
        chunk_index = 0
        total_chunks = (len(content) + self.chunk_size - overlap - 1) // (self.chunk_size - overlap)

        while i < len(content):
            end = min(i + self.chunk_size, len(content))
            chunk_content = content[i:end]

            chunks.append(UniversalContentChunk(
                file_path=file_path,
                content=chunk_content,
                content_type=content_type,
                mime_type=mime_type or "unknown",
                size_bytes=path.stat().st_size,
                is_text=True,
                metadata={
                    "chunk_index": chunk_index,
                    "total_chunks": total_chunks,
                    "start_pos": i,
                    "end_pos": end
                }
            ))

            i += self.chunk_size - overlap
            chunk_index += 1

        return chunks

    def index_file(self, file_path: str) -> int:
        """Indexa um arquivo individual."""
        self.stats["files_processed"] += 1

        try:
            if not self.can_process_file(file_path):
                return 0

            # Criar chunks
            chunks = self.chunk_content(file_path)
            if not chunks:
                return 0

            # Gerar embeddings e armazenar
            points = []
            for chunk in chunks:
                try:
                    # Gerar embedding
                    embedding = self.model.encode(chunk.content, normalize_embeddings=True)

                    # Criar ID único
                    content_hash = hashlib.sha256(
                        f"{chunk.file_path}:{chunk.content}".encode()
                    ).hexdigest()[:16]
                    point_id = int(content_hash, 16)

                    # Payload com metadados
                    payload = {
                        "file_path": chunk.file_path,
                        "content": chunk.content[:2000],  # Limitar tamanho
                        "content_type": chunk.content_type.value,
                        "mime_type": chunk.mime_type,
                        "size_bytes": chunk.size_bytes,
                        "is_text": chunk.is_text,
                        "chunk_metadata": chunk.metadata or {},
                    }

                    points.append(
                        qmodels.PointStruct(id=point_id, vector=embedding.tolist(), payload=payload)
                    )

                except Exception as e:
                    logger.debug(f"Erro ao processar chunk de {file_path}: {e}")
                    continue

            # Upsert no Qdrant
            if points:
                self.client.upsert(collection_name=self.collection_name, points=points)

                # Atualizar estatísticas
                self.stats["files_indexed"] += 1
                self.stats["chunks_created"] += len(points)
                self.stats["bytes_processed"] += chunks[0].size_bytes

                # Estatísticas por tipo
                ct = chunks[0].content_type.value
                self.stats["by_type"][ct] = self.stats["by_type"].get(ct, 0) + 1

                # Estatísticas por extensão
                ext = Path(file_path).suffix.lower()
                self.stats["by_extension"][ext] = self.stats["by_extension"].get(ext, 0) + 1

                logger.debug(f"✅ Indexado: {file_path} ({len(points)} chunks)")
                return len(points)

        except Exception as e:
            self.stats["errors"] += 1
            logger.debug(f"❌ Erro ao indexar {file_path}: {e}")

        return 0

    def get_mount_points(self) -> List[str]:
        """Detecta todos os pontos de montagem (incluindo HD externo)."""
        mount_points = []

        try:
            # Usar psutil para detectar partições
            partitions = psutil.disk_partitions(all=True)

            for partition in partitions:
                mount_point = partition.mountpoint

                # Filtrar pontos de montagem relevantes
                if (os.path.exists(mount_point) and
                    os.access(mount_point, os.R_OK) and
                    not any(skip in mount_point for skip in ["/proc", "/sys", "/dev", "/run"])):
                    mount_points.append(mount_point)

        except Exception as e:
            logger.warning(f"Erro ao detectar pontos de montagem: {e}")
            # Fallback: pontos comuns
            mount_points = ["/", "/home", "/mnt", "/media"]

        return sorted(set(mount_points))

    def index_entire_machine(self, exclude_patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Indexa TODA a máquina - como "chkdsk /f" mas para embeddings.

        Args:
            exclude_patterns: Padrões de caminho a excluir (regex)
        """
        if exclude_patterns is None:
            exclude_patterns = [
                r"/proc/.*",
                r"/sys/.*",
                r"/dev/.*",
                r"/run/.*",
                r"/tmp/.*",
                r"/var/tmp/.*",
                r".*/\.git/.*",
                r".*/node_modules/.*",
                r".*/__pycache__/.*",
                r".*/\.cache/.*",
                r".*\.pyc$",
                r".*\.pyo$",
            ]

        logger.info("🚀 Iniciando indexação COMPLETA da máquina")
        logger.info("💡 Isso pode levar HORAS dependendo do tamanho dos discos")

        # Detectar pontos de montagem
        mount_points = self.get_mount_points()
        logger.info(f"📍 Pontos de montagem detectados: {mount_points}")

        total_files_found = 0
        total_chunks_created = 0

        # Processar cada ponto de montagem
        for mount_point in mount_points:
            logger.info(f"🔍 Indexando: {mount_point}")
            mount_chunks = self._index_mount_point(mount_point, exclude_patterns)
            total_chunks_created += mount_chunks

        # Estatísticas finais
        final_stats = self.get_stats()
        logger.info("🎉 Indexação completa da máquina finalizada!")
        logger.info(f"📊 Total processado: {final_stats['files_processed']} arquivos")
        logger.info(f"✅ Total indexado: {final_stats['files_indexed']} arquivos")
        logger.info(f"🧩 Total chunks: {final_stats['chunks_created']}")
        logger.info(f"💾 Total bytes: {final_stats['bytes_processed'] / (1024**3):.2f} GB")

        return final_stats

    def _index_mount_point(self, mount_point: str, exclude_patterns: List[str]) -> int:
        """Indexa um ponto de montagem específico."""
        chunks_created = 0

        try:
            # Coletar todos os arquivos
            all_files = []
            for root, dirs, files in os.walk(mount_point):
                # Aplicar exclusões
                for pattern in exclude_patterns:
                    import re
                    if re.search(pattern, root):
                        dirs[:] = []  # Não entrar neste diretório
                        break

                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)

            logger.info(f"📂 Encontrados {len(all_files)} arquivos em {mount_point}")

            # Processar em paralelo
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self.index_file, file_path) for file_path in all_files]

                for future in as_completed(futures):
                    try:
                        chunks = future.result()
                        chunks_created += chunks
                    except Exception as e:
                        logger.debug(f"Erro em future: {e}")

        except Exception as e:
            logger.error(f"Erro ao indexar {mount_point}: {e}")

        return chunks_created

    def search_universal(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Busca semântica universal em todo o conteúdo indexado."""
        # Gerar embedding da query
        query_embedding = self.model.encode(query, normalize_embeddings=True)

        # Buscar no Qdrant
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding.tolist(),
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        # Formatar resultados
        results = []
        for point in search_result.points:
            payload = point.payload or {}
            results.append({
                "score": float(point.score),
                "file_path": payload.get("file_path", ""),
                "content": payload.get("content", ""),
                "content_type": payload.get("content_type", ""),
                "mime_type": payload.get("mime_type", ""),
                "size_bytes": payload.get("size_bytes", 0),
                "is_text": payload.get("is_text", False),
                "chunk_metadata": payload.get("chunk_metadata", {}),
            })

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Estatísticas detalhadas da indexação."""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            base_stats = {
                "collection_name": self.collection_name,
                "vector_dim": self.embedding_dim,
                "total_chunks": collection_info.points_count,
                "model": self.model_name,
            }
        except Exception:
            base_stats = {"error": "Não foi possível obter stats da coleção"}

        # Combinar com stats locais
        base_stats.update(self.stats)
        return base_stats


def main():
    """Função principal para indexação completa."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logger.info("🤖 OMNIMIND - Indexação Universal da Máquina")
    logger.info("=" * 60)

    # Verificar dependências
    try:
        import sentence_transformers
        import qdrant_client
        import psutil
        logger.info("✅ Dependências OK")
    except ImportError as e:
        logger.error(f"❌ Dependência faltando: {e}")
        sys.exit(1)

    # Verificar Qdrant
    try:
        client = QdrantClient("http://localhost:6333")
        collections = client.get_collections()
        logger.info("✅ Qdrant OK")
    except Exception as e:
        logger.error(f"❌ Qdrant inacessível: {e}")
        logger.error("💡 Execute: docker run -p 6333:6333 qdrant/qdrant")
        sys.exit(1)

    # Inicializar indexador universal
    indexer = UniversalEmbeddingsIndexer()

    # Indexar máquina completa
    try:
        logger.info("🚀 Iniciando indexação COMPLETA...")
        logger.info("⚠️  Isso pode levar muito tempo!")

        stats = indexer.index_entire_machine()

        logger.info("\n🎉 Indexação concluída!")
        logger.info("📊 Estatísticas finais:")
        for key, value in stats.items():
            if isinstance(value, dict):
                logger.info(f"   {key}:")
                for subkey, subvalue in value.items():
                    logger.info(f"      {subkey}: {subvalue}")
            else:
                logger.info(f"   {key}: {value}")

    except KeyboardInterrupt:
        logger.info("\n⏹️  Indexação interrompida pelo usuário")
        stats = indexer.get_stats()
        logger.info("📊 Estatísticas parciais salvas")

    except Exception as e:
        logger.error(f"❌ Erro durante indexação: {e}")
        sys.exit(1)

    # Teste de busca
    try:
        logger.info("\n🔍 Testando busca universal...")
        test_queries = [
            "sistema de arquivos Linux",
            "configuração de rede",
            "código Python para machine learning",
            "documentação de API",
        ]

        for query in test_queries:
            logger.info(f"\n🔎 '{query}':")
            results = indexer.search_universal(query, top_k=3)

            for i, result in enumerate(results, 1):
                logger.info(f"   {i}. [{result['content_type']}] {result['file_path']}")
                logger.info(f"      Score: {result['score']:.3f}")
                logger.info(f"      Conteúdo: {result['content'][:100]}...")

    except Exception as e:
        logger.error(f"❌ Erro no teste de busca: {e}")

    logger.info("\n🎯 Sistema pronto para buscas semânticas universais!")
    logger.info("\n💡 Uso:")
    logger.info("   from universal_indexer import UniversalEmbeddingsIndexer")
    logger.info("   indexer = UniversalEmbeddingsIndexer()")
    logger.info("   results = indexer.search_universal('sua consulta')")


if __name__ == "__main__":
    main()