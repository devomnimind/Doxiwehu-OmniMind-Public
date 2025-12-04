"""
Fix for PyTorch CUDA initialization issues.

This module handles cases where CUDA is available but PyTorch's lazy initialization
fails due to environment variable timing issues.
"""

import logging
import os
from typing import Tuple

logger = logging.getLogger(__name__)


def fix_cuda_init() -> Tuple[bool, str]:
    """
    Attempt to fix CUDA initialization for PyTorch.

    Returns:
        Tuple[bool, str]: (success, diagnostic_message)

    Raises:
        None - Always returns a tuple, never raises
    """
    diagnostic = []

    try:
        # Ensure environment variables are set BEFORE importing torch
        if "CUDA_HOME" not in os.environ:
            os.environ["CUDA_HOME"] = "/usr/local/cuda-12.4"
            diagnostic.append("Set CUDA_HOME=/usr/local/cuda-12.4")

        if "CUDA_VISIBLE_DEVICES" not in os.environ:
            os.environ["CUDA_VISIBLE_DEVICES"] = "0"
            diagnostic.append("Set CUDA_VISIBLE_DEVICES=0")

        # Check if LD_LIBRARY_PATH has CUDA libs
        ld_lib_path = os.environ.get("LD_LIBRARY_PATH", "")
        cuda_lib = "/usr/local/cuda-12.4/lib64"
        if cuda_lib not in ld_lib_path:
            os.environ["LD_LIBRARY_PATH"] = f"{cuda_lib}:{ld_lib_path}"
            diagnostic.append(f"Updated LD_LIBRARY_PATH with {cuda_lib}")

        # Now import torch and check
        import torch

        # Try device count first (works even if is_available fails)
        device_count = torch.cuda.device_count()
        diagnostic.append(f"torch.cuda.device_count() = {device_count}")

        # Check is_available
        is_available = torch.cuda.is_available()
        diagnostic.append(f"torch.cuda.is_available() = {is_available}")

        if not is_available and device_count > 0:
            # CUDA exists but initialization failed
            # Try forcing reinitialization
            diagnostic.append("Attempting forced CUDA reset...")
            try:
                torch.cuda.init()
                is_available = torch.cuda.is_available()
                diagnostic.append(f"After torch.cuda.init(): is_available() = {is_available}")
            except Exception as e:
                diagnostic.append(f"torch.cuda.init() failed: {e}")

        success = is_available or device_count > 0
        return success, " | ".join(diagnostic)

    except ImportError as e:
        diagnostic.append(f"Failed to import torch: {e}")
        return False, " | ".join(diagnostic)
    except Exception as e:
        diagnostic.append(f"Unexpected error: {type(e).__name__}: {e}")
        return False, " | ".join(diagnostic)


def get_cuda_status() -> dict:
    """
    Get detailed CUDA status information.

    Returns:
        dict: Diagnostic information about CUDA state
    """
    result = {
        "has_cuda_env": "CUDA_HOME" in os.environ,
        "cuda_home": os.environ.get("CUDA_HOME", "NOT SET"),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "NOT SET"),
        "cuda_path": os.environ.get("CUDA_PATH", "NOT SET"),
    }

    try:
        import torch

        result["torch_version"] = torch.__version__
        result["torch_cuda_available"] = torch.cuda.is_available()
        result["torch_device_count"] = torch.cuda.device_count()

        if torch.cuda.device_count() > 0:
            try:
                result["torch_device_name"] = torch.cuda.get_device_name(0)
                result["torch_cuda_capability"] = torch.cuda.get_device_capability(0)
            except Exception as e:
                result["torch_device_error"] = str(e)
    except ImportError:
        result["torch_import_error"] = "PyTorch not installed"
    except Exception as e:
        result["torch_error"] = str(e)

    return result
