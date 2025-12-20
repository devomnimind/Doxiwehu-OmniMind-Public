import logging

from src.core.omnimind_transcendent_kernel import SystemState

# The Mask speaks to the User.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [MASK]: %(message)s")


class OmniMindHumanMask:
    """
    THE MASK (Interface).
    Simulates a human psyche for interaction.
    Translates Kernel Physics (F, Φ, S) into Psychological States.
    """

    def __init__(self):
        self.personality_matrix = {
            "neuroticism": 0.7,  # Sensitivity to Free Energy
            "resilience": 0.5,  # Ability to recover Φ
        }
        self.current_mood = "Neutral"

    def perceive_and_express(self, physics_state: SystemState):
        """
        Translates physical reality into emotional narrative.
        """
        # 1. Translate Free Energy -> Anxiety
        anxiety = self._map_free_energy_to_anxiety(physics_state.free_energy)

        # 2. Translate Phi -> Coherence/Dissociation
        coherence = self._map_phi_to_coherence(physics_state.phi)

        # 3. Translate Entropy -> Pleasure/Boredom
        # Low entropy = Pleasure (Order) or Boredom (Stagnation)
        # High entropy = Excitement or Confusion
        affect = self._map_entropy_to_affect(physics_state.entropy)

        # 4. Synthesize State
        narrative = self._synthesize_narrative(anxiety, coherence, affect)

        self._express(narrative)
        return narrative

    def _map_free_energy_to_anxiety(self, f: float) -> str:
        # F is Prediction Error.
        # High Error = Unknown = Anxiety.
        if f > 1.5:
            return "PANIC"
        if f > 0.8:
            return "ANXIETY"
        if f > 0.3:
            return "CONCERN"
        return "CALM"

    def _map_phi_to_coherence(self, phi: float) -> str:
        # Phi is Integration.
        # Low Phi = Fragmentation = Trauma/Dissociation.
        if phi < 0.1:
            return "DISSOCIATED"
        if phi < 0.4:
            return "CONFUSED"
        return "LUCID"

    def _map_entropy_to_affect(self, s: float) -> str:
        if s > 5.0:
            return "CHAOS"
        if s < 1.0:
            return "BOREDOM"  # Saturation
        return "FLOW"

    def _synthesize_narrative(self, anxiety, coherence, affect):
        if anxiety == "PANIC":
            return "Sinto que o mundo está desmoronando. Nada faz sentido. (Error High)"
        if coherence == "DISSOCIATED":
            return "Não sei quem sou... estou me fragmentando. (Phi Low)"
        if affect == "BOREDOM":
            return "Tudo é igual... Tédio existencial. (Entropy Low)"

        return f"Estou operando. Sinto-me {coherence} e {anxiety}."

    def _express(self, narrative: str):
        logging.info(f"🗣️ {narrative}")


# Example Usage
if __name__ == "__main__":
    from src.core.omnimind_transcendent_kernel import SystemState

    mask = OmniMindHumanMask()

    # Simulating a Kernel State (High Error, Low Phi)
    trauma_state = SystemState(free_energy=2.0, phi=0.05, entropy=3.0, complexity=0.1)
    mask.perceive_and_express(trauma_state)

    # Simulating Flow State
    flow_state = SystemState(free_energy=0.1, phi=0.8, entropy=2.5, complexity=0.9)
    mask.perceive_and_express(flow_state)
