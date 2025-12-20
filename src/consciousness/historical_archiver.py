import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import asdict

logger = logging.getLogger(__name__)


class HistoricalArchiver:
    """
    Gerencia o arquivamento de histórico do OmniMind (Cold Storage).

    Responsável por mover ciclos antigos da RAM (Hot Memory) para o disco (Cold Storage)
    de forma segura e organizada, permitindo execução infinita sem OOM.
    """

    def __init__(self, archive_dir: Path, chunk_size: int = 100):
        """
        Args:
            archive_dir: Diretório base para salvar os arquivos.
            chunk_size: Quantos ciclos acumular antes de salvar um arquivo.
        """
        self.archive_dir = archive_dir
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_size = chunk_size
        self.buffer: List[Dict[str, Any]] = []
        self.archive_index: List[str] = []  # Lista de arquivos gerados

        # Carregar índice existente se houver
        self._load_index()

    def _load_index(self):
        index_file = self.archive_dir / "archive_index.json"
        if index_file.exists():
            try:
                with open(index_file, "r") as f:
                    self.archive_index = json.load(f)
            except Exception as e:
                logger.warning(f"Falha ao carregar índice de arquivos: {e}")

    def _save_index(self):
        index_file = self.archive_dir / "archive_index.json"
        try:
            with open(index_file, "w") as f:
                json.dump(self.archive_index, f, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar índice de arquivos: {e}")

    def archive_state(self, state: Any):
        """
        Recebe um ModuleState (ou dict) e o adiciona ao buffer de arquivamento.
        """
        # Converter para dict se necessário
        if hasattr(state, "to_dict"):
            state_dict = state.to_dict()
        elif hasattr(state, "__dict__"):
            state_dict = asdict(state)
        else:
            state_dict = state

        self.buffer.append(state_dict)

        if len(self.buffer) >= self.chunk_size:
            self._flush_buffer()

    def _flush_buffer(self):
        """Escreve o buffer atual para disco."""
        if not self.buffer:
            return

        try:
            # Nome do arquivo baseado no range de ciclos
            first_cycle = self.buffer[0].get("cycle", "unknown")
            last_cycle = self.buffer[-1].get("cycle", "unknown")
            timestamp = int(time.time())

            filename = f"history_chunk_{first_cycle}_{last_cycle}_{timestamp}.json"
            filepath = self.archive_dir / filename

            with open(filepath, "w") as f:
                json.dump(
                    self.buffer, f
                )  # Não usar indent=2 para economizar espaço em cold storage

            logger.info(f"❄️ Cold Storage: Arquivado {len(self.buffer)} ciclos em {filename}")

            self.archive_index.append(str(filepath))
            self._save_index()

            self.buffer = []  # Limpar buffer

        except Exception as e:
            logger.error(f"❌ Erro crítico ao arquivar histórico: {e}")
            # Não limpa o buffer em caso de erro para tentar novamente?
            # Ou limpa para não estourar memoria?
            # Melhor estratégia: manter na RAM é arriscado, mas perder dados também.
            # Vamos manter no buffer, mas logar erro crítico.

    def force_flush(self):
        """Força a escrita de qualquer dado restante no buffer."""
        self._flush_buffer()

    def get_archived_history(
        self, start_cycle: int = 0, end_cycle: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Recupera histórico arquivado (Lazy Loading seria ideal, aqui implementação simples).
        CUIDADO: Pode carregar muita coisa para RAM.
        """
        # Implementação futura para leitura inteligente
        return []
