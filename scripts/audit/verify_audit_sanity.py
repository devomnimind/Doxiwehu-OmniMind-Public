import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(PROJECT_ROOT))

# pylint: disable=wrong-import-position
from src.audit.immutable_audit import ImmutableAuditSystem  # noqa: E402


def main():
    print("� Starting Deep Audit Chain REPAIR...")
    audit = ImmutableAuditSystem()

    # Force repair
    result = audit.repair_chain_integrity()

    print("\n📊 Repair Result:")
    print(f"Repaired: {result['repaired']}")
    print(f"Message: {result['message']}")
    if result["repaired"]:
        print(f"Events Repaired: {result.get('events_repaired', 0)}")
        print(f"Events Removed: {result.get('events_removed', 0)}")
        print(f"Events Recovered: {result.get('events_recovered', 0)}")

    # Verify again
    print("\n🔍 Post-Repair Verification...")
    check = audit.verify_chain_integrity()
    print(f"Status: {'✅ VALID' if check['valid'] else '❌ INVALID'}")
    print(f"Message: {check['message']}")


if __name__ == "__main__":
    main()
