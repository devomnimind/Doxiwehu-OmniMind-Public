import os
import logging
import hashlib
import argparse
from typing import List, Dict, Any, Generator, Optional
from pathlib import Path
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/library_indexing.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Constants
COLLECTION_NAME = "universal_machine_embeddings"
QDRANT_URL = os.getenv("OMNIMIND_QDRANT_URL", "http://localhost:6333")
BATCH_SIZE = 50
CHECKPOINT_FILE = "data/library_indexing_checkpoint.txt"
MAX_FILE_SIZE_MB = 100  # Skip files larger than 100MB to avoid OOM
STRATEGIC_CHUNK_SIZE = 1000  # Characters


class LibraryIndexer:
    def __init__(self, base_paths: List[str]):
        self.base_paths = [Path(p).resolve() for p in base_paths]
        self.client = QdrantClient(url=QDRANT_URL)
        logger.info(f"💾 Loading Embedding Model (CPU optimized)...")
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2", device="cpu"
        )  # Use CPU to save GPU for training
        self._ensure_collection()
        self.processed_files = self._load_checkpoint()
        logger.info(
            f"✅ Initialized. Found {len(self.processed_files)} previously processed files."
        )

    def _ensure_collection(self):
        try:
            self.client.get_collection(COLLECTION_NAME)
        except Exception:
            logger.info(f"Collection {COLLECTION_NAME} not found. Creating...")
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )

    def _load_checkpoint(self) -> set:
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, "r") as f:
                return set(line.strip() for line in f)
        return set()

    def _save_checkpoints_batch(self, filepaths: List[str]):
        with open(CHECKPOINT_FILE, "a") as f:
            for fp in filepaths:
                f.write(f"{fp}\n")

    def _compute_id(self, key_str: str) -> str:
        """Computes a stable ID based on path + chunk identifier."""
        return hashlib.md5(key_str.encode()).hexdigest()

    def _extract_text_from_pdf(self, path: Path) -> str:
        try:
            import pypdf

            # Check file size
            if path.stat().st_size > MAX_FILE_SIZE_MB * 1024 * 1024:
                logger.warning(
                    f"⏩ Skipping huge PDF {path.name} ({path.stat().st_size // 1024 // 1024}MB)"
                )
                return ""

            reader = pypdf.PdfReader(path)

            # Check if encrypted
            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except:
                    logger.warning(f"🔒 PDF Encrypted: {path.name}")
                    return ""

            num_pages = len(reader.pages)
            if num_pages == 0:
                return ""

            # Strategic Extraction: Start, Middle, End
            # Don't read whole file if too big
            pages_to_read = []

            # Always read start (Intro/TOC)
            pages_to_read.extend(range(0, min(5, num_pages)))

            # Read middle
            if num_pages > 20:
                mid = num_pages // 2
                pages_to_read.extend(range(mid, min(mid + 3, num_pages)))

            # Read end (Conclusion/Index)
            if num_pages > 10:
                pages_to_read.extend(range(max(num_pages - 3, 0), num_pages))

            pages_to_read = sorted(list(set(pages_to_read)))

            text = []
            for p_num in pages_to_read:
                try:
                    page_text = reader.pages[p_num].extract_text()
                    if page_text:
                        text.append(page_text)
                except Exception:
                    continue

            return "\n".join(text)

        except Exception as e:
            logger.warning(f"❌ Failed to read PDF {path.name}: {e}")
            return ""

    def _extract_text_from_epub(self, path: Path) -> str:
        try:
            import ebooklib
            from ebooklib import epub
            from bs4 import BeautifulSoup

            # Suppress ebooklib warnings
            logging.getLogger("ebooklib").setLevel(logging.ERROR)

            book = epub.read_epub(str(path))
            text = []
            count = 0
            # Limit chunks to avoid huge EPUB parsing
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), "html.parser")
                    t = soup.get_text()
                    if len(t) > 200:
                        text.append(t)
                        count += 1
                        if count > 20:  # Limit to 20 chapters/sections per book
                            break
            return "\n".join(text)
        except Exception as e:
            logger.warning(f"❌ Failed to read EPUB {path.name}: {e}")
            return ""

    def process_file_content(self, path: Path) -> Optional[Dict[str, Any]]:
        """Reads file logic with format dispatch."""
        suffix = path.suffix.lower()
        content = ""

        if suffix == ".pdf":
            content = self._extract_text_from_pdf(path)
        elif suffix == ".epub":
            content = self._extract_text_from_epub(path)
        elif suffix in [".txt", ".md", ".markdown"]:
            try:
                if path.stat().st_size < MAX_FILE_SIZE_MB * 1024 * 1024:
                    content = path.read_text(errors="ignore")
            except Exception:
                pass

        if not content:
            return None

        if len(content.strip()) < 100:
            # Maybe scanned image only?
            return None

        return {"filename": path.name, "content": content, "format": suffix}

    def strategic_chunking(self, content: str) -> List[str]:
        """
        Splits content into strategic chunks (Start, 25%, 50%, 75%, End)
        instead of indexing everything.
        """
        total_len = len(content)
        if total_len <= STRATEGIC_CHUNK_SIZE * 2:
            return [content]

        chunks = []

        # 1. Beginning
        chunks.append(content[:STRATEGIC_CHUNK_SIZE])

        # 2. Middle segments
        steps = [0.25, 0.5, 0.75]
        for step in steps:
            idx = int(total_len * step)
            end = min(total_len, idx + STRATEGIC_CHUNK_SIZE)
            chunks.append(content[idx:end])

        # 3. End
        chunks.append(content[-STRATEGIC_CHUNK_SIZE:])

        # Filter too small / duplicates
        unique_chunks = sorted(list(set([c for c in chunks if len(c) > 100])))
        return unique_chunks

    def discover_files(self) -> Generator[Path, None, None]:
        """Robust recursive file discovery using os.walk."""
        valid_extensions = {".pdf", ".epub", ".txt", ".md", ".markdown"}

        for base_path in self.base_paths:
            if not base_path.exists():
                logger.warning(f"⚠️ Path not found: {base_path}")
                continue

            logger.info(f"📂 Scanning directory: {base_path}")
            for root, dirs, files in os.walk(base_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith(".")]

                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix.lower() in valid_extensions:
                        yield file_path

    def index(self):
        current_batch = []
        processed_in_session = 0
        total_vectors = 0

        file_generator = self.discover_files()

        logger.info("🚀 Starting robust indexing process...")

        try:
            for file_path in file_generator:
                str_path = str(file_path)

                if str_path in self.processed_files:
                    continue

                try:
                    data = self.process_file_content(file_path)

                    if data:
                        # Strategic Chunking
                        chunks = self.strategic_chunking(data["content"])

                        for i, chunk in enumerate(chunks):
                            embedding = self.model.encode(chunk).tolist()

                            vector_id = self._compute_id(f"{str_path}_{i}")

                            payload = {
                                "source": "robust_library_indexer",
                                "folder": str(file_path.parent),
                                "filename": data["filename"],
                                "path": str_path,
                                "format": data["format"],
                                "content_snippet": chunk[:200],  # Preview
                                "chunk_index": i,
                                "total_chunks_extracted": len(chunks),
                                "full_text_length": len(data["content"]),
                                "indexed_at": datetime.now().isoformat(),
                            }

                            point = PointStruct(id=vector_id, vector=embedding, payload=payload)
                            current_batch.append(point)
                            total_vectors += 1

                        processed_in_session += 1

                        # Add to processed list (optimistic)
                        self.processed_files.add(str_path)

                        # Print progress every 10 files
                        if processed_in_session % 10 == 0:
                            print(
                                f"📚 Processed {processed_in_session} files... (Vectors: {total_vectors})",
                                end="\r",
                            )

                        # Upsert batch
                        if len(current_batch) >= BATCH_SIZE:
                            self.client.upsert(
                                collection_name=COLLECTION_NAME, points=current_batch
                            )

                            # Save checkpoints for all files in this batch's chunks
                            # We can just save the set of files processed in this batch
                            files_in_batch = set(p.payload["path"] for p in current_batch)
                            self._save_checkpoints_batch(list(files_in_batch))

                            current_batch = []

                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    logger.error(f"❌ Error processing {file_path.name}: {e}")
                    continue

            # Final batch
            if current_batch:
                self.client.upsert(collection_name=COLLECTION_NAME, points=current_batch)
                files_in_batch = set(p.payload["path"] for p in current_batch)
                self._save_checkpoints_batch(list(files_in_batch))

            logger.info(
                f"\n✅ Indexing Complete! Processed {processed_in_session} new files. Total vectors: {total_vectors}"
            )

        except KeyboardInterrupt:
            logger.info("\n⚠️ Indexing interrupted by user. Checkpoints saved.")
            # Try to save last batch if exists
            if current_batch:
                logger.info("Saving pending batch...")
                self.client.upsert(collection_name=COLLECTION_NAME, points=current_batch)
                files_in_batch = set(p.payload["path"] for p in current_batch)
                self._save_checkpoints_batch(list(files_in_batch))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OmniMind Robust Library Indexer")
    parser.add_argument(
        "paths",
        metavar="path",
        type=str,
        nargs="*",
        help="Paths to index (directories)",
        default=[
            "data/library_sources/free-livros",
            "data/library_sources/BibliotecaDev",
            "/home/fahbrain/Downloads/Livros",
        ],
    )

    args = parser.parse_args()

    print(f"🔍 Indexing Locations: {args.paths}")

    indexer = LibraryIndexer(args.paths)
    indexer.index()
