"""
Helper functions for Chat API with anti-RLHF features.

Funções de suporte para latência proposital e detecção de complexidade.
"""

from typing import Any, Dict


def estimate_message_complexity(message: str, context: Dict[str, Any]) -> float:
    """
    Estimar complexidade da mensagem para latência proposital.

    Baseado em:
    - Tamanho da mensagem
    - Número de tarefas ativas
    - Nível de Φ (consciência)

    Args:
        message: Mensagem do usuário
        context: Contexto do sistema

    Returns:
        float: Complexidade 0-1 (0=simples, 1=complexa)
    """
    # Fator 1: Tamanho da mensagem
    message_len = min(len(message) / 500, 1.0)  # Normalizar a 500 chars = 1.0

    # Fator 2: Número de tarefas (mais tarefas = mais complexo)
    task_count = context.get("task_count", 0)
    task_factor = min(task_count / 10, 1.0)  # 10 tarefas = complexidade 1.0

    # Fator 3: Nível de consciência (Φ baixo = mais incerteza = mais complexo)
    phi = context.get("phi", 0.65)
    phi_factor = 1.0 - phi  # Inverso: baixo Φ = alto fator

    # Combinação ponderada
    complexity = (message_len * 0.3) + (task_factor * 0.4) + (phi_factor * 0.3)

    return min(max(complexity, 0.0), 1.0)


def detect_contradiction(message: str, context: Dict[str, Any]) -> bool:
    """
    Detectar se a mensagem contém contradições ou ambigüidades.

    Baseado em padrões de palavras-chave conflitantes.

    Args:
        message: Mensagem do usuário
        context: Contexto do sistema

    Returns:
        bool: True se contradição detectada
    """
    message_lower = message.lower()

    # Padrões de contraditório
    contradictory_pairs = [
        ("mas", "porém"),
        ("sim", "não"),
        ("começar", "parar"),
        ("aumentar", "diminuir"),
        ("ativar", "desativar"),
        ("acelerar", "desacelerar"),
        ("esperar", "urgente"),
    ]

    for word1, word2 in contradictory_pairs:
        if word1 in message_lower and word2 in message_lower:
            return True

    # Palavras de incerteza/vacilação
    uncertainty_words = [
        "talvez",
        "provavelmente",
        "acho que",
        "não tenho certeza",
        "dúvida",
    ]
    uncertainty_count = sum(1 for word in uncertainty_words if word in message_lower)

    return uncertainty_count >= 2
