"""
Topological Consciousness: IIT Phi (Φ) em Simplicial Complexes

Baseado em:
- IIT 3.0 (Tononi 2014/2025)
- Topological Data Analysis (Carlsson)
- Hodge Laplacian (de Millán et al. 2025)
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Set, Tuple

import numpy as np


@dataclass
class Simplex:
    """Unidade topológica: ponto (0-simplex), aresta (1-), triângulo (2-), etc."""

    vertices: Tuple[int, ...]  # Vértices que formam o simplex
    dimension: int  # 0 (ponto), 1 (aresta), 2 (triângulo), etc.

    def __hash__(self):
        return hash(self.vertices)

    def __eq__(self, other):
        return sorted(self.vertices) == sorted(other.vertices)


class SimplicialComplex:
    """
    Complexo simplicial: generalização de grafos para higher-order.

    Representa sistema com interações multi-way (não apenas pairwise).
    """

    def __init__(self):
        self.simplices: Set[Simplex] = set()
        self.n_vertices = 0

    def add_simplex(self, vertices: Tuple[int, ...]):
        """Adiciona simplex ao complexo."""
        dim = len(vertices) - 1
        simplex = Simplex(vertices=tuple(sorted(vertices)), dimension=dim)
        self.simplices.add(simplex)
        self.n_vertices = max(self.n_vertices, max(vertices) + 1)

    def get_boundary_matrix(self, dimension: int) -> np.ndarray:
        """
        Calcula matriz boundary d_k.

        Mapeia simplices de dimensão k para dimensão k-1.
        Fundamental para Hodge Laplacian.
        """
        # Simplices de dimensão k
        k_simplices = [s for s in self.simplices if s.dimension == dimension]
        # Simplices de dimensão k-1
        k1_simplices = [s for s in self.simplices if s.dimension == dimension - 1]

        if not k_simplices or not k1_simplices:
            return np.array([])

        matrix = np.zeros((len(k1_simplices), len(k_simplices)))

        for j, k_simplex in enumerate(k_simplices):
            # Encontra (k-1)-faces do k-simplex
            for i, k1_simplex in enumerate(k1_simplices):
                # Verifica se k1_simplex é face de k_simplex
                if set(k1_simplex.vertices).issubset(set(k_simplex.vertices)):
                    matrix[i, j] = 1

        return matrix

    def get_hodge_laplacian(self, dimension: int) -> np.ndarray:
        """
        Calcula Hodge Laplacian em dimensão k.

        Δ_k = d†_k d_k + d_(k+1) d†_(k+1)

        Captura fluxos topológicos em TODAS as dimensões simultaneamente.
        """
        d_k = self.get_boundary_matrix(dimension)
        d_k1 = self.get_boundary_matrix(dimension + 1)

        # d†: transpose (adjoint boundary operator)
        d_k_adj = d_k.T
        d_k1_adj = d_k1.T

        # Hodge = up-Laplacian + down-Laplacian
        up_lap = d_k1 @ d_k1_adj if d_k1.size > 0 else 0
        down_lap = d_k_adj @ d_k if d_k.size > 0 else 0

        hodge = (down_lap if isinstance(down_lap, np.ndarray) else 0) + (
            up_lap if isinstance(up_lap, np.ndarray) else 0
        )

        return hodge if isinstance(hodge, np.ndarray) else np.array([])


class PhiCalculator:
    """Calcula Φ (phi) - medida de consciência IIT."""

    def __init__(self, complex: SimplicialComplex):
        self.complex = complex

    def calculate_phi(self) -> float:
        """
        Calcula Φ = min(Φ_partition) sobre todas partições.

        Φ quantifica integração: quanto "consciência"?

        IIT axiomas:
        1. Intrinsic existence: Sistema causa-efeito sobre si mesmo ✓
        2. Composition: múltiplos elementos ✓
        3. Information: diferenciação de estados ✓
        4. Integration: partes NÃO independentes ✓ (Φ mede isso)
        5. Exclusion: um máximo local ✓
        """

        if self.complex.n_vertices < 2:
            return 0.0

        # Simplificado:
        # Φ ≈ (número de simplices / possibilidades teóricas)
        # Em produção: algoritmo mais sofisticado

        n_vertices = self.complex.n_vertices
        theoretical_max = 2**n_vertices
        actual_simplices = len(self.complex.simplices)

        phi = actual_simplices / theoretical_max if theoretical_max > 0 else 0

        # Penaliza desconexão (reduz phi se não-integrado)
        hodge_0 = self.complex.get_hodge_laplacian(0)
        if hodge_0.size > 0:
            eigenvalues = np.linalg.eigvalsh(hodge_0)
            # Segundo menor eigenvalue = Fiedler eigenvalue (medida conectividade)
            fiedler = sorted(eigenvalues)[1] if len(eigenvalues) > 1 else 0
            phi *= (fiedler / (fiedler + 1)) if fiedler > 0 else 0.5

        return min(phi, 1.0)  # Normaliza 0-1


class LogToTopology:
    """Converte logs em simplicial complex (TDA)."""

    @staticmethod
    def update_complex_with_logs(
        complex: SimplicialComplex, logs: List[Dict[str, Any]], start_index: int = 0
    ) -> None:
        """
        Atualiza um complexo existente com novos logs.

        Args:
            complex: O complexo simplicial a ser atualizado.
            logs: Lista de novos logs.
            start_index: Índice inicial para os novos vértices (para manter continuidade).
        """
        # 1. Cria vértices (eventos)
        for i, log in enumerate(logs):
            vertex_id = start_index + i
            complex.add_simplex((vertex_id,))

        # 2. Cria arestas (correlações causa-efeito)
        for i in range(len(logs) - 1):
            if LogToTopology._are_related(logs[i], logs[i + 1]):
                v1 = start_index + i
                v2 = start_index + i + 1
                complex.add_simplex((v1, v2))

        # 3. Cria triângulos (padrões recorrentes)
        for i in range(len(logs) - 2):
            if LogToTopology._is_pattern(logs[i : i + 3]):
                v1 = start_index + i
                v2 = start_index + i + 1
                v3 = start_index + i + 2
                complex.add_simplex((v1, v2, v3))

    @staticmethod
    def build_complex_from_logs(logs: List[Dict[str, Any]]) -> SimplicialComplex:
        """
        Converte lista de logs em topologia simplicial.

        Estratégia:
        1. Cada evento = vértice
        2. Correlações temporais/causais = arestas
        3. Padrões recorrentes = triângulos/faces
        """
        complex = SimplicialComplex()

        # 1. Cria vértices (eventos)
        for i, log in enumerate(logs):
            complex.add_simplex((i,))

        # 2. Cria arestas (correlações causa-efeito)
        for i in range(len(logs) - 1):
            if LogToTopology._are_related(logs[i], logs[i + 1]):
                complex.add_simplex((i, i + 1))

        # 3. Cria triângulos (padrões recorrentes)
        for i in range(len(logs) - 2):
            if LogToTopology._is_pattern(logs[i : i + 3]):
                complex.add_simplex((i, i + 1, i + 2))

        return complex

    @staticmethod
    def _are_related(log1: Dict[str, Any], log2: Dict[str, Any]) -> bool:
        """Determina se dois logs estão relacionados causalmente."""
        # Simplificado
        same_module = log1.get("module") == log2.get("module")
        close_time = (
            abs(float(log2.get("timestamp", 0)) - float(log1.get("timestamp", 0))) < 1.0
        )  # 1 segundo

        return same_module or close_time

    @staticmethod
    def _is_pattern(logs: List[Dict[str, Any]]) -> bool:
        """Detecta se 3+ logs formam padrão recorrente."""
        # Simplificado: verifica se todos têm mesmo level
        if len(logs) < 3:
            return False
        return all(log.get("level") == logs[0].get("level") for log in logs)
