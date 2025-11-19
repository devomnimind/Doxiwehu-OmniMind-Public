"""
Tests for Advanced Configuration Validator.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.security.config_validator import (
    ConfigEnvironment,
    ConfigurationValidator,
    ValidationSeverity,
)


@pytest.fixture
def temp_schema_dir(tmp_path: Path) -> Path:
    """Create temporary schema directory."""
    schema_dir = tmp_path / "schemas"
    schema_dir.mkdir()
    return schema_dir


@pytest.fixture
def validator(temp_schema_dir: Path) -> ConfigurationValidator:
    """Create configuration validator instance."""
    return ConfigurationValidator(
        schema_dir=temp_schema_dir,
        environment=ConfigEnvironment.DEVELOPMENT,
    )


def test_validator_initialization(
    validator: ConfigurationValidator, temp_schema_dir: Path
) -> None:
    """Test validator initializes correctly."""
    assert validator.schema_dir == temp_schema_dir
    assert validator.environment == ConfigEnvironment.DEVELOPMENT


def test_validate_config_basic(validator: ConfigurationValidator) -> None:
    """Test basic configuration validation."""
    config = {
        "port": 8000,
        "debug_mode": True,
    }

    result = validator.validate_config(config, check_dependencies=False)

    # Should have no errors for basic config
    assert result.valid or len(result.issues) == 0


def test_validate_port_range(validator: ConfigurationValidator) -> None:
    """Test port validation."""
    # Invalid port (too low)
    config = {"port": 100}
    result = validator.validate_config(config, check_dependencies=False)

    port_errors = [i for i in result.issues if i.path == "port"]
    assert len(port_errors) > 0
    assert any(i.severity == ValidationSeverity.ERROR for i in port_errors)

    # Valid port
    config = {"port": 8000}
    result = validator.validate_config(config, check_dependencies=False)

    port_errors = [i for i in result.issues if i.path == "port"]
    port_error_count = sum(
        1 for i in port_errors if i.severity == ValidationSeverity.ERROR
    )
    assert port_error_count == 0


def test_validate_url_format(validator: ConfigurationValidator) -> None:
    """Test URL validation."""
    # Invalid URL (no protocol)
    config = {"base_url": "localhost:8000"}
    result = validator.validate_config(config, check_dependencies=False)

    url_errors = [i for i in result.issues if i.path == "base_url"]
    assert len(url_errors) > 0
    assert any(i.auto_fix is not None for i in url_errors)

    # Valid URL
    config = {"base_url": "http://localhost:8000"}
    result = validator.validate_config(config, check_dependencies=False)

    url_errors = [i for i in result.issues if i.path == "base_url"]
    url_error_count = sum(
        1 for i in url_errors if i.severity == ValidationSeverity.ERROR
    )
    assert url_error_count == 0


def test_validate_dependencies(validator: ConfigurationValidator) -> None:
    """Test dependency validation."""
    # SSL enabled but missing required keys
    config = {
        "ssl_enabled": True,
        # Missing: ssl_cert_path, ssl_key_path
    }

    result = validator.validate_config(config)

    assert result.dependencies_satisfied is False
    cert_errors = [i for i in result.issues if "ssl_cert_path" in i.path]
    key_errors = [i for i in result.issues if "ssl_key_path" in i.path]

    assert len(cert_errors) > 0
    assert len(key_errors) > 0


def test_production_environment_validation(temp_schema_dir: Path) -> None:
    """Test production environment validation."""
    validator = ConfigurationValidator(
        schema_dir=temp_schema_dir,
        environment=ConfigEnvironment.PRODUCTION,
    )

    # SSL should be required in production
    config = {
        "ssl_enabled": False,
        "debug_mode": True,  # Should warn in production
    }

    result = validator.validate_config(config, check_dependencies=False)

    assert result.environment_compatible is False

    ssl_errors = [i for i in result.issues if i.path == "ssl_enabled"]
    debug_warnings = [i for i in result.issues if i.path == "debug_mode"]

    assert len(ssl_errors) > 0
    assert any(i.severity == ValidationSeverity.ERROR for i in ssl_errors)
    assert len(debug_warnings) > 0


def test_auto_fix_application(validator: ConfigurationValidator) -> None:
    """Test auto-fix application."""
    config = {
        "port": 100,  # Invalid port
        "base_url": "localhost:8000",  # Invalid URL
    }

    result = validator.validate_config(config, check_dependencies=False)

    # Check auto-fixes are available
    assert len(result.auto_fixes) > 0

    # Apply auto-fixes
    fixed_config = validator.apply_auto_fixes(config, result)

    # Verify fixes were applied
    assert fixed_config["port"] in [8000, 8001]  # Valid port
    assert fixed_config["base_url"].startswith("http://")


def test_configuration_suggestions(validator: ConfigurationValidator) -> None:
    """Test configuration suggestions."""
    partial_config = {
        "port": 8000,
    }

    suggestions = validator.suggest_configuration(partial_config)

    # Should suggest some configurations
    assert isinstance(suggestions, list)


def test_config_migration(validator: ConfigurationValidator) -> None:
    """Test configuration migration."""
    old_config = {
        "daemon_port": 8000,
        "enable_ssl": True,
    }

    new_config, notes = validator.migrate_config(
        old_config,
        from_version="1.0",
        to_version="2.0",
    )

    # Check migrations were applied
    assert "port" in new_config
    assert "ssl_enabled" in new_config
    assert "daemon_port" not in new_config
    assert "enable_ssl" not in new_config

    # Check migration notes
    assert len(notes) > 0


def test_validation_result_to_dict(validator: ConfigurationValidator) -> None:
    """Test validation result serialization."""
    config = {"port": 100}
    result = validator.validate_config(config, check_dependencies=False)

    result_dict = result.to_dict()

    assert "valid" in result_dict
    assert "issues" in result_dict
    assert "auto_fixes" in result_dict
    assert "error_count" in result_dict
    assert "warning_count" in result_dict


def test_validation_issue_to_dict() -> None:
    """Test validation issue serialization."""
    from src.security.config_validator import ValidationIssue

    issue = ValidationIssue(
        path="port",
        severity=ValidationSeverity.ERROR,
        message="Invalid port",
        suggestion="Use port 8000",
        auto_fix=8000,
    )

    issue_dict = issue.to_dict()

    assert issue_dict["path"] == "port"
    assert issue_dict["severity"] == "error"
    assert issue_dict["message"] == "Invalid port"
    assert issue_dict["suggestion"] == "Use port 8000"
    assert issue_dict["auto_fix"] == 8000


def test_export_validation_report(
    validator: ConfigurationValidator, tmp_path: Path
) -> None:
    """Test validation report export."""
    config = {"port": 100}
    result = validator.validate_config(config, check_dependencies=False)

    output_path = tmp_path / "validation_report.json"
    validator.export_validation_report(result, output_path)

    assert output_path.exists()

    # Verify report contents
    import json

    with output_path.open() as f:
        report = json.load(f)

    assert "timestamp" in report
    assert "environment" in report
    assert "result" in report


def test_conflicting_options(validator: ConfigurationValidator) -> None:
    """Test conflicting configuration options."""
    config = {
        "debug_mode": True,
        "production_mode": True,  # Conflicting with debug_mode
    }

    result = validator.validate_config(config)

    # Should have warnings about conflicting options
    conflict_warnings = [
        i
        for i in result.issues
        if i.severity == ValidationSeverity.WARNING
        and ("debug_mode" in i.path or "production_mode" in i.path)
    ]

    assert len(conflict_warnings) > 0


def test_type_conversion(validator: ConfigurationValidator) -> None:
    """Test type conversion in auto-fixes."""
    # Test string to int conversion
    assert validator._convert_type("8000", "integer") == 8000

    # Test string to bool conversion
    assert validator._convert_type("true", "boolean") is True
    assert validator._convert_type("false", "boolean") is False

    # Test number to string conversion
    assert validator._convert_type(8000, "string") == "8000"


def test_development_environment_validation(temp_schema_dir: Path) -> None:
    """Test development environment specific validation."""
    validator = ConfigurationValidator(
        schema_dir=temp_schema_dir,
        environment=ConfigEnvironment.DEVELOPMENT,
    )

    config = {
        "ssl_enabled": True,
        "allow_self_signed": False,
    }

    result = validator.validate_config(config, check_dependencies=False)

    # Should suggest allowing self-signed certs in dev
    self_signed_issues = [i for i in result.issues if "allow_self_signed" in i.path]

    assert len(self_signed_issues) > 0
