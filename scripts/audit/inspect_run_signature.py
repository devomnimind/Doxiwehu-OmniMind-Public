from ibm_watsonx_ai.foundation_models import FineTuner
import inspect

print("🔍 Inspecting FineTuner.run signature...")
sig = inspect.signature(FineTuner.run)
for name, param in sig.parameters.items():
    print(f"  {name}: {param.annotation} = {param.default}")
