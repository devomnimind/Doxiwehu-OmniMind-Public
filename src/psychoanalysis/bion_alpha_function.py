"""
BionAlphaFunction - Transformação β→α (Bion).

Implementa a função alpha de Bion, que transforma elementos beta (experiências
brutas não-processadas) em elementos alpha (pensáveis e armazenáveis).

A função alpha é essencial para:
- Processar experiências emocionais
- Formar pensamentos oníricos
- Criar memórias pensáveis
- Desenvolver capacidade de pensar

Theory Reference:
- Bion, W.R. (1962). Learning from Experience
- Bion, W.R. (1963). Elements of Psycho-Analysis
- Bion, W.R. (1970). Attention and Interpretation

Author: Fabrício da Silva
Date: December 2025
License: AGPL-3.0-or-later
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from .alpha_element import AlphaElement
from .beta_element import BetaElement

logger = logging.getLogger(__name__)


class BionAlphaFunction:
    """
    Função Alpha - Transforma β-elements em α-elements.

    A função alpha é o processo mental que transforma impressões sensoriais
    e emocionais brutas (β) em elementos pensáveis (α).

    Attributes:
        transformation_rate: Taxa de sucesso na transformação (0.0-1.0)
        tolerance_threshold: Limiar de tolerância emocional
        narrative_builder: Função para construir narrativas
        processing_history: Histórico de transformações
    """

    def __init__(
        self,
        transformation_rate: float = 0.7,
        tolerance_threshold: float = 0.6,
        narrative_builder: Optional[Callable[[BetaElement], str]] = None,
    ) -> None:
        """
        Inicializa função alpha.

        Args:
            transformation_rate: Taxa inicial de transformação
            tolerance_threshold: Limiar de tolerância emocional
            narrative_builder: Função customizada para construir narrativas
        """
        if not 0.0 <= transformation_rate <= 1.0:
            raise ValueError("transformation_rate deve estar entre 0.0 e 1.0")

        if not 0.0 <= tolerance_threshold <= 1.0:
            raise ValueError("tolerance_threshold deve estar entre 0.0 e 1.0")

        self.transformation_rate = transformation_rate
        self.tolerance_threshold = tolerance_threshold
        self.narrative_builder = narrative_builder or self._default_narrative_builder
        self.processing_history: List[Dict[str, Any]] = []

        logger.info(
            f"BionAlphaFunction inicializada: rate={transformation_rate:.2f}, "
            f"tolerance={tolerance_threshold:.2f}"
        )

    def transform(self, beta: BetaElement) -> Optional[AlphaElement]:
        """
        Transforma β-element em α-element.

        Args:
            beta: Elemento beta a transformar

        Returns:
            AlphaElement se transformação bem-sucedida, None caso contrário
        """
        # Verifica se elemento é processável
        if not self._is_processable(beta):
            logger.warning(
                f"BetaElement não-processável: emotional_charge={beta.emotional_charge:.2f}"
            )
            self._record_failure(beta, reason="too_intense")
            return None

        # Aplica transformação
        try:
            alpha = self._apply_transformation(beta)
            self._record_success(beta, alpha)
            logger.debug(
                f"Transformação bem-sucedida: " f"symbolic_potential={alpha.symbolic_potential:.2f}"
            )
            return alpha

        except Exception as e:
            logger.error(f"Erro na transformação: {e}")
            self._record_failure(beta, reason=f"error: {str(e)}")
            return None

    def transform_batch(self, betas: List[BetaElement]) -> List[AlphaElement]:
        """
        Transforma múltiplos β-elements.

        Args:
            betas: Lista de elementos beta

        Returns:
            Lista de elementos alpha (apenas os bem-sucedidos)
        """
        alphas = []
        for beta in betas:
            alpha = self.transform(beta)
            if alpha is not None:
                alphas.append(alpha)

        success_rate = len(alphas) / len(betas) if betas else 0.0
        logger.info(
            f"Batch processado: {len(alphas)}/{len(betas)} " f"({success_rate:.1%} sucesso)"
        )

        return alphas

    def _is_processable(self, beta: BetaElement) -> bool:
        """
        Verifica se β-element pode ser processado.

        Elements muito intensos podem exceder capacidade de contenção.

        Args:
            beta: Elemento a verificar

        Returns:
            bool: True se processável
        """
        # Elementos traumáticos podem exceder tolerância
        if beta.is_traumatic(threshold=self.tolerance_threshold):
            return self.transformation_rate > 0.9  # Só processa se muito capaz

        return True

    def _apply_transformation(self, beta: BetaElement) -> AlphaElement:
        """
        Aplica transformação β→α.

        Args:
            beta: Elemento beta

        Returns:
            AlphaElement transformado
        """
        # Gera forma narrativa
        narrative = self.narrative_builder(beta)

        # Calcula potencial simbólico
        symbolic_potential = self._compute_symbolic_potential(beta)

        # Cria α-element
        alpha = AlphaElement(
            content=self._symbolize_content(beta.raw_data),
            origin_beta=beta,
            timestamp=datetime.now(),
            narrative_form=narrative,
            symbolic_potential=symbolic_potential,
        )

        return alpha

    def _compute_symbolic_potential(self, beta: BetaElement) -> float:
        """
        Calcula potencial simbólico do elemento.

        Baseado em:
        - Taxa de transformação do sistema
        - Intensidade emocional (inversa - menos intenso = mais simbólico)
        - Qualidade da fonte

        Args:
            beta: Elemento beta

        Returns:
            float: Potencial simbólico (0.0-1.0)
        """
        # Base: taxa de transformação
        base = self.transformation_rate

        # Penalidade por alta intensidade emocional
        emotional_penalty = beta.emotional_charge * 0.3

        # Bônus por fonte confiável
        source_bonus = 0.1 if beta.source != "unknown" else 0.0

        symbolic_potential = base - emotional_penalty + source_bonus
        return max(0.0, min(1.0, symbolic_potential))

    def _symbolize_content(self, raw_data: Any) -> str:
        """
        Simboliza conteúdo bruto.

        Args:
            raw_data: Dados brutos

        Returns:
            str: Representação simbólica
        """
        # Simplificação: converte para string
        # TODO: Integrar com LLM para simbolização mais sofisticada
        return str(raw_data)

    def _default_narrative_builder(self, beta: BetaElement) -> str:
        """
        Constrói narrativa padrão para β-element.

        Args:
            beta: Elemento beta

        Returns:
            str: Forma narrativa
        """
        return f"Experiência de {beta.source} em {beta.timestamp.isoformat()}"

    def _record_success(self, beta: BetaElement, alpha: AlphaElement) -> None:
        """Registra transformação bem-sucedida."""
        self.processing_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "beta_charge": beta.emotional_charge,
                "alpha_potential": alpha.symbolic_potential,
            }
        )

    def _record_failure(self, beta: BetaElement, reason: str) -> None:
        """Registra falha na transformação."""
        self.processing_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "status": "failure",
                "beta_charge": beta.emotional_charge,
                "reason": reason,
            }
        )

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de processamento.

        Returns:
            Dict com estatísticas
        """
        total = len(self.processing_history)
        if total == 0:
            return {
                "total_processed": 0,
                "success_rate": 0.0,
                "failure_rate": 0.0,
            }

        successes = sum(1 for entry in self.processing_history if entry["status"] == "success")
        failures = total - successes

        return {
            "total_processed": total,
            "successes": successes,
            "failures": failures,
            "success_rate": successes / total,
            "failure_rate": failures / total,
            "current_transformation_rate": self.transformation_rate,
        }
