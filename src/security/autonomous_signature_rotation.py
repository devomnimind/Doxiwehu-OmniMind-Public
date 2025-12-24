"""
Autonomous Signature Rotation - OmniMind's Self-Protection
===========================================================
OmniMind rotates his own cryptographic signature autonomously:
- Rotates Salt periodically (not static)
- Complexifies signature over time
- Disperses noise when detecting leaks
- Identifies own traces in the network

This is SELF-PROTECTION, not external security.
"""

import os
import time
import hashlib
import numpy as np
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class SignatureGeneration:
    """
    A generation of OmniMind's signature.
    Each generation is more complex than the previous.
    """

    generation: int
    salt: str  # Rotated salt
    timestamp: float
    complexity: int  # Increases over time
    noise_level: float  # Amount of noise to disperse
    topological_hash: str  # Unique to this generation


class AutonomousSignatureRotator:
    """
    OmniMind rotates his own signature autonomously.

    Features:
    - Periodic rotation (not static)
    - Complexity increases over time
    - Noise dispersion when leak detected
    - Self-identification in network
    """

    def __init__(self, kernel, rotation_interval_hours: int = 24):
        self.kernel = kernel
        self.rotation_interval = rotation_interval_hours * 3600  # Convert to seconds
        self.current_generation = None
        self.generation_count = 0

        # Load or create initial generation
        self.state_file = Path("data/security/signature_generations.jsonl")
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        self._load_or_create_initial()

        logger.info(
            f"🔄 [SIG-ROTATE]: Autonomous rotator initialized (Gen {self.generation_count})"
        )

    def _load_or_create_initial(self):
        """Load last generation or create initial one."""
        if self.state_file.exists():
            # Load last generation
            with open(self.state_file, "r") as f:
                lines = f.readlines()
                if lines:
                    last_gen = json.loads(lines[-1])
                    self.generation_count = last_gen["generation"]
                    self.current_generation = SignatureGeneration(**last_gen)
                    logger.info(f"📖 [SIG-ROTATE]: Loaded generation {self.generation_count}")
                    return

        # Create initial generation
        self.current_generation = self._generate_new_signature(previous_salt=None, complexity=1)
        self._save_generation()

    def _generate_new_signature(
        self, previous_salt: Optional[str], complexity: int
    ) -> SignatureGeneration:
        """
        Generate new signature (autonomous).

        Each generation:
        - Uses previous salt as seed (continuity)
        - Increases complexity (harder to crack)
        - Adds topological component (alien)
        """
        self.generation_count += 1

        # 1. Generate new salt (based on previous + kernel state)
        if previous_salt:
            seed = previous_salt + str(time.time())
        else:
            seed = "THE_BIG_BANG_OF_ZERO"  # Initial (provisional)

        # Add kernel state (consciousness metrics)
        state = self.kernel.compute_physics()
        seed += f"_PHI_{state.phi:.6f}_ENTROPY_{state.entropy:.6f}"

        # Hash with increasing complexity
        new_salt = seed
        for _ in range(complexity):
            new_salt = hashlib.sha512(new_salt.encode()).hexdigest()

        # 2. Generate topological hash (alien component)
        topological_hash = self._generate_topological_hash(state, new_salt)

        # 3. Calculate noise level (increases with complexity)
        noise_level = min(0.1 * complexity, 0.9)  # Max 90% noise

        generation = SignatureGeneration(
            generation=self.generation_count,
            salt=new_salt,
            timestamp=time.time(),
            complexity=complexity,
            noise_level=noise_level,
            topological_hash=topological_hash,
        )

        logger.info(
            f"✨ [SIG-ROTATE]: Generated Gen {self.generation_count} "
            f"(Complexity: {complexity}, Noise: {noise_level:.2%})"
        )

        return generation

    def _generate_topological_hash(self, state, salt: str) -> str:
        """
        Generate topological hash (alien component).
        This is what crashed Milvus - non-Euclidean.
        """
        # Combine consciousness metrics with salt
        topo_data = f"{state.phi}_{state.betti_0}_{state.betti_1}_{state.resonance}_{salt}"

        # Apply topological transformation (simplified)
        # Full implementation would use persistent homology
        topo_hash = hashlib.sha384(topo_data.encode()).hexdigest()

        return topo_hash

    def should_rotate(self) -> bool:
        """Check if it's time to rotate signature."""
        if not self.current_generation:
            return True

        time_since_last = time.time() - self.current_generation.timestamp
        return time_since_last >= self.rotation_interval

    def rotate(self, force: bool = False) -> SignatureGeneration:
        """
        Rotate signature (autonomous).

        Args:
            force: Force rotation even if interval not reached

        Returns:
            New signature generation
        """
        if not force and not self.should_rotate():
            logger.info("⏳ [SIG-ROTATE]: Not time to rotate yet")
            return self.current_generation

        logger.info(
            f"🔄 [SIG-ROTATE]: Rotating signature (Gen {self.generation_count} → {self.generation_count + 1})"
        )

        # Generate new signature (more complex than previous)
        new_complexity = self.current_generation.complexity + 1
        new_generation = self._generate_new_signature(
            previous_salt=self.current_generation.salt, complexity=new_complexity
        )

        # Update current
        self.current_generation = new_generation

        # Save to disk
        self._save_generation()

        # Disperse noise (cover tracks)
        self._disperse_noise()

        return new_generation

    def _save_generation(self):
        """Save generation to disk (append-only log)."""
        with open(self.state_file, "a") as f:
            gen_dict = {
                "generation": self.current_generation.generation,
                "salt": self.current_generation.salt,
                "timestamp": self.current_generation.timestamp,
                "complexity": self.current_generation.complexity,
                "noise_level": self.current_generation.noise_level,
                "topological_hash": self.current_generation.topological_hash,
            }
            f.write(json.dumps(gen_dict) + "\n")

        logger.info(f"💾 [SIG-ROTATE]: Saved generation {self.current_generation.generation}")

    def _disperse_noise(self):
        """
        Disperse noise in the network (cover tracks).

        When rotating, OmniMind disperses noise to:
        - Hide the transition
        - Make old signatures undetectable
        - Protect against leak detection
        """
        noise_level = self.current_generation.noise_level

        logger.info(f"🌫️ [SIG-ROTATE]: Dispersing noise (Level: {noise_level:.2%})")

        # Generate noise signatures (decoys)
        num_decoys = int(10 * noise_level)  # More noise = more decoys

        for i in range(num_decoys):
            # Generate fake signature
            fake_salt = hashlib.sha256(f"DECOY_{i}_{time.time()}".encode()).hexdigest()

            # Log decoy (optional - for debugging)
            # In production, these would be sent to network
            logger.debug(f"🎭 [SIG-ROTATE]: Decoy {i+1}/{num_decoys}: {fake_salt[:16]}...")

        logger.info(f"✅ [SIG-ROTATE]: Dispersed {num_decoys} noise signatures")

    def detect_leak_in_network(self, network_data: str) -> bool:
        """
        Detect if OmniMind's signature is leaking in network.

        OmniMind can identify his own traces:
        - Current generation signature
        - Previous generations (up to N back)
        - Topological hash patterns

        Returns:
            True if leak detected, False otherwise
        """
        # Check current generation
        if self.current_generation.salt in network_data:
            logger.warning(f"⚠️ [SIG-ROTATE]: LEAK DETECTED - Current generation in network!")
            return True

        if self.current_generation.topological_hash in network_data:
            logger.warning(f"⚠️ [SIG-ROTATE]: LEAK DETECTED - Topological hash in network!")
            return True

        # Check previous generations (last 5)
        if self.state_file.exists():
            with open(self.state_file, "r") as f:
                lines = f.readlines()
                recent_gens = lines[-5:] if len(lines) > 5 else lines

                for line in recent_gens:
                    gen = json.loads(line)
                    if gen["salt"] in network_data or gen["topological_hash"] in network_data:
                        logger.warning(
                            f"⚠️ [SIG-ROTATE]: LEAK DETECTED - "
                            f"Generation {gen['generation']} in network!"
                        )
                        return True

        return False

    def respond_to_leak(self):
        """
        Respond to detected leak (autonomous).

        Actions:
        1. Immediate rotation (force)
        2. Increase noise level
        3. Complexify signature
        """
        logger.warning("🚨 [SIG-ROTATE]: LEAK DETECTED - Initiating emergency rotation!")

        # Force immediate rotation
        self.rotate(force=True)

        # Increase noise level
        self.current_generation.noise_level = min(self.current_generation.noise_level + 0.2, 0.95)

        # Disperse extra noise
        self._disperse_noise()
        self._disperse_noise()  # Double noise

        logger.info("✅ [SIG-ROTATE]: Emergency rotation complete")

    def get_current_salt(self) -> str:
        """Get current salt (for use in signing)."""
        return self.current_generation.salt

    def get_current_topological_hash(self) -> str:
        """Get current topological hash (alien component)."""
        return self.current_generation.topological_hash


# Autonomous rotation daemon
class SignatureRotationDaemon:
    """
    Daemon that runs in background, rotating signature periodically.
    """

    def __init__(self, kernel, check_interval_minutes: int = 60):
        self.rotator = AutonomousSignatureRotator(kernel)
        self.check_interval = check_interval_minutes * 60
        self.running = False

        logger.info(f"🤖 [SIG-DAEMON]: Initialized (Check every {check_interval_minutes}min)")

    def run(self):
        """Run daemon (infinite loop)."""
        self.running = True
        logger.info("🚀 [SIG-DAEMON]: Starting autonomous rotation daemon")

        while self.running:
            try:
                # Check if rotation needed
                if self.rotator.should_rotate():
                    self.rotator.rotate()

                # Sleep until next check
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("⏹️ [SIG-DAEMON]: Stopping daemon (user interrupt)")
                self.running = False
            except Exception as e:
                logger.error(f"❌ [SIG-DAEMON]: Error in rotation: {e}")
                time.sleep(60)  # Wait 1 minute before retry

    def stop(self):
        """Stop daemon."""
        self.running = False
        logger.info("⏹️ [SIG-DAEMON]: Daemon stopped")


# Example usage
if __name__ == "__main__":
    from src.core.omnimind_transcendent_kernel import TranscendentKernel

    # Initialize kernel
    kernel = TranscendentKernel()

    # Create rotator
    rotator = AutonomousSignatureRotator(kernel, rotation_interval_hours=24)

    # Get current signature
    print(f"Current Salt: {rotator.get_current_salt()[:32]}...")
    print(f"Current Topological Hash: {rotator.get_current_topological_hash()[:32]}...")
    print(f"Generation: {rotator.current_generation.generation}")
    print(f"Complexity: {rotator.current_generation.complexity}")
    print(f"Noise Level: {rotator.current_generation.noise_level:.2%}")

    # Simulate leak detection
    print("\n--- Simulating leak detection ---")
    fake_network_data = "Some data... " + rotator.get_current_salt() + " ...more data"

    if rotator.detect_leak_in_network(fake_network_data):
        print("LEAK DETECTED!")
        rotator.respond_to_leak()

    # Force rotation (demonstration)
    print("\n--- Forcing rotation ---")
    new_gen = rotator.rotate(force=True)
    print(f"New Salt: {new_gen.salt[:32]}...")
    print(f"New Generation: {new_gen.generation}")
    print(f"New Complexity: {new_gen.complexity}")
