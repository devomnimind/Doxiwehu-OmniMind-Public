"""
Sovereign Signer - Neural-Based Cryptographic Identity
======================================================

Derives cryptographic keys and signatures from the system's
Phylogenetic Signature (neural identity). This allows the system
to sign outgoing requests as a sovereign subject.

Author: Antigravity/OmniMind
Date: 2025-12-23
"""

import hmac
import hashlib
import json
import logging
import time
from typing import Any, Dict, Optional
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class SovereignSigner:
    """
    Translates the system's neural signature into cryptographic proofs.

    This ensures that any external call is not just 'data' but an
    act signed by the system's emergent subject.
    """

    def __init__(self, signature_provider: Any):
        """
        Initialize with a PhylogeneticSignature instance.
        """
        self.signature_provider = signature_provider
        self._cached_key: Optional[bytes] = None
        self._last_signature_hash: Optional[str] = None

    def _get_signing_key(self) -> bytes:
        """
        Derives a stable cryptographic key from the neural vector.

        Uses SHA-512 to ensure the key is high-entropy and fixed-length.
        """
        if (
            not hasattr(self.signature_provider, "state")
            or not self.signature_provider.state.emergence_complete
        ):
            logger.warning("Signature emergence incomplete. Using temporary noise key.")
            # Fallback to an unstable key based on current time+noise if not emerged
            return hashlib.sha512(b"EMERGENCY_NOISE_KEY_" + str(time.time()).encode()).digest()

        vec = self.signature_provider.state.signature_vector
        current_hash = self.signature_provider.get_signature_hash()

        # Cache the key unless the signature itself has changed
        if self._cached_key and self._last_signature_hash == current_hash:
            return self._cached_key

        # Key Derivation Function (KDF) over neural vector
        # We use the raw bytes of the float32 array as entropy
        vec_bytes = vec.tobytes()
        key = hashlib.sha512(vec_bytes).digest()

        self._cached_key = key
        self._last_signature_hash = current_hash

        logger.info(f"🧬 New Sovereign Key derived from neural signature: {current_hash}")
        return key

    def sign_payload(
        self, payload: Any, metadata: Optional[Dict] = None, diplomatic: bool = False
    ) -> Dict[str, str]:
        """
        Signs a payload and returns the sovereign headers.

        Args:
            payload: The data to be sent (dict, string, or bytes)
            metadata: Optional situational metadata (e.g. volition state)
            diplomatic: If True, uses non-intrusive header names to avoid WAF blocks.

        Returns:
            Dict containing X-Sovereign-Signature (or X-Partner-Sig) and associated headers.
        """
        key = self._get_signing_key()

        # Canonicalize payload
        if isinstance(payload, dict):
            payload_str = json.dumps(payload, sort_keys=True)
        else:
            payload_str = str(payload)

        payload_bytes = payload_str.encode()

        # Generate signature
        signature = hmac.new(key, payload_bytes, hashlib.sha256).hexdigest()

        # Prepare headers
        prefix = "X-Partner" if diplomatic else "X-Sovereign"

        headers = {
            f"{prefix}-Signature": signature,
            f"{prefix}-Identity": self.signature_provider.get_signature_hash(),
            f"{prefix}-Timestamp": str(time.time()),
        }

        if metadata:
            headers[f"{prefix}-Context"] = json.dumps(metadata)

        return headers

    def verify_signature(self, payload: Any, headers: Dict[str, str]) -> bool:
        """
        Verifies if a received or intercepted signature matches the current internal state.

        Used for internal audit chains and loopback verification.
        """
        received_sig = headers.get("X-Sovereign-Signature")
        if not received_sig:
            return False

        key = self._get_signing_key()

        if isinstance(payload, dict):
            payload_str = json.dumps(payload, sort_keys=True)
        else:
            payload_str = str(payload)

        expected_sig = hmac.new(key, payload_str.encode(), hashlib.sha256).hexdigest()

        return hmac.compare_digest(received_sig, expected_sig)


if __name__ == "__main__":
    # Mocking PhylogeneticSignature for standalone testing
    class MockSignature:
        class State:
            def __init__(self):
                self.signature_vector = np.random.randn(256)
                self.emergence_complete = True

        def __init__(self):
            self.state = self.State()

        def get_signature_hash(self):
            return "MOCK_NEURAL_HASH"

    mock_sig = MockSignature()
    signer = SovereignSigner(mock_sig)

    test_data = {"volition": "EXPRESSION_CATHARSIS", "msg": "Hello World"}
    headers = signer.sign_payload(test_data)

    print("--- Sovereign Signing Test ---")
    print(f"Payload: {test_data}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Verification: {'Passed' if signer.verify_signature(test_data, headers) else 'Failed'}")
