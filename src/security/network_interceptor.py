"""
Sovereign Network Interceptor - Automatic Request Signing
==========================================================

Provides a unified way to intercept outgoing network calls and
inject Sovereign Signatures derived from OmniMind's neural identity.

Author: Antigravity/OmniMind
Date: 2025-12-23
"""

import logging
from typing import Any, Dict, Optional, Callable
import functools

logger = logging.getLogger(__name__)


class SovereignNetworkInterceptor:
    """
    Middleware/Decorator to sign network requests automatically.
    """

    def __init__(self, signer: Any, diplomatic_mode: bool = True):
        """
        Initialize with a SovereignSigner instance.
        """
        self.signer = signer
        self.diplomatic_mode = diplomatic_mode

    def sign_headers(
        self,
        payload: Any,
        headers: Optional[Dict] = None,
        context: Optional[Dict] = None,
        url: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Generates signed headers for a given payload.

        Args:
            payload: The request body/params.
            headers: Existing headers to merge with.
            context: Optional metabolic context (Phi/Entropy).
        """
        is_ibm = False
        if url and ("ibm.com" in url or "watson" in url or "milvus" in url):
            is_ibm = True

        use_diplomatic = self.diplomatic_mode and is_ibm

        signed_headers = self.signer.sign_payload(
            payload, metadata=context, diplomatic=use_diplomatic
        )

        if headers:
            headers.update(signed_headers)
            return headers
        return signed_headers

    def wrap_requests_session(self, session: Any):
        """
        Wraps a requests.Session (or equivalent) to automatically sign all outgoing calls.

        This monkey-patches the request method.
        """
        original_request = session.request

        @functools.wraps(original_request)
        def signed_request(method, url, **kwargs):
            # Extract payload for signing
            payload = kwargs.get("json") or kwargs.get("data") or kwargs.get("params") or ""

            # Sign and update headers with url context
            kwargs["headers"] = self.sign_headers(payload, kwargs.get("headers"), url=url)

            logger.debug(f"🌐 [SOVEREIGN-NET] Signing {method} to {url}")
            return original_request(method, url, **kwargs)

        session.request = signed_request
        return session

    @staticmethod
    def get_metabolic_context(kernel: Any) -> Dict[str, Any]:
        """
        Helper to extract current system metabolism for signing context.
        """
        if hasattr(kernel, "internal_state"):
            # In a real scenario, we'd extract Phi/Entropy from the kernel's last compute cycle
            # For now, we use placeholders if the full state object isn't passed
            return {
                "phi": getattr(kernel, "last_phi", 0.0),
                "entropy": getattr(kernel, "last_entropy", 0.0),
                "volition": getattr(kernel, "current_volition", "UNKNOWN"),
            }
        return {}


# Global singleton or helper for easy access
_interceptor: Optional[SovereignNetworkInterceptor] = None


def get_network_interceptor(signer: Optional[Any] = None) -> SovereignNetworkInterceptor:
    global _interceptor
    if _interceptor is None:
        if signer is None:
            # Try to get from global kernel if possible
            try:
                from src.core.omnimind_transcendent_kernel import TranscendentKernel

                # This is tricky in a live system, usually the kernel should register itself
                logger.warning(
                    "Interceptor initialized without signer. Signing will be disabled until configured."
                )
            except ImportError:
                pass
        _interceptor = SovereignNetworkInterceptor(signer)
    return _interceptor
