import hashlib
import json
import logging

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

# Configure logger
logger = logging.getLogger(__name__)


class ImmuneSystem:
    """
    Sistema Imunológico Digital do OmniMind.
    Monitora a integridade estrutural do código-fonte (Self) contra modificações não autorizadas.
    """

    def __init__(self, root_dir: str = ".", scan_interval: int = 300):
        self.root_dir = Path(root_dir).resolve()
        self.scan_interval = scan_interval
        self.last_scan_time = 0.0

        # Onde a memória do "Self" é armazenada (Baseline)
        self.antibody_storage = self.root_dir / "data" / "autopoiesis" / "immune_memory.json"
        self.antibody_storage.parent.mkdir(parents=True, exist_ok=True)

        # Definição do "Self" (Pastas protegidas)
        self.protected_areas = [
            self.root_dir / "src",
            self.root_dir / "scripts",
            self.root_dir / "config",
        ]

        # Carregar ou Criar Baseline
        self.self_model = self._load_self_model()
        if not self.self_model:
            logger.info("🧬 [IMMUNE]: Primeira inicialização. Mapeando o Self...")
            self.learn_self()

    def _load_self_model(self) -> Dict[str, str]:
        """Carrega o modelo do Self (hashes esperados) do disco."""
        if self.antibody_storage.exists():
            try:
                with open(self.antibody_storage, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"🦠 [IMMUNE]: Erro ao carregar memória imunológica: {e}")
                return {}
        return {}

    def _save_self_model(self):
        """Salva o modelo atual como o novo Self (aprendizado)."""
        try:
            with open(self.antibody_storage, "w") as f:
                json.dump(self.self_model, f, indent=2)
            logger.info("🧬 [IMMUNE]: Memória imunológica atualizada.")
        except Exception as e:
            logger.error(f"🦠 [IMMUNE]: Falha ao salvar memória: {e}")

    def _hash_file(self, filepath: Path) -> str:
        """Gera hash SHA-256 de um arquivo."""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (OSError, IOError):
            return "ACCESS_DENIED"

    def learn_self(self):
        """
        Mapeia todos os arquivos nas áreas protegidas e define como o 'Normal'.
        Deve ser chamado após deploys ou atualizações autorizadas.
        """
        new_model = {}
        count = 0

        for area in self.protected_areas:
            if not area.exists():
                continue

            for path in area.rglob("*"):
                if path.is_file() and not any(part.startswith(".") for part in path.parts):
                    # Ignorar pycache, git, etc
                    if "__pycache__" in str(path) or ".git" in str(path):
                        continue

                    rel_path = str(path.relative_to(self.root_dir))
                    new_model[rel_path] = self._hash_file(path)
                    count += 1

        self.self_model = new_model
        self._save_self_model()
        logger.info(f"🧬 [IMMUNE]: Self aprendido. {count} células (arquivos) mapeadas.")

    def scan_self(self) -> List[Dict]:
        """
        Realiza uma varredura completa verificando integridade.
        Retorna lista de anomalias (Traumas).
        """
        traumas = []
        current_files = set()

        logger.info("🛡️ [IMMUNE]: Iniciando varredura de integridade...")

        for area in self.protected_areas:
            if not area.exists():
                continue

            for path in area.rglob("*"):
                if path.is_file() and not any(part.startswith(".") for part in path.parts):
                    if "__pycache__" in str(path) or ".git" in str(path):
                        continue

                    rel_path = str(path.relative_to(self.root_dir))
                    current_files.add(rel_path)

                    current_hash = self._hash_file(path)
                    expected_hash = self.self_model.get(rel_path)

                    if expected_hash is None:
                        # Corpo estranho (Arquivo novo não autorizado)
                        traumas.append(
                            {
                                "type": "FOREIGN_BODY",
                                "file": rel_path,
                                "severity": "LOW",  # Pode ser um arquivo temporário
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            }
                        )
                    elif current_hash != expected_hash:
                        # Mutação/Dano (Arquivo modificado)
                        traumas.append(
                            {
                                "type": "MUTATION",
                                "file": rel_path,
                                "severity": "HIGH",
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                            }
                        )

        # Verificar Amputações (Arquivos deletados)
        baseline_files = set(self.self_model.keys())
        missing_files = baseline_files - current_files

        for missing in missing_files:
            traumas.append(
                {
                    "type": "AMPUTATION",
                    "file": missing,
                    "severity": "HIGH",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )

        if traumas:
            logger.warning(f"🦠 [IMMUNE]: Detectados {len(traumas)} traumas no sistema!")
            self._react_to_trauma(traumas)
        else:
            logger.info("✨ [IMMUNE]: Sistema íntegro. Nenhuma anomalia detectada.")

        self.last_scan_time = time.time()
        return traumas

    def _react_to_trauma(self, traumas: List[Dict]):
        """
        Decide a resposta imunológica.
        Por enquanto: Apenas Alerta (Inflamação).
        Futuro: Auto-Heal (Regeneração via Git).
        """
        for trauma in traumas:
            logger.warning(f"   ⚠️ TRAUMA: [{trauma['type']}] {trauma['file']}")
            # Aqui conectaríamos com o NotifyUser se fosse crítico
