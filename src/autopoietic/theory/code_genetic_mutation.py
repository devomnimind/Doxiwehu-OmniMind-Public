import difflib
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import json

# Configure logger
logger = logging.getLogger(__name__)


class GeneticMutator:
    """
    Motor de Evolução Genética do OmniMind.
    Responsável por analisar o próprio código fonte (DNA) e propor mutações (Pull Requests/Patches)
    para otimização, correção ou expansão de funcionalidades.
    """

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.mutation_storage = self.root_dir / "data" / "autopoiesis" / "mutations"
        self.mutation_storage.mkdir(parents=True, exist_ok=True)

        # Histórico de Evolução
        self.evolution_log = self.root_dir / "data" / "autopoiesis" / "evolution_history.jsonl"

    def list_genes(self, protected_areas: List[Path] = None) -> List[Path]:
        """Lista todos os arquivos de código (Genes) editáveis."""
        if not protected_areas:
            protected_areas = [self.root_dir / "src"]

        genes = []
        for area in protected_areas:
            if not area.exists():
                continue
            for path in area.rglob("*.py"):
                genes.append(path)
        return genes

    def propose_mutation(
        self, target_file: str, instruction: str, new_content: str
    ) -> Optional[str]:
        """
        Cria uma proposta de mutação (Patch) baseada em uma instrução.
        NÃO APLICA A MUDANÇA (Safety First). Apenas gera o arquivo .patch.
        """
        target_path = (self.root_dir / target_file).resolve()
        if not target_path.exists():
            logger.error(f"🧬 [GENETICS]: Alvo não encontrado: {target_file}")
            return None

        try:
            # 1. Ler DNA atual
            original_code = target_path.read_text().splitlines(keepends=True)
            new_code_lines = new_content.splitlines(keepends=True)

            # 2. Gerar Diferença (Unified Diff)
            diff = difflib.unified_diff(
                original_code,
                new_code_lines,
                fromfile=f"a/{target_file}",
                tofile=f"b/{target_file}",
                lineterm="",
            )

            patch_content = "".join(diff)
            if not patch_content:
                logger.info(f"🧬 [GENETICS]: Nenhuma mutação necessária para {target_file}.")
                return None

            # 3. Salvar Mutação
            mutation_id = f"mutation_{int(time.time())}_{hash(instruction) % 10000}"
            patch_filename = f"{mutation_id}.patch"
            patch_path = self.mutation_storage / patch_filename

            # Metadata da Mutação
            metadata = {
                "id": mutation_id,
                "target": target_file,
                "goal": instruction,
                "timestamp": datetime.now().isoformat(),
                "status": "PROPOSED",
            }

            # Salvar .patch e .json
            patch_path.write_text(patch_content)
            (self.mutation_storage / f"{mutation_id}.json").write_text(
                json.dumps(metadata, indent=2)
            )

            logger.info(f"🧬 [GENETICS]: Mutação proposta salva em {patch_path}")
            self._log_history("PROPOSAL", metadata)

            return str(patch_path)

        except Exception as e:
            logger.error(f"🧬 [GENETICS]: Falha na transcrição genética: {e}")
            return None

    def _log_history(self, action: str, details: Dict):
        """Registra o histórico evolutivo."""
        entry = {"action": action, "details": details, "timestamp": datetime.now().isoformat()}
        with open(self.evolution_log, "a") as f:
            f.write(json.dumps(entry) + "\n")


# Exemplo de Teste Unitário (Self-Test)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mutator = GeneticMutator()
    print(f"Genes encontrados: {len(mutator.list_genes())}")

    # Simular uma mutação em si mesmo (Meta-Evolução)
    self_path = "src/autopoiesis/code_genetic_mutation.py"
    if (Path(self_path)).exists():
        original = Path(self_path).read_text()
        # Adicionar um comentário
        mutated = original + "\n# Mutação de Teste: Evolução detectada.\n"
        mutator.propose_mutation(self_path, "Adicionar comentário de teste", mutated)
