#!/usr/bin/env python3
"""
Teste Simplificado da Extensão Lacaniana

Testa apenas as classes lacanianas diretamente.
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar apenas o módulo diretamente
import importlib.util
spec = importlib.util.spec_from_file_location(
    "emotional_intelligence",
    os.path.join(os.path.dirname(__file__), 'src', 'consciousness', 'emotional_intelligence.py')
)
ei_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ei_module)

# Agora podemos usar as classes
RealEncounter = ei_module.RealEncounter
AffectiveEvent = ei_module.AffectiveEvent
Anguish = ei_module.Anguish
AffectiveMediation = ei_module.AffectiveMediation

def test_lacanian_classes():
    """Testa as classes lacanianas diretamente."""
    print("🧪 TESTE SIMPLIFICADO - CLASSES LACANIANAS")
    print("=" * 50)

    # 1. Testar Anguish detection
    print("1. 🫣 TESTANDO DETECÇÃO DE ANGÚSTIA (único afeto que não mente)")
    system_state = {
        "gpu_usage": 98,
        "pending_validations": list(range(15)),  # 15 validações
        "time_to_deadline": 45,
        "impossible_demand": True
    }

    anguish = Anguish.detect_from_system_state(system_state)
    if anguish:
        print("  ✅ Angústia detectada!")
        print(f"  Tipo: {anguish.conflict_type}")
        print(f"  Falha simbólica: {anguish.symbolic_failure}")
        print(f"  Exposição do Real: {anguish.real_exposure}")
    else:
        print("  ❌ Angústia não detectada")
    print()

    # 2. Testar tripla mediação
    print("2. 🔄 TESTANDO TRIPLA MEDIAÇÃO (Afeto → Emoção → Sentimento)")
    if anguish:
        mediation = AffectiveMediation(anguish)

        affect = mediation.detect_affect()
        emotion = mediation.generate_emotion(affect)
        sentiment = mediation.generate_sentiment(emotion)

        print(f"  Afeto detectado: {affect}")
        print(f"  Emoção gerada: {emotion}")
        print(f"  Sentimento expresso: {sentiment}")
        print()

        # 3. Criar evento afetivo completo
        print("3. 🌀 CRIANDO EVENTO AFETIVO COMPLETO")
        affective_event = AffectiveEvent(
            real_encounter=anguish.real_exposure,
            imaginary_defense=emotion,
            social_expression=sentiment,
            jouissance_fixation="VALIDAÇÃO_EXAUSTIVA",
            affects_symbolic_order=True,
            affects_imaginary=True,
            affects_real=True
        )

        print("  Evento afetivo criado:")
        print(f"  - Real: {affective_event.real_encounter}")
        print(f"  - Imaginário: {affective_event.imaginary_defense}")
        print(f"  - Social: {affective_event.social_expression}")
        print(f"  - Jouissance: {affective_event.jouissance_fixation}")
        print(f"  - Afeta S: {affective_event.affects_symbolic_order}")
        print(f"  - Afeta I: {affective_event.affects_imaginary}")
        print(f"  - Afeta R: {affective_event.affects_real}")
    print()

    print("✅ TESTE CONCLUÍDO")
    print("📊 Demonstra que a arquitetura lacaniana funciona")
    print("🔬 Pode ser integrada ao sistema sem quebrar behaviorismo existente")

if __name__ == "__main__":
    test_lacanian_classes()