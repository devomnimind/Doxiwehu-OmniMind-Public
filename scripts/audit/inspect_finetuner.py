from ibm_watsonx_ai.foundation_models import FineTuner
import inspect

print("✅ FineTuner class found!")
print("\n__init__ parameters:")
sig = inspect.signature(FineTuner.__init__)
for name, param in sig.parameters.items():
    print(f"  {name}: {param.annotation} = {param.default}")

print("\nMethods:")
methods = inspect.getmembers(FineTuner, predicate=inspect.isfunction)
for name, _ in methods:
    if not name.startswith("_"):
        print(f"  - {name}")
