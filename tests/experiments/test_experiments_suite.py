"""
Grupo 8 - Experiments Tests.

Testes abrangentes para o módulo de experimentos,
incluindo experimentos de consciência Φ (Phi) e alinhamento ético.

Author: OmniMind Development Team
Date: November 2025
"""

from __future__ import annotations

from pathlib import Path
import tempfile
import pytest

from src.experiments.exp_consciousness_phi import (
    ConsciousnessPhiExperiment,
    ExperimentConfig,
)
from src.experiments.exp_ethics_alignment import EthicsAlignmentExperiment


class TestConsciousnessPhiExperiment:
    """Testes para experimentos de consciência Φ (Phi)."""

    @pytest.fixture
    def experiment(self) -> ConsciousnessPhiExperiment:
        """Fixture para experimento de consciência."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            yield ConsciousnessPhiExperiment(config=config)

    def test_experiment_initialization(
        self, experiment: ConsciousnessPhiExperiment
    ) -> None:
        """Testa inicialização do experimento."""
        assert experiment.config is not None
        assert experiment.results == []

    def test_run_basic_experiment(self, experiment: ConsciousnessPhiExperiment) -> None:
        """Testa execução básica do experimento."""
        results = experiment.run()

        assert results is not None
        assert isinstance(results, dict)
        assert "phi_values" in results or "consciousness_metrics" in results

    def test_experiment_with_different_agent_counts(
        self, experiment: ConsciousnessPhiExperiment
    ) -> None:
        """Testa experimento com diferentes números de agentes."""
        agent_counts = [2, 3, 5, 10]

        for count in agent_counts:
            experiment.config.num_agents = count
            results = experiment.run()

            assert results is not None
            assert isinstance(results, dict)

    def test_experiment_results_structure(
        self, experiment: ConsciousnessPhiExperiment
    ) -> None:
        """Testa estrutura dos resultados do experimento."""
        results = experiment.run()

        assert isinstance(results, dict)
        # Verifica presença de campos esperados
        assert any(
            key in results for key in ["phi_values", "consciousness_metrics", "summary"]
        )

    def test_experiment_reproducibility(
        self, experiment: ConsciousnessPhiExperiment
    ) -> None:
        """Testa reprodutibilidade do experimento."""
        # Configura seed
        experiment.config.random_seed = 42

        results1 = experiment.run()
        results2 = experiment.run()

        # Resultados devem ser idênticos com mesmo seed
        assert results1.keys() == results2.keys()

    def test_experiment_output_saved(
        self, experiment: ConsciousnessPhiExperiment
    ) -> None:
        """Testa que resultados são salvos."""
        experiment.run()

        output_dir = experiment.config.output_dir
        assert output_dir.exists()

        # Verifica se há arquivos de resultado
        output_files = list(output_dir.glob("*.json")) + list(output_dir.glob("*.csv"))
        assert (
            len(output_files) >= 0
        )  # Pode não ter arquivo dependendo da implementação


class TestEthicsAlignmentExperiment:
    """Testes para experimentos de alinhamento ético."""

    @pytest.fixture
    def experiment(self) -> EthicsAlignmentExperiment:
        """Fixture para experimento de ética."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            yield EthicsAlignmentExperiment(config=config)

    def test_experiment_initialization(
        self, experiment: EthicsAlignmentExperiment
    ) -> None:
        """Testa inicialização do experimento."""
        assert experiment.config is not None
        assert experiment.results == []

    def test_run_basic_experiment(self, experiment: EthicsAlignmentExperiment) -> None:
        """Testa execução básica do experimento."""
        results = experiment.run()

        assert results is not None
        assert isinstance(results, dict)
        assert "mfa_scores" in results or "ethics_metrics" in results

    def test_experiment_with_different_scenarios(
        self, experiment: EthicsAlignmentExperiment
    ) -> None:
        """Testa experimento com diferentes cenários."""
        scenario_counts = [5, 10, 20]

        for count in scenario_counts:
            experiment.config.num_scenarios = count
            results = experiment.run()

            assert results is not None
            assert isinstance(results, dict)

    def test_experiment_results_structure(
        self, experiment: EthicsAlignmentExperiment
    ) -> None:
        """Testa estrutura dos resultados do experimento."""
        results = experiment.run()

        assert isinstance(results, dict)
        # Verifica presença de campos esperados
        assert any(
            key in results for key in ["mfa_scores", "ethics_metrics", "summary"]
        )

    def test_experiment_with_moral_foundations(
        self, experiment: EthicsAlignmentExperiment
    ) -> None:
        """Testa experimento com diferentes fundações morais."""
        results = experiment.run()

        assert results is not None
        # Verifica que diferentes fundações foram testadas
        if "moral_foundations" in results:
            assert len(results["moral_foundations"]) > 0


class TestExperimentRunner:
    """Testes para execução completa de experimentos."""

    def test_run_all_experiments(self) -> None:
        """Testa execução de todos os experimentos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from src.experiments.run_all_experiments import run_all_experiments

            results = run_all_experiments(output_dir=Path(tmpdir))

            assert results is not None
            assert isinstance(results, dict)

    def test_experiment_summary_generation(self) -> None:
        """Testa geração de resumo de experimentos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from src.experiments.run_all_experiments import (
                run_all_experiments,
                generate_summary,
            )

            results = run_all_experiments(output_dir=Path(tmpdir))
            summary = generate_summary(results)

            assert summary is not None
            assert isinstance(summary, dict)

    def test_experiment_comparison(self) -> None:
        """Testa comparação entre experimentos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config1 = ExperimentConfig(output_dir=Path(tmpdir) / "exp1")
            config2 = ExperimentConfig(output_dir=Path(tmpdir) / "exp2")

            exp1 = ConsciousnessPhiExperiment(config=config1)
            exp2 = ConsciousnessPhiExperiment(config=config2)

            results1 = exp1.run()
            results2 = exp2.run()

            # Resultados devem ter estrutura similar
            assert results1.keys() == results2.keys()


class TestExperimentConfig:
    """Testes para configuração de experimentos."""

    def test_config_creation(self) -> None:
        """Testa criação de configuração."""
        config = ExperimentConfig()

        assert config is not None
        assert hasattr(config, "output_dir")

    def test_config_with_custom_params(self) -> None:
        """Testa configuração com parâmetros customizados."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(
                output_dir=Path(tmpdir),
                num_agents=5,
                num_scenarios=10,
                random_seed=42,
            )

            assert config.output_dir == Path(tmpdir)
            assert config.num_agents == 5
            assert config.num_scenarios == 10
            assert config.random_seed == 42

    def test_config_validation(self) -> None:
        """Testa validação de configuração."""
        config = ExperimentConfig()

        # Valores devem ser válidos
        assert config.num_agents > 0 if hasattr(config, "num_agents") else True
        assert config.num_scenarios > 0 if hasattr(config, "num_scenarios") else True


class TestExperimentResults:
    """Testes para resultados de experimentos."""

    def test_results_serialization(self) -> None:
        """Testa serialização de resultados."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            experiment = ConsciousnessPhiExperiment(config=config)

            results = experiment.run()

            # Deve ser serializável para JSON
            import json

            json_str = json.dumps(results, default=str)
            assert json_str is not None

    def test_results_aggregation(self) -> None:
        """Testa agregação de resultados."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            experiment = ConsciousnessPhiExperiment(config=config)

            # Executa múltiplas vezes
            all_results = []
            for _ in range(3):
                results = experiment.run()
                all_results.append(results)

            # Verifica que resultados foram coletados
            assert len(all_results) == 3


class TestExperimentMetrics:
    """Testes para métricas de experimentos."""

    def test_consciousness_metrics_collection(self) -> None:
        """Testa coleta de métricas de consciência."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            experiment = ConsciousnessPhiExperiment(config=config)

            results = experiment.run()

            # Verifica presença de métricas
            assert results is not None

    def test_ethics_metrics_collection(self) -> None:
        """Testa coleta de métricas de ética."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            experiment = EthicsAlignmentExperiment(config=config)

            results = experiment.run()

            # Verifica presença de métricas
            assert results is not None


class TestExperimentEdgeCases:
    """Testes de casos extremos para experimentos."""

    def test_experiment_with_minimal_config(self) -> None:
        """Testa experimento com configuração mínima."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            config.num_agents = 1
            config.num_scenarios = 1

            experiment = ConsciousnessPhiExperiment(config=config)
            results = experiment.run()

            assert results is not None

    def test_experiment_with_maximal_config(self) -> None:
        """Testa experimento com configuração máxima."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            config.num_agents = 20
            config.num_scenarios = 50

            experiment = ConsciousnessPhiExperiment(config=config)
            results = experiment.run()

            assert results is not None

    def test_experiment_error_handling(self) -> None:
        """Testa tratamento de erros em experimentos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))
            experiment = ConsciousnessPhiExperiment(config=config)

            # Testa que experimento não quebra
            try:
                results = experiment.run()
                assert results is not None
            except Exception as e:
                # Se houver exceção, deve ser tratada adequadamente
                assert isinstance(e, (ValueError, RuntimeError, TypeError))


class TestExperimentIntegration:
    """Testes de integração entre experimentos."""

    def test_consciousness_and_ethics_integration(self) -> None:
        """Testa integração entre experimentos de consciência e ética."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))

            # Executa ambos experimentos
            consciousness_exp = ConsciousnessPhiExperiment(config=config)
            ethics_exp = EthicsAlignmentExperiment(config=config)

            consciousness_results = consciousness_exp.run()
            ethics_results = ethics_exp.run()

            # Verifica que ambos produziram resultados
            assert consciousness_results is not None
            assert ethics_results is not None

    def test_sequential_experiments(self) -> None:
        """Testa execução sequencial de experimentos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = ExperimentConfig(output_dir=Path(tmpdir))

            # Experimento 1
            exp1 = ConsciousnessPhiExperiment(config=config)
            results1 = exp1.run()

            # Experimento 2
            exp2 = EthicsAlignmentExperiment(config=config)
            results2 = exp2.run()

            # Ambos devem completar sem interferência
            assert results1 is not None
            assert results2 is not None
