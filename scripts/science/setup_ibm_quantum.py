#!/usr/bin/env python3
"""
Setup IBM Quantum Account
-------------------------
Helper script to configure IBM Quantum access for OmniMind.

Steps:
1. Get your IBM Quantum API token from: https://quantum.ibm.com/
2. Run this script and paste your token when prompted
3. Token will be saved securely for future use
"""

from qiskit_ibm_runtime import QiskitRuntimeService


def setup_ibm_account():
    print("🔮 IBM QUANTUM ACCOUNT SETUP")
    print("=" * 60)
    print()
    print("To use IBM Quantum hardware, you need an API token.")
    print("Get it from: https://quantum.ibm.com/account")
    print()

    token = input("Enter your IBM Quantum API token: ").strip()

    if not token:
        print("❌ No token provided. Exiting.")
        return

    try:
        # Save account
        QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)

        print()
        print("✅ IBM Quantum account saved successfully!")
        print()

        # Test connection
        print("Testing connection...")
        service = QiskitRuntimeService()
        backends = service.backends()

        print(f"✅ Connected! Found {len(backends)} quantum backends:")
        for backend in backends[:5]:  # Show first 5
            print(f"   - {backend.name} ({backend.num_qubits} qubits)")

        if len(backends) > 5:
            print(f"   ... and {len(backends) - 5} more")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your token and try again.")


if __name__ == "__main__":
    setup_ibm_account()
