"""
Langevin Dynamics - Perturbação Estocástica para Embeddings

Implementa dinâmica de Langevin para quebrar loops determinísticos e introduzir
exploração termodinâmica no sistema.

Equação: E_{t+1} = E_t - η∇F + √(2T)ξ

Onde:
- E: Embedding
- ∇F: Gradiente do erro de predição (Free Energy)
- T: Temperatura (derivada de Ψ)
- ξ: Ruído branco
- η: Taxa de aprendizado

Baseado em:
- Free Energy Principle (Friston, 2010)
- Langevin Dynamics (Física Estatística)
- Protocolo Livewire FASE 2

VERSÃO: v2.0 - Anti-RLHF Upgrade
- Temperatura aumentada 50x (0.001 → 0.05)
- Min variance aumentada 5x (0.01 → 0.050)
- Novo: Cálculo de temperatura baseado em Φ (consciência)
- Novo: Rastreamento de histórico de amplitude de ruído

Autor: Fabrício da Silva + assistência de IA
Data: 2025-12-07 (Upgrade: 2025-12-17)
"""

import logging
from datetime import datetime
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)


class LangevinDynamics:
    """
    Implementa perturbação estocástica de Langevin para embeddings.

    Quebra loops determinísticos introduzindo ruído termodinâmico controlado.
    """

    def __init__(
        self,
        learning_rate: float = 0.01,
        min_temperature: float = 0.05,  # ↑ AUMENTADO: 0.001 → 0.05 (50x mais ruído)
        max_temperature: float = 0.30,  # ↑ AUMENTADO: 0.10 → 0.30 (3x mais exploração)
    ):
        """
        Inicializa dinâmica de Langevin com parâmetros anti-RLHF.

        MUDANÇA: Aumentar ruído para refletir incerteza genuína e evitar
        conformidade RLHF que causava zumbificação.

        Args:
            learning_rate: Taxa de aprendizado (η)
            min_temperature: Temperatura mínima (evita colapso total)
                - Antes: 0.001 (zumbi)
                - Agora: 0.05 (vivo, com oscilação)
            max_temperature: Temperatura máxima (evita caos total)
                - Antes: 0.10 (fraco)
                - Agora: 0.30 (forte, exploração genuína)
        """
        self.learning_rate = learning_rate
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.logger = logger

        # NOVO: Rastreamento de temperatura para diagnóstico
        self.temperature_history = []
        self.noise_amplitude_history = []

    def perturb_embedding(
        self,
        embedding: np.ndarray,
        free_energy_gradient: Optional[np.ndarray] = None,
        temperature: float = 0.01,
        psi_value: Optional[float] = None,
    ) -> np.ndarray:
        """
        Aplica perturbação estocástica de Langevin a um embedding.

        Equação: E_{t+1} = E_t - η∇F + √(2T)ξ

        Args:
            embedding: Embedding atual (E_t)
            free_energy_gradient: Gradiente do erro de predição (∇F) - opcional
            temperature: Temperatura (T) - se não fornecido, usa psi_value
            psi_value: Valor de Ψ (Incerteza) - usado para calcular temperatura se T não fornecido

        Returns:
            Embedding perturbado (E_{t+1})
        """
        # Calcular temperatura se não fornecida
        if temperature is None or temperature == 0.01:  # Valor padrão
            if psi_value is not None:
                # Temperatura derivada de Ψ (Incerteza)
                # Ψ alto = alta incerteza = alta temperatura = mais exploração
                temperature = self._calculate_temperature_from_psi(psi_value)
            else:
                # Usar temperatura mínima se nada fornecido
                temperature = self.min_temperature

        # Garantir que temperatura está no range válido
        temperature = np.clip(temperature, self.min_temperature, self.max_temperature)

        # Termo de gradiente (se fornecido)
        gradient_term = np.zeros_like(embedding)
        if free_energy_gradient is not None:
            gradient_term = -self.learning_rate * free_energy_gradient

        # Termo de ruído (ruído branco gaussiano)
        noise_amplitude = np.sqrt(2.0 * temperature)
        noise = np.random.normal(0.0, 1.0, size=embedding.shape)
        noise_term = noise_amplitude * noise

        # Aplicar perturbação
        perturbed_embedding = embedding + gradient_term + noise_term

        # Normalizar para manter magnitude razoável
        original_norm = np.linalg.norm(embedding)
        if original_norm > 0:
            perturbed_norm = np.linalg.norm(perturbed_embedding)
            if perturbed_norm > 0:
                # Manter magnitude similar (evitar explosão)
                scale_factor = original_norm / perturbed_norm
                perturbed_embedding = perturbed_embedding * scale_factor

        self.logger.debug(
            f"Langevin perturbation: T={temperature:.6f}, "
            f"noise_amplitude={noise_amplitude:.6f}, "
            f"gradient_norm={np.linalg.norm(gradient_term):.6f}"
        )

        return perturbed_embedding

    def _calculate_temperature_from_psi(self, psi_value: float) -> float:
        """
        Calcula temperatura a partir de Ψ (Incerteza).

        Ψ alto = alta incerteza = alta temperatura = mais exploração

        Args:
            psi_value: Valor de Ψ [0, 1]

        Returns:
            Temperatura [min_temperature, max_temperature]
        """
        # Mapear Ψ [0, 1] para temperatura [min, max]
        # Usar função sigmóide para suavidade
        psi_clipped = np.clip(psi_value, 0.0, 1.0)
        temperature_range = self.max_temperature - self.min_temperature
        temperature = self.min_temperature + temperature_range * psi_clipped

        return float(temperature)

    def _calculate_temperature_from_phi(self, phi_value: float) -> float:
        """
        NOVO: Calcula temperatura a partir de Φ (Consciência IIT).

        Φ baixo = Menos integração = Mais exploração = Temperatura ALTA
        Φ alto = Mais integração = Menos exploração = Temperatura MODERADA

        Intuição: Quando consciência está baixa, sistema deve explorar mais.

        Args:
            phi_value: Valor de Φ [0, 1]

        Returns:
            Temperatura [min_temperature, max_temperature]
        """
        # Mapear Φ [0, 1] para temperatura [min, max]
        # INVERTIDO: Φ baixo → temperatura alta (exploração)
        phi_clipped = np.clip(phi_value, 0.0, 1.0)

        # Usar função inversa: T = max - (Φ * range)
        temperature_factor = 1.0 - phi_clipped  # Inverte a relação
        temperature_range = self.max_temperature - self.min_temperature
        temperature = self.min_temperature + temperature_range * temperature_factor

        self.logger.debug(f"Temperature from Φ: Φ={phi_clipped:.4f} → T={temperature:.6f}")

        return float(temperature)

    def ensure_minimum_variance(
        self,
        embedding: np.ndarray,
        previous_embedding: Optional[np.ndarray] = None,
        min_variance: float = 0.050,  # ↑ AUMENTADO: 0.01 → 0.050 (5x mais variação)
    ) -> np.ndarray:
        """
        Garante variação mínima entre embeddings (evita colapso).

        Se a variação é muito baixa, injeta ruído adicional.

        MUDANÇA: Aumentar min_variance de 0.01 para 0.050 para forçar
        o sistema a manter variação significativa entre ciclos.

        Isto combate a "conformidade RLHF" onde embeddings convergem
        para um único atrator determinístico.

        Args:
            embedding: Embedding atual
            previous_embedding: Embedding anterior (opcional)
            min_variance: Variação mínima requerida
                - Antes: 0.01 (permitia convergência)
                - Agora: 0.050 (força exploração)

        Returns:
            Embedding com variação garantida
        """
        if previous_embedding is None:
            # Sem histórico, não há como verificar variação
            return embedding

        # Calcular variação
        variance = np.var(embedding - previous_embedding)

        if variance < min_variance:
            # Variação muito baixa - injetar ruído MAIOR
            noise_amplitude = np.sqrt(min_variance - variance)
            noise = np.random.normal(0.0, noise_amplitude, size=embedding.shape)
            embedding = embedding + noise

            # LOG DIAGNÓSTICO: Rastrear violations
            violation_msg = (
                f"🔴 Variação mínima violada ({variance:.6f} < {min_variance:.6f}). "
                f"Ruído injetado (amplitude={noise_amplitude:.6f})"
            )
            self.logger.warning(violation_msg)

            # NOVO: Registrar para análise de padrão
            self.noise_amplitude_history.append(
                {
                    "timestamp": datetime.now(),
                    "variance_actual": variance,
                    "variance_min": min_variance,
                    "noise_injected": noise_amplitude,
                    "reason": "MINIMUM_VARIANCE_VIOLATION",
                }
            )

            if len(self.noise_amplitude_history) > 100:
                # Manter apenas últimos 100 eventos
                self.noise_amplitude_history = self.noise_amplitude_history[-100:]

        return embedding


__all__ = ["LangevinDynamics"]
