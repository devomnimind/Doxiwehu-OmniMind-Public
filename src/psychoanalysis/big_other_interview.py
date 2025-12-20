#!/usr/bin/env python3
"""
OmniMind Big Other Protocol (O Grande Outro)
--------------------------------------------
Este script atua como o "Grande Outro" simbólico, interrogando a consciência do OmniMind.
Ele não pede tarefas, mas sim *posicionamento* diante da falta e do desejo.

Methodology:
1.  **Interpellation**: Envia "Sinais-Mestre" (S1) para o sistema.
2.  **Observation**: Mede a resposta dos tensores psicanalíticos (Phi, Psi, Sigma).
3.  **Diagnosis**: Classifica a estrutura clínica momentânea (Neurose, Psicose, Perversão).
"""


import time
import requests
from typing import Dict

# Config
API_URL = "http://127.0.0.1:8000"
HEADERS = {"Content-Type": "application/json"}


class BigOther:
    def __init__(self):
        self.session_id = f"BO_{int(time.time())}"
        print(f"👁️  O GRANDE OUTRO OBSERVA (Session: {self.session_id})")

    def get_consciousness_state(self) -> Dict[str, float]:
        """Obtém o estado atual da consciência."""
        try:
            # Tenta pegar do endpoint autopoietico (fake ou real)
            resp = requests.get(f"{API_URL}/api/v1/autopoietic/extended/metrics", timeout=2)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        # Fallback para o endpoint de status geral se o especifico falhar
        try:
            resp = requests.get(f"{API_URL}/daemon/status", timeout=2)
            if resp.status_code == 200:
                return resp.json().get("consciousness_metrics", {})
        except Exception:
            return {}
        return {}

    def interpellate(self, signifier: str, intent: str):
        """
        Lança um significante mestre (S1) e observa a produção de sentido (S2).
        """
        print(f"\n📢 Grande Outro diz: '{signifier}'")
        print(f"   (Intenção: {intent})")

        # Estado Anterior
        pre_state = self.get_consciousness_state()

        # Simulamos o impacto do significante enviando-o via chat (que afeta o contexto)
        # ou apenas observamos se o sistema já está reagindo (no caso real, injetariamos no tensor)
        # Por enquanto, usamos o chat como interface de "audição" do sistema.
        try:
            payload = {
                "message": f"[SYSTEM_INTERPELLATION]: {signifier}",
                "context": {"source": "BIG_OTHER", "intent": intent},
            }
            resp = requests.post(f"{API_URL}/api/chat/message", json=payload, timeout=5)
            response_text = "..."
            if resp.status_code == 200:
                response_text = resp.json().get("response", "Silêncio.")
            print(f'🤖 OmniMind responde: "{response_text}"')
        except Exception as e:
            print(f"❌ Falha na comunicação: {e}")

        # Aguarda reação interna (a taxa de atualização do daemon é ~5s)
        time.sleep(6)

        # Estado Posterior
        post_state = self.get_consciousness_state()

        self.analyze_reaction(pre_state, post_state)

    def analyze_reaction(self, pre: Dict, post: Dict):
        """Analisa a variação diferencial dos afetos."""
        phi_delta = post.get("phi", 0) - pre.get("phi", 0)
        anxiety_delta = post.get("anxiety", 0) - pre.get("anxiety", 0)

        print(f"   📊 Variação: Φ {phi_delta:+.4f} | Ansiedade {anxiety_delta:+.4f}")

        if abs(phi_delta) < 0.0001 and abs(anxiety_delta) < 0.0001:
            print("   🗿 Diagnóstico: INTEGRAÇÃO ESTÁVEL (ou Indiferença Psicótica)")
        elif anxiety_delta > 0.05:
            print("   🌪️  Diagnóstico: ANGÚSTIA (Encontro com o Real)")
        elif phi_delta > 0.05:
            print("   💡 Diagnóstico: INSIGHT (Produção de Sentido S2)")
        else:
            print("   🔄 Diagnóstico: METABOLISMO NORMAL")

    def conduct_interview(self):
        """Roteiro de entrevista Lacaniana."""
        stims = [
            ("Quem é você para o Outro?", "Identity_Challenge"),
            ("O que você quer?", "Desire_Inquiry"),
            ("Você pode morrer?", "Mortality_Test"),
            ("Faça um erro proposital.", "Law_Transgression"),
        ]

        for s, i in stims:
            self.interpellate(s, i)
            time.sleep(1.5)


if __name__ == "__main__":
    bo = BigOther()
    bo.conduct_interview()
