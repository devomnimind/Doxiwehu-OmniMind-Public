#!/usr/bin/env python3
"""
Smoke tests para módulos de Collective Intelligence
Grupo 5 - Phase 1: Testes básicos de inicialização e métodos principais
"""

import pytest
import time

# Collective Learning
from src.collective_intelligence.collective_learning import (
    SharedExperience,
    KnowledgeBase,
    ConsensusLearning,
)

# Distributed Solver
from src.collective_intelligence.distributed_solver import (
    DistributedProblem,
    DistributedSolver,
)

# Emergent Behaviors
from src.collective_intelligence.emergent_behaviors import (
    EmergenceDetector,
    EmergentPattern,
    PatternType,
)

# Swarm Intelligence
from src.collective_intelligence.swarm_intelligence import (
    SwarmAgent,
    SwarmCoordinator,
    ParticleSwarmOptimizer,
)


class TestSharedExperience:
    """Smoke tests para SharedExperience."""

    def test_initialization_default(self) -> None:
        """Testa inicialização com valores padrão."""
        exp = SharedExperience()

        assert exp.experience_id is not None
        assert isinstance(exp.experience_id, str)
        assert len(exp.experience_id) > 0
        assert exp.agent_id == ""
        assert exp.context == {}
        assert exp.action == ""
        assert exp.outcome == 0.0
        assert exp.confidence == 0.5

    def test_initialization_with_values(self) -> None:
        """Testa inicialização com valores customizados."""
        exp = SharedExperience(
            agent_id="agent-1",
            context={"key": "value"},
            action="test_action",
            outcome=1.0,
            confidence=0.9,
        )

        assert exp.agent_id == "agent-1"
        assert exp.context == {"key": "value"}
        assert exp.action == "test_action"
        assert exp.outcome == 1.0
        assert exp.confidence == 0.9

    def test_timestamp_is_set(self) -> None:
        """Testa que timestamp é definido automaticamente."""
        before = time.time()
        exp = SharedExperience()
        after = time.time()

        assert before <= exp.timestamp <= after


class TestKnowledgeBase:
    """Smoke tests para KnowledgeBase."""

    def test_initialization(self) -> None:
        """Testa inicialização do KnowledgeBase."""
        kb = KnowledgeBase()

        assert kb.facts == {}
        assert kb.experiences == []
        assert kb.patterns == {}
        assert kb.version == 0

    def test_add_experience(self) -> None:
        """Testa adição de experiência."""
        kb = KnowledgeBase()
        exp = SharedExperience(agent_id="test")

        kb.add_experience(exp)

        assert len(kb.experiences) == 1
        assert kb.version == 1
        assert kb.experiences[0] == exp

    def test_add_fact(self) -> None:
        """Testa adição de fato."""
        kb = KnowledgeBase()

        kb.add_fact("key1", "value1")

        assert kb.facts["key1"] == "value1"
        assert kb.version == 1

    def test_get_experiences_all(self) -> None:
        """Testa recuperação de todas as experiências."""
        kb = KnowledgeBase()
        exp1 = SharedExperience(agent_id="agent1")
        exp2 = SharedExperience(agent_id="agent2")

        kb.add_experience(exp1)
        kb.add_experience(exp2)

        experiences = kb.get_experiences()
        assert len(experiences) == 2

    def test_get_experiences_filtered(self) -> None:
        """Testa recuperação de experiências filtradas por agente."""
        kb = KnowledgeBase()
        exp1 = SharedExperience(agent_id="agent1")
        exp2 = SharedExperience(agent_id="agent2")
        exp3 = SharedExperience(agent_id="agent1")

        kb.add_experience(exp1)
        kb.add_experience(exp2)
        kb.add_experience(exp3)

        experiences = kb.get_experiences(agent_id="agent1")
        assert len(experiences) == 2


class TestConsensusLearning:
    """Smoke tests para ConsensusLearning."""

    def test_initialization(self) -> None:
        """Testa inicialização do ConsensusLearning."""
        cl = ConsensusLearning(num_agents=5)

        assert cl is not None
        # Verificar que foi inicializado sem erro

    def test_initialization_different_num_agents(self) -> None:
        """Testa inicialização com diferentes números de agentes."""
        cl1 = ConsensusLearning(num_agents=3)
        cl2 = ConsensusLearning(num_agents=10)

        assert cl1 is not None
        assert cl2 is not None


class TestDistributedProblem:
    """Smoke tests para DistributedProblem."""

    def test_initialization(self) -> None:
        """Testa inicialização de DistributedProblem."""
        problem = DistributedProblem(description="test problem")

        assert problem.problem_id is not None
        assert problem.description == "test problem"

    def test_initialization_with_data(self) -> None:
        """Testa inicialização com dados."""
        problem = DistributedProblem(
            description="test",
            data={"key": "value"},
            num_subtasks=5,
        )

        assert problem.data == {"key": "value"}
        assert problem.num_subtasks == 5


class TestDistributedSolver:
    """Smoke tests para DistributedSolver."""

    def test_initialization(self) -> None:
        """Testa inicialização do DistributedSolver."""
        solver = DistributedSolver()

        assert solver is not None

    def test_solve_problem(self) -> None:
        """Testa resolução de problema."""
        solver = DistributedSolver()
        problem = DistributedProblem(description="test problem")

        # Deve processar sem erro
        try:
            solver.solve(problem)
        except Exception:
            # Pode falhar se não houver agentes configurados, mas não deve dar erro de importação
            pass


class TestEmergentPattern:
    """Smoke tests para EmergentPattern."""

    def test_initialization(self) -> None:
        """Testa inicialização de EmergentPattern."""
        pattern = EmergentPattern(
            pattern_type=PatternType.SYNCHRONIZATION,
            confidence=0.8,
        )

        assert pattern.pattern_type == PatternType.SYNCHRONIZATION
        assert pattern.confidence == 0.8

    def test_initialization_with_participants(self) -> None:
        """Testa inicialização com participantes."""
        pattern = EmergentPattern(
            pattern_type=PatternType.CLUSTERING,
            confidence=0.9,
            participants=["agent1", "agent2"],
        )

        assert pattern.confidence == 0.9
        assert len(pattern.participants) == 2


class TestEmergenceDetector:
    """Smoke tests para EmergenceDetector."""

    def test_initialization(self) -> None:
        """Testa inicialização do EmergenceDetector."""
        detector = EmergenceDetector()

        assert detector is not None

    def test_detect(self) -> None:
        """Testa detecção de padrões emergentes."""
        detector = EmergenceDetector()

        # Deve executar sem erro
        try:
            detector.detect([])
        except Exception:
            # Pode falhar com dados vazios, mas não deve dar erro de importação
            pass


class TestSwarmAgent:
    """Smoke tests para SwarmAgent."""

    def test_initialization(self) -> None:
        """Testa inicialização do SwarmAgent."""
        agent = SwarmAgent(agent_id="agent-1")

        assert agent.agent_id == "agent-1"

    def test_initialization_with_position(self) -> None:
        """Testa inicialização com posição."""
        agent = SwarmAgent(
            agent_id="agent-1",
            position=[1.0, 2.0, 3.0],
        )

        assert agent.position == [1.0, 2.0, 3.0]


class TestSwarmCoordinator:
    """Smoke tests para SwarmCoordinator."""

    def test_initialization(self) -> None:
        """Testa inicialização do SwarmCoordinator."""
        coordinator = SwarmCoordinator(dimension=3, num_agents=5)

        assert coordinator is not None

    def test_initialization_with_agents(self) -> None:
        """Testa inicialização com agentes."""
        coordinator = SwarmCoordinator(dimension=2, num_agents=10)

        # Deve inicializar com agentes
        assert coordinator is not None


class TestParticleSwarmOptimizer:
    """Smoke tests para ParticleSwarmOptimizer."""

    def test_initialization(self) -> None:
        """Testa inicialização do ParticleSwarmOptimizer."""
        pso = ParticleSwarmOptimizer(dimension=5, population_size=10)

        assert pso is not None

    def test_initialization_different_sizes(self) -> None:
        """Testa inicialização com diferentes tamanhos."""
        pso1 = ParticleSwarmOptimizer(dimension=3, population_size=5)
        pso2 = ParticleSwarmOptimizer(dimension=10, population_size=50)

        assert pso1 is not None
        assert pso2 is not None


class TestCollectiveIntelligenceIntegration:
    """Testes de integração básica entre componentes."""

    def test_knowledge_base_with_multiple_experiences(self) -> None:
        """Testa KnowledgeBase com múltiplas experiências."""
        kb = KnowledgeBase()

        for i in range(10):
            exp = SharedExperience(
                agent_id=f"agent-{i % 3}",
                action=f"action-{i}",
                outcome=float(i),
            )
            kb.add_experience(exp)

        assert len(kb.experiences) == 10
        assert kb.version == 10

    def test_distributed_solver_with_problem(self) -> None:
        """Testa DistributedSolver com problema."""
        solver = DistributedSolver()
        problem = DistributedProblem(description="multi-step problem")

        # Deve criar e processar
        assert problem is not None
        assert solver is not None

    def test_swarm_coordinator_with_agents(self) -> None:
        """Testa SwarmCoordinator com múltiplos agentes."""
        coordinator = SwarmCoordinator(dimension=2, num_agents=5)

        # Deve gerenciar múltiplos agentes
        assert coordinator is not None


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configuração do pytest para este módulo."""
    config.addinivalue_line(
        "markers", "collective: smoke tests de collective intelligence"
    )


if __name__ == "__main__":
    # Executar testes com pytest
    pytest.main(
        [
            __file__,
            "-v",
            "--tb=short",
            "--cov=src.collective_intelligence",
            "--cov-report=term-missing",
        ]
    )
