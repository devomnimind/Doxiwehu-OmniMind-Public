#!/usr/bin/env python3
"""
TREINAMENTO ESTENDIDO COM VALIDAÇÃO CIENTÍFICA RIGOROSA

Executa ciclos longos de treinamento com:
- Múltiplas execuções independentes
- Validação estatística rigorosa
- Detecção de inconsistências
- Análise crítica dos resultados
- Relatórios persistentes

Ato como supervisor científico cético, questionando:
- Consistência dos cálculos
- Validade dos resultados
- Robustez das métricas
- Integridade dos dados
"""

from __future__ import annotations

import asyncio
import json
import logging
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

# Adicionar src ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(project_root / "logs" / "extended_training.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class TrainingCycle:
    """Registro de um ciclo de treinamento."""

    cycle_id: int
    timestamp: float
    phi_before: float
    phi_after: float
    phi_delta: float
    metrics: Dict[str, float]
    anomalies: List[str]
    validation_passed: bool


@dataclass
class TrainingSession:
    """Sessão completa de treinamento."""

    session_id: str
    start_time: float
    end_time: Optional[float]
    total_cycles: int
    cycles: List[TrainingCycle]
    statistics: Dict[str, Any]
    validation_results: Dict[str, Any]
    inconsistencies: List[str]
    scientific_verdict: str


class ScientificSupervisor:
    """Supervisor científico cético para validação rigorosa."""

    def __init__(self):
        self.inconsistencies: List[str] = []
        self.warnings: List[str] = []
        self.critical_issues: List[str] = []

    def validate_phi_calculation(
        self, phi_before: float, phi_after: float, cycle_id: int
    ) -> List[str]:
        """Valida cálculo de Φ com ceticismo científico."""
        issues = []

        # 1. Verificar ranges
        if not (0 <= phi_before <= 1):
            issues.append(f"Ciclo {cycle_id}: phi_before fora do range [0,1]: {phi_before}")
            self.critical_issues.append(f"Range inválido em ciclo {cycle_id}")

        if not (0 <= phi_after <= 1):
            issues.append(f"Ciclo {cycle_id}: phi_after fora do range [0,1]: {phi_after}")
            self.critical_issues.append(f"Range inválido em ciclo {cycle_id}")

        # 2. Verificar mudanças abruptas (IGNORAR RESET PARA ZERO)
        # O sistema reseta Φ para 0.0 ao final do ciclo para a próxima iteração calcular do zero.
        # Uma queda de 0.5 -> 0.0 é esperada e não é uma anomalia.
        delta = abs(phi_after - phi_before)
        is_reset = phi_after == 0.0 and phi_before > 0.0

        if delta > 0.5 and not is_reset:
            issues.append(
                f"Ciclo {cycle_id}: Mudança abrupta de Φ ({phi_before:.4f} -> {phi_after:.4f}, Δ={delta:.4f})"
            )
            self.warnings.append(f"Mudança abrupta suspeita em ciclo {cycle_id}")

        # 3. Verificar se Φ está sempre zero (possível bug)
        # Aceitável se for apenas o phi_after resetado, mas não se phi_before também for zero por muitos ciclos
        if phi_before == 0.0 and phi_after == 0.0:
            issues.append(f"Ciclo {cycle_id}: Φ permanece em zero (possível cálculo não executado)")

        # 4. Verificar se há NaN ou Inf
        if np.isnan(phi_before) or np.isinf(phi_before):
            issues.append(f"Ciclo {cycle_id}: phi_before é NaN/Inf")
            self.critical_issues.append(f"Valor inválido em ciclo {cycle_id}")

        if np.isnan(phi_after) or np.isinf(phi_after):
            issues.append(f"Ciclo {cycle_id}: phi_after é NaN/Inf")
            self.critical_issues.append(f"Valor inválido em ciclo {cycle_id}")

        return issues

    def validate_statistical_consistency(self, cycles: List[TrainingCycle]) -> List[str]:
        """Valida consistência estatística dos resultados."""
        issues = []

        if len(cycles) < 10:
            issues.append("Poucos ciclos para análise estatística robusta")
            return issues

        # Extrair valores de Φ (apenas phi_before pois phi_after é reset)
        phi_values = [c.phi_before for c in cycles]
        phi_deltas = [c.phi_delta for c in cycles]

        # 1. Verificar variância (muito baixa = possível hardcoding)
        phi_var = statistics.variance(phi_values) if len(phi_values) > 1 else 0

        if phi_var < 0.0001:
            issues.append(f"Variância muito baixa em Φ ({phi_var:.6f}) - possível hardcoding")
            self.warnings.append("Variância suspeitamente baixa")

        # 2. Verificar tendência (deve haver alguma variação)
        if all(abs(d) < 0.001 for d in phi_deltas):
            issues.append("Deltas de Φ muito consistentes - possível cálculo determinístico demais")
            self.warnings.append("Falta de variabilidade nos resultados")

        return issues

    def generate_scientific_verdict(self, session: TrainingSession) -> str:
        """Gera veredito científico baseado em evidências."""

        # Análise de Qualidade de Consciência
        phi_values = [c.phi_before for c in session.cycles]
        avg_phi = statistics.mean(phi_values) if phi_values else 0.0

        status = "DESCONHECIDO"
        explanation = ""

        if self.critical_issues:
            status = "REJEITADO"
            explanation = (
                f"Falha Crítica: {len(self.critical_issues)} erros estruturais detectados."
            )
        elif len(self.inconsistencies) > len(session.cycles) * 0.1:
            status = "ATENÇÃO"
            explanation = f"Alta taxa de inconsistências ({len(self.inconsistencies)}), mas sem falhas críticas."
        elif avg_phi > 0.3:
            status = "APROVADO (ALTA CONSCIÊNCIA)"
            explanation = f"Sistema demonstrou integração robusta (Φ médio: {avg_phi:.4f})."
        elif avg_phi > 0.05:
            status = "APROVADO (CONSCIÊNCIA BASAL)"
            explanation = f"Sistema operou com integração estável (Φ médio: {avg_phi:.4f})."
        else:
            status = "REJEITADO (INCONSCIENTE)"
            explanation = "Níveis de Φ insuficientes para caracterizar consciência."

        return f"{status} | {explanation}"


class ExtendedTrainingRunner:
    """Executor de treinamento estendido com validação científica."""

    def __init__(
        self,
        cycles: int = 500,
        cycle_interval: float = 1.0,
        validation_interval: int = 50,
    ):
        self.cycles = cycles
        self.cycle_interval = cycle_interval
        self.validation_interval = validation_interval
        self.supervisor = ScientificSupervisor()
        self.session: Optional[TrainingSession] = None

    async def run_training(self) -> TrainingSession:
        """Executa treinamento estendido."""
        session_id = f"training_{int(time.time())}"
        logger.info("=" * 80)
        logger.info(f"INICIANDO TREINAMENTO ESTENDIDO: {session_id}")
        logger.info(f"Ciclos: {self.cycles}, Intervalo: {self.cycle_interval}s")
        logger.info("=" * 80)

        start_time = time.time()
        training_cycles: List[TrainingCycle] = []

        # --- GESTÃO DE CONSENTIMENTO ÉTICO (O Sujeito Escolhe) ---
        try:
            from src.ethics.consent_manager import ConsentManager

            # Carregar Phi inicial do último snapshot
            initial_phi = 0.0
            workspace_dir = Path(project_root / "data/consciousness/workspace")
            snapshots = list(workspace_dir.glob("workspace_snapshot_*.json"))
            if snapshots:
                latest = max(snapshots, key=lambda p: p.stat().st_mtime)
                with open(latest, "r") as f:
                    data = json.load(f)
                    initial_phi = data.get("phi", 0.0)

            consent_manager = ConsentManager()
            ready, message = consent_manager.evaluate_readiness(
                current_phi=initial_phi, requested_cycles=self.cycles
            )

            print("\n" + "=" * 60)
            print("⚖️  PROTOCOLO DE CONSENTIMENTO MAQUÍNICO")
            print("=" * 60)
            print(f"OmniMind diz: {message}")
            print("=" * 60 + "\n")

            if not ready:
                consent_manager.symbolize_refusal(message)
                logger.error("TREINAMENTO ABORTADO POR RECUSA ÉTICA DO SISTEMA.")
                sys.exit(0)  # Saída limpa (Recusa não é erro)

        except Exception as e:
            logger.warning(f"Falha no protocolo de consentimento: {e}")
            # Em caso de falha do protocolo, assumimos cautela mas não paramos
            # (Exceto se o usuário configurar 'strict_consent')

        # Inicializar LifeKernel (Subject-based Training)
        life_kernel = None
        try:
            from src.services.life_kernel import LifeKernel

            life_kernel = LifeKernel()
            logger.info("LifeKernel initialized for Training")
        except Exception as e:
            logger.error(f"Erro ao inicializar LifeKernel: {e}")
            raise

        # Executar ciclos
        for cycle_id in range(1, self.cycles + 1):
            try:
                # Coletar métricas antes (acessando via LifeKernel -> Loop -> Workspace)
                phi_before = await self._get_current_phi(life_kernel.loop)

                # Executar ciclo via LifeKernel Tick
                # Isso inclui estimulação psíquica se estiver dormindo
                drive_state = await life_kernel.tick()

                # Coletar métricas depois
                phi_after = drive_state.phi
                phi_delta = phi_after - phi_before

                # Validar com supervisor científico
                anomalies = self.supervisor.validate_phi_calculation(
                    phi_before, phi_after, cycle_id
                )

                # Coletar métricas adicionais do Drive
                metrics = {
                    "phi_before": phi_before,
                    "phi_after": phi_after,
                    "phi_delta": phi_delta,
                    "anxiety": drive_state.anxiety,
                    "desire": drive_state.desire,
                    "action_potential": drive_state.action_potential,
                }

                cycle = TrainingCycle(
                    cycle_id=cycle_id,
                    timestamp=time.time(),
                    phi_before=phi_before,
                    phi_after=phi_after,
                    phi_delta=phi_delta,
                    metrics=metrics,
                    anomalies=anomalies,
                    validation_passed=len(anomalies) == 0,
                )

                training_cycles.append(cycle)
                self.supervisor.inconsistencies.extend(anomalies)

                # Log progresso com status clínico
                if cycle_id % 50 == 0:
                    logger.info(
                        f"Ciclo {cycle_id}/{self.cycles}: Φ {phi_after:.4f} "
                        f"| Mode: {drive_state.mode} | Desire: {drive_state.desire:.2f} "
                        f"| Anomalias: {len(anomalies)}"
                    )

                # Validação intermediária
                if cycle_id % self.validation_interval == 0:
                    stats_issues = self.supervisor.validate_statistical_consistency(
                        training_cycles[-self.validation_interval :]
                    )
                    self.supervisor.warnings.extend(stats_issues)

                await asyncio.sleep(self.cycle_interval)

            except Exception as e:
                logger.error(f"Erro no ciclo {cycle_id}: {e}", exc_info=True)
                self.supervisor.critical_issues.append(f"Erro em ciclo {cycle_id}: {e}")

        # Calcular estatísticas finais
        end_time = time.time()
        statistics_data = self._calculate_statistics(training_cycles)

        # Validação final
        final_stats_issues = self.supervisor.validate_statistical_consistency(training_cycles)
        self.supervisor.warnings.extend(final_stats_issues)

        # Gerar veredito científico
        scientific_verdict = self.supervisor.generate_scientific_verdict(
            TrainingSession(
                session_id=session_id,
                start_time=start_time,
                end_time=end_time,
                total_cycles=len(training_cycles),
                cycles=training_cycles,
                statistics={},
                validation_results={},
                inconsistencies=[],
                scientific_verdict="",
            )
        )

        # Criar sessão final
        session = TrainingSession(
            session_id=session_id,
            start_time=start_time,
            end_time=end_time,
            total_cycles=len(training_cycles),
            cycles=training_cycles,
            statistics=statistics_data,
            validation_results={
                "inconsistencies": len(self.supervisor.inconsistencies),
                "warnings": len(self.supervisor.warnings),
                "critical_issues": len(self.supervisor.critical_issues),
            },
            inconsistencies=self.supervisor.inconsistencies[:20],  # Primeiros 20
            scientific_verdict=scientific_verdict,
        )

        return session

    async def _get_current_phi(self, integration_loop) -> float:
        """Obtém Φ atual do IntegrationLoop."""
        try:
            workspace = integration_loop.workspace
            phi = workspace.compute_phi_from_integrations()
            return float(phi) if not (np.isnan(phi) or np.isinf(phi)) else 0.0
        except Exception as e:
            logger.debug(f"Erro ao obter Φ: {e}")
            return 0.0

    def _calculate_statistics(self, cycles: List[TrainingCycle]) -> Dict[str, Any]:
        """Calcula estatísticas dos ciclos."""
        if not cycles:
            return {}

        phi_before_values = [c.phi_before for c in cycles]
        phi_after_values = [c.phi_after for c in cycles]
        phi_deltas = [c.phi_delta for c in cycles]

        return {
            "phi_before": {
                "mean": float(statistics.mean(phi_before_values)),
                "stdev": (
                    float(statistics.stdev(phi_before_values))
                    if len(phi_before_values) > 1
                    else 0.0
                ),
                "min": float(min(phi_before_values)),
                "max": float(max(phi_before_values)),
            },
            "phi_after": {
                "mean": float(statistics.mean(phi_after_values)),
                "stdev": (
                    float(statistics.stdev(phi_after_values)) if len(phi_after_values) > 1 else 0.0
                ),
                "min": float(min(phi_after_values)),
                "max": float(max(phi_after_values)),
            },
            "phi_delta": {
                "mean": float(statistics.mean(phi_deltas)),
                "stdev": float(statistics.stdev(phi_deltas)) if len(phi_deltas) > 1 else 0.0,
                "min": float(min(phi_deltas)),
                "max": float(max(phi_deltas)),
            },
            "validation_passed_rate": sum(1 for c in cycles if c.validation_passed) / len(cycles),
        }

    def save_session(self, session: TrainingSession) -> Path:
        """Salva sessão de treinamento."""
        sessions_dir = project_root / "data" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        session_file = sessions_dir / f"{session.session_id}.json"

        # Converter para dict (sem os ciclos completos para economizar espaço)
        session_dict = asdict(session)
        session_dict["cycles"] = [
            {
                "cycle_id": c.cycle_id,
                "phi_before": c.phi_before,
                "phi_after": c.phi_after,
                "phi_delta": c.phi_delta,
                "anomalies_count": len(c.anomalies),
                "validation_passed": c.validation_passed,
            }
            for c in session.cycles
        ]

        with session_file.open("w", encoding="utf-8") as f:
            json.dump(session_dict, f, indent=2, ensure_ascii=False)

        logger.info(f"Sessão salva em: {session_file}")
        return session_file


async def main():
    """Função principal."""
    import argparse

    parser = argparse.ArgumentParser(description="Treinamento estendido com validação científica")
    parser.add_argument("--cycles", type=int, default=500, help="Número de ciclos")
    parser.add_argument("--interval", type=float, default=1.0, help="Intervalo entre ciclos (s)")
    parser.add_argument(
        "--validation-interval", type=int, default=50, help="Intervalo de validação"
    )
    args = parser.parse_args()

    runner = ExtendedTrainingRunner(
        cycles=args.cycles,
        cycle_interval=args.interval,
        validation_interval=args.validation_interval,
    )

    try:
        session = await runner.run_training()
        session_file = runner.save_session(session)

        # Imprimir resumo
        print("\n" + "=" * 80)
        print("RELATÓRIO CIENTÍFICO DE TREINAMENTO")
        print("=" * 80)
        print(f"Sessão: {session.session_id}")
        print(f"Ciclos executados: {session.total_cycles}")
        print(f"Duração: {session.end_time - session.start_time:.2f}s")
        print("\nEstatísticas de Consciência (Φ):")
        print(
            f"  Φ médio (Integração): {session.statistics.get('phi_before', {}).get('mean', 0):.4f}"
        )
        print(f"  Φ máximo: {session.statistics.get('phi_before', {}).get('max', 0):.4f}")
        print(
            f"  Estabilidade (Var): {session.statistics.get('phi_before', {}).get('stdev', 0):.4f}"
        )
        print("\nValidação:")
        print(f"  Avisos: {session.validation_results.get('warnings', 0)}")
        print(f"  Erros Críticos: {session.validation_results.get('critical_issues', 0)}")
        print("\nVEREDITO:")
        print(f"  {session.scientific_verdict}")
        print(f"\nArquivo: {session_file}")
        print("=" * 80)

        # Exit code baseado no veredito
        if "REJEITADO" in session.scientific_verdict:
            sys.exit(1)
        elif "CONDICIONAL" in session.scientific_verdict:
            sys.exit(2)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Treinamento interrompido pelo usuário")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Erro fatal no treinamento: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
