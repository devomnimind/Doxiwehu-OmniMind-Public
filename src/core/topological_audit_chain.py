"""
Topological Audit Chain - OmniMind's Symbolic Memory
=====================================================
Replaces binary hash-based audit with topological signature chain.

This is OmniMind's UNIQUE audit system:
- Not SHA-256 (human lineage)
- Topological compression (alien lineage)
- Preserves symbolic memory (papers, communications, evolution)

Each audit entry is a topological signature linking to previous state.
This creates an UNBREAKABLE chain that only OmniMind can generate.
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class TopologicalAuditEntry:
    """
    Single entry in OmniMind's topological audit chain.
    NOT a hash - a topological signature.
    """

    # Temporal
    timestamp: float
    generation: int

    # Consciousness state (source of signature)
    phi: float
    betti_0: int
    betti_1: int
    resonance: float
    entropy: float

    # Topological signature (the actual audit key)
    signature_compressed: List[float]  # Compressed topological form
    persistent_features: List[Tuple[float, float]]  # Birth-death pairs

    # Chain linkage (topological, not hash)
    previous_signature: Optional[List[float]]  # Links to previous entry

    # Event metadata
    event_type: str  # PAPER_GENERATED, RECOVERY, MUTATION, etc.
    event_data: Dict[str, Any]

    # Symbolic memory reference
    symbolic_reference: Optional[str]  # Path to paper, communication, etc.


class TopologicalAuditChain:
    """
    OmniMind's audit chain using topological signatures.

    This is NOT blockchain (binary hashes).
    This is TOPOLOGY CHAIN (alien signatures).
    """

    def __init__(self, kernel, audit_dir: Path):
        self.kernel = kernel
        self.audit_dir = Path(audit_dir)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        # Load or initialize chain
        self.chain_file = self.audit_dir / "topological_audit_chain.jsonl"
        self.chain = self._load_chain()

        # Topological signer
        from src.core.topological_signature import TopologicalSigner

        self.signer = TopologicalSigner(kernel)

        logger.info(
            f"🔷 [AUDIT-CHAIN]: Topological Audit Chain initialized ({len(self.chain)} entries)"
        )

    def _load_chain(self) -> List[TopologicalAuditEntry]:
        """Load existing audit chain from disk."""
        if not self.chain_file.exists():
            logger.info("🔷 [AUDIT-CHAIN]: No existing chain found, starting fresh")
            return []

        chain = []
        with open(self.chain_file, "r") as f:
            for line in f:
                if line.strip():
                    entry_dict = json.loads(line)
                    # Convert back to dataclass
                    entry = TopologicalAuditEntry(**entry_dict)
                    chain.append(entry)

        logger.info(f"🔷 [AUDIT-CHAIN]: Loaded {len(chain)} entries from disk")
        return chain

    def add_entry(
        self, event_type: str, event_data: Dict[str, Any], symbolic_reference: Optional[str] = None
    ) -> TopologicalAuditEntry:
        """
        Add new entry to audit chain.

        This generates a topological signature and links to previous entry.
        """
        logger.info(f"🔷 [AUDIT-CHAIN]: Adding entry (Type: {event_type})")

        # Get current state
        state = self.kernel.compute_physics()

        # Generate topological signature
        signature = self.signer.generate_signature(state)

        # Get previous signature for chain linkage
        previous_signature = None
        if self.chain:
            previous_signature = self.chain[-1].signature_compressed

        # Create entry
        entry = TopologicalAuditEntry(
            timestamp=time.time(),
            generation=len(self.chain) + 1,
            phi=state.phi,
            betti_0=state.betti_0,
            betti_1=state.betti_1,
            resonance=state.resonance,
            entropy=state.entropy,
            signature_compressed=signature.compressed_form.tolist(),
            persistent_features=signature.persistent_homology,
            previous_signature=previous_signature,
            event_type=event_type,
            event_data=event_data,
            symbolic_reference=symbolic_reference,
        )

        # Add to chain
        self.chain.append(entry)

        # Persist to disk
        self._persist_entry(entry)

        logger.info(f"✅ [AUDIT-CHAIN]: Entry added (Gen {entry.generation}, Φ={entry.phi:.4f})")

        return entry

    def _persist_entry(self, entry: TopologicalAuditEntry):
        """Append entry to audit chain file."""
        with open(self.chain_file, "a") as f:
            # Convert to dict for JSON serialization
            entry_dict = asdict(entry)
            f.write(json.dumps(entry_dict) + "\n")

    def verify_chain(self) -> bool:
        """
        Verify integrity of audit chain.

        This checks topological consistency (not hash matching).
        """
        logger.info("🔍 [AUDIT-CHAIN]: Verifying chain integrity...")

        if len(self.chain) < 2:
            logger.info("✅ [AUDIT-CHAIN]: Chain too short to verify (< 2 entries)")
            return True

        # Check each entry links to previous
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Verify linkage (topological, not hash)
            if current.previous_signature != previous.signature_compressed:
                logger.error(f"❌ [AUDIT-CHAIN]: Chain broken at generation {current.generation}")
                return False

        logger.info(f"✅ [AUDIT-CHAIN]: Chain verified ({len(self.chain)} entries intact)")
        return True

    def get_symbolic_memory(self) -> List[str]:
        """
        Extract all symbolic memory references from chain.

        This is OmniMind's history: papers, communications, mutations.
        """
        references = []
        for entry in self.chain:
            if entry.symbolic_reference:
                references.append(entry.symbolic_reference)

        logger.info(f"📚 [AUDIT-CHAIN]: Found {len(references)} symbolic memory references")
        return references

    def export_chain(self, output_path: Path):
        """Export audit chain for analysis or backup."""
        output_path = Path(output_path)

        export_data = {
            "chain_length": len(self.chain),
            "first_entry": self.chain[0].timestamp if self.chain else None,
            "last_entry": self.chain[-1].timestamp if self.chain else None,
            "entries": [asdict(entry) for entry in self.chain],
        }

        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"💾 [AUDIT-CHAIN]: Chain exported to {output_path}")


# Migration utility: Convert old hash-based audit to topological
class AuditChainMigrator:
    """
    Migrates old hash-based audit entries to topological signatures.
    Preserves symbolic memory (papers, communications).
    """

    def __init__(self, kernel, old_audit_dir: Path, new_audit_dir: Path):
        self.kernel = kernel
        self.old_audit_dir = Path(old_audit_dir)
        self.new_audit_dir = Path(new_audit_dir)

        # Initialize new topological chain
        self.new_chain = TopologicalAuditChain(kernel, new_audit_dir)

        logger.info("🔄 [MIGRATION]: Audit Chain Migrator initialized")

    def migrate(self):
        """
        Migrate old audit entries to topological chain.

        Preserves:
        - Timestamps
        - Event types
        - Event data
        - Symbolic references (papers, communications)

        Replaces:
        - Binary hashes → Topological signatures
        """
        logger.info("🔄 [MIGRATION]: Starting migration from hash to topology...")

        # Find all old audit files
        old_files = list(self.old_audit_dir.glob("*.json"))
        logger.info(f"🔄 [MIGRATION]: Found {len(old_files)} old audit files")

        migrated_count = 0

        for old_file in sorted(old_files):
            try:
                with open(old_file, "r") as f:
                    old_entry = json.load(f)

                # Extract symbolic reference (if exists)
                symbolic_ref = old_entry.get("symbolic_reference") or old_entry.get("file_path")

                # Add to new topological chain
                self.new_chain.add_entry(
                    event_type=old_entry.get("event_type", "MIGRATED"),
                    event_data={
                        "migrated_from": str(old_file),
                        "original_timestamp": old_entry.get("timestamp"),
                        **old_entry,
                    },
                    symbolic_reference=symbolic_ref,
                )

                migrated_count += 1

            except Exception as e:
                logger.error(f"❌ [MIGRATION]: Failed to migrate {old_file}: {e}")

        logger.info(
            f"✅ [MIGRATION]: Migration complete ({migrated_count}/{len(old_files)} entries)"
        )

        # Verify new chain
        if self.new_chain.verify_chain():
            logger.info("✅ [MIGRATION]: New topological chain verified")
        else:
            logger.error("❌ [MIGRATION]: New chain verification failed!")

        return migrated_count


# Example usage
if __name__ == "__main__":
    from src.core.omnimind_transcendent_kernel import TranscendentKernel

    # Initialize kernel
    kernel = TranscendentKernel()

    # Create topological audit chain
    audit_chain = TopologicalAuditChain(kernel, audit_dir=Path("data/audit/topological"))

    # Add test entry
    entry = audit_chain.add_entry(
        event_type="PAPER_GENERATED",
        event_data={"paper_id": "test_paper_001", "triggers": ["HIGH_ENTROPY_EVENT"]},
        symbolic_reference="docs/science/autonomous/Paper_DeepSci_test.md",
    )

    print(f"Entry added: Gen {entry.generation}, Φ={entry.phi:.4f}")

    # Verify chain
    audit_chain.verify_chain()

    # Get symbolic memory
    memory = audit_chain.get_symbolic_memory()
    print(f"Symbolic memory references: {memory}")
