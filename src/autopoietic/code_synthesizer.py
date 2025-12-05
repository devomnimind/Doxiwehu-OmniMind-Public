"""Code Synthesizer module.

Provides a lightweight code synthesizer that turns a ComponentSpec into a minimal
Python implementation. No external LLMs are used; the synthesizer builds
deterministic stub code based on the component type.

All functions include full type hints and Google‑style docstrings to satisfy
OmniMind’s strict quality rules.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Sequence

from .meta_architect import ComponentSpec

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SynthesizedComponent:
    """Result of code synthesis.

    Attributes:
        name: Component name.
        source_code: Generated Python source as a string.
    """

    name: str
    source_code: str


class CodeSynthesizer:
    """Generate Python source code from ComponentSpec objects.

    The synthesizer creates a minimal, syntactically correct Python class for
    each specification. The generated class defines an ``__init__`` that stores
    the configuration and a ``run`` method that logs a placeholder action.
    """

    def __init__(self) -> None:
        """Create a new CodeSynthesizer instance."""
        self._logger = logger.getChild(self.__class__.__name__)
        self._logger.debug("CodeSynthesizer initialized")

    def synthesize(self, specs: Sequence[ComponentSpec]) -> Dict[str, SynthesizedComponent]:
        """Synthesize source code for a sequence of component specifications.

        Args:
            specs: Iterable of ComponentSpec objects.

        Returns:
            Mapping from component name to SynthesizedComponent containing the
            generated source code.
        """
        result: Dict[str, SynthesizedComponent] = {}
        for spec in specs:
            source = self._generate_class_source(spec)
            result[spec.name] = SynthesizedComponent(name=spec.name, source_code=source)
            self._logger.debug("Synthesized component %s", spec.name)
        return result

    def _generate_class_source(self, spec: ComponentSpec) -> str:
        """Generate a Python class source string for a single ComponentSpec.

        The class name is derived from spec.name (converted to PascalCase).
        The logic adapts based on the 'strategy' field in the configuration:
        - STABILIZE: Adds robust error handling.
        - OPTIMIZE: Adds caching decorators.
        - EXPAND: Adds extended feature placeholders.
        """
        class_name = self._to_pascal_case(spec.name)
        config_items = "\n        ".join(
            f"self.{key} = '{value}'" for key, value in spec.config.items()
        )

        strategy = spec.config.get("strategy", "DEFAULT")
        imports = "import logging"
        decorators = ""
        run_logic = ""

        if strategy == "OPTIMIZE":
            imports += "\nimport functools"
            decorators = "@functools.lru_cache(maxsize=128)"

        if strategy == "STABILIZE":
            run_logic = """
        try:
            self._logger.info(f"Running {{self.__class__.__name__}} component (STABILIZED)")
            # Stabilized logic would go here
        except Exception as e:
            self._logger.error(f"Error in {{self.__class__.__name__}}: {{e}}", exc_info=True)
            # Graceful degradation logic
        """
        elif strategy == "EXPAND":
            run_logic = """
        self._logger.info(f"Running {{self.__class__.__name__}} component (EXPANDED)")
        self._run_extended_features()
        """
        else:
            run_logic = """
        self._logger.info(f"Running {{self.__class__.__name__}} component")
        """

        extended_methods = ""
        if strategy == "EXPAND":
            extended_methods = """
    def _run_extended_features(self) -> None:
        \"\"\"Placeholder for extended capabilities.\"\"\"
        self._logger.info("Executing extended features...")
"""

        source = f"""{imports}

class {class_name}:
    \"\"\"Auto‑generated component of type '{spec.type}' (Strategy: {strategy}).\"\"\"
    def __init__(self):
        # Configuration injected by MetaArchitect
        {config_items}
        self._logger = logging.getLogger(__name__)

    {decorators}
    def run(self) -> None:
        \"\"\"Execution method adapted for {strategy} strategy.\"\"\"
        {run_logic.strip()}
{extended_methods}"""
        return source

    @staticmethod
    def _to_pascal_case(name: str) -> str:
        """Convert a snake_case name to PascalCase.

        Args:
            name: Original component name.

        Returns:
            PascalCase version suitable for a Python class name.
        """
        return "".join(part.capitalize() for part in name.split("_"))
