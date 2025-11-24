"""
Collective Intelligence Module (LEGACY).

.. warning::
    This module is DEPRECATED and will be removed in future versions.
    Please use `src.swarm` (Phase 19) for Swarm Intelligence capabilities.

Provides distributed problem-solving capabilities through swarm intelligence
and emergent behavior analysis.
"""
import warnings

warnings.warn(
    "src.collective_intelligence is deprecated. Use src.swarm instead.",
    DeprecationWarning,
    stacklevel=2
)

from src.collective_intelligence.swarm_intelligence import (
    SwarmAgent,
    SwarmCoordinator,
    SwarmBehavior,
    SwarmConfiguration,
    ParticleSwarmOptimizer,
    AntColonyOptimizer,
)

from src.collective_intelligence.distributed_solver import (
    DistributedProblem,
    DistributedSolution,
    DistributedSolver,
    ConsensusProtocol,
    TaskDecomposer,
    SolutionAggregator,
)

from src.collective_intelligence.emergent_behaviors import (
    EmergentPattern,
    BehaviorRule,
    EmergenceDetector,
    PatternType,
    SelfOrganization,
    AdaptiveSystem,
)

from src.collective_intelligence.collective_learning import (
    CollectiveLearner,
    KnowledgeBase,
    SharedExperience,
    ConsensusLearning,
    FederatedLearning,
    MultiAgentTrainer,
)

__all__ = [
    # Swarm Intelligence
    "SwarmAgent",
    "SwarmCoordinator",
    "SwarmBehavior",
    "SwarmConfiguration",
    "ParticleSwarmOptimizer",
    "AntColonyOptimizer",
    # Distributed Solving
    "DistributedProblem",
    "DistributedSolution",
    "DistributedSolver",
    "ConsensusProtocol",
    "TaskDecomposer",
    "SolutionAggregator",
    # Emergent Behaviors
    "EmergentPattern",
    "BehaviorRule",
    "EmergenceDetector",
    "PatternType",
    "SelfOrganization",
    "AdaptiveSystem",
    # Collective Learning
    "CollectiveLearner",
    "KnowledgeBase",
    "SharedExperience",
    "ConsensusLearning",
    "FederatedLearning",
    "MultiAgentTrainer",
]

__version__ = "1.0.0"
