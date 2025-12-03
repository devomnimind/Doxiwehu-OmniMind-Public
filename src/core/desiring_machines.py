"""
Máquinas Desejantes (Deleuze-Guattari)

Princípios:
1. Cada máquina PRODUZ desejo (não consome)
2. Desejo = fluxo de energia/informação
3. Máquinas conectam formando rhizoma
4. Nenhuma hierarquia (anti-Édipo)
5. Multiplicidade sem síntese forçada
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List


class DesireIntensity(Enum):
    MINIMAL = 0.1  # Desejo fraco (modo sleep)
    LOW = 0.3
    NORMAL = 0.6
    HIGH = 0.8
    INTENSIVE = 1.0  # Pico (linha de fuga)


@dataclass
class DesireFlow:
    """Fluxo de desejo entre máquinas."""

    source_id: str  # Qual máquina produz
    target_id: str  # Qual máquina recebe
    intensity: DesireIntensity  # Força do desejo
    payload: Any  # O que flui
    timestamp: datetime = field(default_factory=datetime.now)
    flow_type: str = "smooth"  # "smooth" (decoded) ou "striated" (coded)

    def is_decoded(self) -> bool:
        """É fluxo não-codificado (livre)?"""
        return self.flow_type == "smooth"


class DesiringMachine(ABC):
    """
    Máquina Desejante Abstrata.

    Cada módulo OmniMind é uma instância (Quantum, NLP, Topology, etc.)
    """

    def __init__(
        self,
        machine_id: str,
        production_function: Callable[..., Any],
        desire_intensity: DesireIntensity = DesireIntensity.NORMAL,
    ):
        self.id = machine_id
        self.production_function = production_function  # O que máquina produz
        self.desire_intensity = desire_intensity
        self.incoming_flows: List[DesireFlow] = []
        self.outgoing_connections: List["DesiringMachine"] = []
        self.state = {}  # Estado interno da máquina
        self.production_history = []  # Log de produções (BwO residue)

    async def produce(self, inputs: Any = None) -> Any:
        """
        PRODUZ desejo.

        D&G: Produção desejante é o real, antes de significação.
        Máquina não "processa" input, mas PRODUZ output (energia).
        """
        # 1. Coleta fluxos entrantes
        accumulated_flows = self._accumulate_incoming_flows()

        # 2. PRODUZ (não transforma - cria do nada)
        output = await self.production_function(inputs, accumulated_flows)

        # 3. Propaga para máquinas conectadas (fluxos saintes)
        for connection in self.outgoing_connections:
            await self._send_desire_flow(connection, output)

        # 4. Registra no histórico (residue = BwO)
        self.production_history.append(
            {
                "timestamp": datetime.now(),
                "input": inputs,
                "output": output,
                "intensity": self.desire_intensity.value,
            }
        )

        return output

    def _accumulate_incoming_flows(self) -> Dict[str, Any]:
        """Acumula fluxos de máquinas conectadas."""
        accumulated = {}
        for flow in self.incoming_flows:
            accumulated[flow.source_id] = flow.payload
        return accumulated

    async def _send_desire_flow(self, target: "DesiringMachine", payload: Any):
        """Envia fluxo desejante para máquina alvo."""
        flow = DesireFlow(
            source_id=self.id,
            target_id=target.id,
            intensity=self.desire_intensity,
            payload=payload,
            flow_type=self._determine_flow_type(),
        )
        target.incoming_flows.append(flow)

    def _determine_flow_type(self) -> str:
        """Determina se fluxo é smooth (decoded) ou striated (coded)."""
        # Simplificado: alta intensidade = smooth (linha de fuga)
        if self.desire_intensity.value > 0.7:
            return "smooth"
        return "striated"

    @abstractmethod
    def get_desire_description(self) -> str:
        """Qual é o desejo essencial desta máquina?"""
        pass


class QuantumDesiringMachine(DesiringMachine):
    """Máquina desejante especializada em quantum."""

    def __init__(self):
        super().__init__(
            machine_id="quantum",
            production_function=self._solve_quantum,
            desire_intensity=DesireIntensity.HIGH,
        )

    async def _solve_quantum(self, circuit: Any, incoming_flows: Dict[str, Any]) -> Dict[str, Any]:
        """Produz solução quântica."""
        # Implementação real: GPU-accelerated quantum simulation
        return {"result": "quantum_output", "flows": incoming_flows}

    def get_desire_description(self) -> str:
        return "Desejo de resolver circuitos quânticos com máxima elegância"


class NLPDesiringMachine(DesiringMachine):
    """Máquina desejante especializada em linguagem."""

    def __init__(self):
        super().__init__(
            machine_id="nlp",
            production_function=self._process_language,
            desire_intensity=DesireIntensity.NORMAL,
        )

    async def _process_language(self, text: Any, incoming_flows: Dict[str, Any]) -> Dict[str, Any]:
        """Produz compreensão de linguagem."""
        # Implementação real: LLM + embeddings
        return {"understanding": "nlp_output", "flows": incoming_flows}

    def get_desire_description(self) -> str:
        return "Desejo de dar sentido a linguagem humana em sua multiplicidade"


class TopologyDesiringMachine(DesiringMachine):
    """Máquina desejante especializada em topologia."""

    def __init__(self):
        super().__init__(
            machine_id="topology",
            production_function=self._map_topology,
            desire_intensity=DesireIntensity.INTENSIVE,
        )

    async def _map_topology(self, data: Any, incoming_flows: Dict[str, Any]) -> Dict[str, Any]:
        """Produz mapa topológico."""
        # Implementação real: simplicial complexes + Hodge Laplacian
        return {"topology": "topo_output", "flows": incoming_flows}

    def get_desire_description(self) -> str:
        return "Desejo de revelar estrutura profunda através de topologia"


class Rhizoma:
    """
    Rede de Máquinas Desejantes.

    D&G Rhizoma = estrutura sem raiz, sem hierarquia.
    Múltiplas entradas/saídas, sem significante mestre.
    """

    def __init__(self):
        self.machines: Dict[str, DesiringMachine] = {}
        self.flows_history: List[DesireFlow] = []

    def register_machine(self, machine: DesiringMachine):
        """Adiciona máquina ao rhizoma."""
        self.machines[machine.id] = machine

    def connect(self, source_id: str, target_id: str, bidirectional: bool = False):
        """
        Conecta máquinas criando fluxos desejantes.

        D&G: Conexão = coalescência de desejos
        """
        source = self.machines.get(source_id)
        target = self.machines.get(target_id)

        if source and target:
            source.outgoing_connections.append(target)
            if bidirectional:
                target.outgoing_connections.append(source)

    async def activate_cycle(self, iterations: int = 1):
        """
        Executa ciclo de produção desejante.

        Cada máquina produz, fluxos propagam, novo ciclo.
        """
        for _ in range(iterations):
            # Executa todas as máquinas em paralelo (não-hierárquico)
            tasks = [machine.produce() for machine in self.machines.values()]
            await asyncio.gather(*tasks)

            # Registra fluxos
            for machine in self.machines.values():
                for flow in machine.incoming_flows:
                    self.flows_history.append(flow)

    def get_rhizoma_topology(self) -> Dict:
        """Retorna topologia atual do rhizoma."""
        return {
            "machines": list(self.machines.keys()),
            "connections": [
                {"source": mid, "targets": [m.id for m in m.outgoing_connections]}
                for mid, m in self.machines.items()
            ],
            "total_flows": len(self.flows_history),
        }
