import ibm_watsonx_ai


print(f"SDK Version: {ibm_watsonx_ai.__version__}")
print("\nTop level modules:")
print(dir(ibm_watsonx_ai))

try:
    from ibm_watsonx_ai import foundation_models

    print("\nfoundation_models contents:")
    print(dir(foundation_models))
except ImportError:
    print("\nfoundation_models not found")
