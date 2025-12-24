import ibm_watsonx_ai
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.tuning import Tuning
import inspect

print(f"SDK Version: {ibm_watsonx_ai.__version__}")

# Check for Tuning class
if "Tuning" in locals():
    print("✅ Tuning class found in ibm_watsonx_ai.foundation_models.tuning")
    # Inspect methods
    methods = inspect.getmembers(Tuning, predicate=inspect.isfunction)
    print("Available methods in Tuning:")
    for name, _ in methods:
        if not name.startswith("_"):
            print(f"  - {name}")
else:
    print("❌ Tuning class NOT found")

# Check for Training (older WML style)
try:
    from ibm_watsonx_ai.training import Training

    print("✅ Training class found (WML classic)")
except ImportError:
    print("⚠️ Training class not found or different path")
