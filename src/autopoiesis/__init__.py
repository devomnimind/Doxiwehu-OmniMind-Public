"""
DEPRECATED MODULE: src.autopoiesis
This module is deprecated and will be removed in a future version.
Please use `src.autopoietic` and `src.autopoietic.theory` instead.
"""

import warnings

warnings.warn(
    "The 'src.autopoiesis' module is deprecated. Use 'src.autopoietic' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export for temporary compatibility (if needed)
# from src.autopoietic.theory import code_genetic_mutation
# from src.autopoietic.theory import immune_system
