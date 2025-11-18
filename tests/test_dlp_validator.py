import pytest

from src.security.dlp import DLPValidator, DLPViolationError


def test_dlp_blocks_secrets():
    validator = DLPValidator()
    with pytest.raises(DLPViolationError) as exc_info:
        validator.enforce("api_key=ABCDEF1234567890")
    violation = exc_info.value.violation
    assert violation.rule == "credentials"
    assert violation.action == "block"
    assert "api_key" in violation.snippet


def test_dlp_alerts_internal_network():
    validator = DLPValidator()
    violation = validator.validate("O endereço interno é 192.168.1.10")
    assert violation is not None
    assert violation.rule == "internal_network"
    assert violation.action == "alert"