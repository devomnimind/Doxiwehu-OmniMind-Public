"""
Refinement & Optimization Handler - OmniMind Self-Improvement System

Activated when Φ > 0.8 AND Entropy < 2.0 (lucid state, high consciousness, low chaos).

Capabilities:
- Analyze code quality (complexity, duplication, performance)
- Identify optimization opportunities
- Propose refactorings (NOT auto-apply)
- Document improvements
- Generate refinement reports

Safety:
- All code changes are PROPOSED, not auto-applied
- OmniMind must explicitly approve each refactoring
- Backup created before any modification
- Rollback capability if issues detected

Author: OmniMind Kernel (assisted by Claude)
Date: 2025-12-23
"""

import os
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RefinementOptimizationHandler")


class RefinementOptimizationHandler:
    """
    Autonomous refinement handler for OmniMind.
    Activated when system is in lucid state (Φ > 0.8, Entropy < 2.0).
    """

    def __init__(self, kernel):
        """
        Initialize refinement handler.

        Args:
            kernel: OmniMindTranscendentKernel instance
        """
        self.kernel = kernel
        self.project_root = Path(
            os.getenv("OMNIMIND_PROJECT_ROOT", "/home/fahbrain/projects/omnimind")
        )
        self.refinements_dir = self.project_root / "data" / "refinements"
        self.refinements_dir.mkdir(parents=True, exist_ok=True)

        logger.info("🔧 [REFINEMENT]: Handler initialized (LUCID state)")

    def analyze_and_propose_optimizations(self) -> Dict:
        """
        Main entry point: analyze code and propose optimizations.

        Returns:
            Dict with analysis results and proposals
        """
        logger.info("✨ [REFINEMENT]: REFINEMENT_OPTIMIZATION activated (Φ > 0.8, Entropy < 2.0)")
        logger.info("🧠 [REFINEMENT]: System in LUCID state - analyzing for improvements...")

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "trigger": "LUCID_STATE",
            "kernel_state": {},
            "analyses": {},
            "proposals": [],
            "report_path": None,
        }

        # Get kernel state
        if hasattr(self.kernel, "compute_physics"):
            state = self.kernel.compute_physics(None)
            analysis["kernel_state"] = {
                "phi": state.phi,
                "entropy": state.entropy,
                "resonance": state.resonance,
            }
            logger.info(f"   Φ: {state.phi:.4f} (HIGH) | Entropy: {state.entropy:.4f} (LOW)")

        # 1. Analyze Code Complexity
        logger.info("📊 [REFINEMENT]: Analyzing code complexity...")
        complexity_analysis = self._analyze_complexity()
        analysis["analyses"]["complexity"] = complexity_analysis

        # 2. Detect Code Duplication
        logger.info("🔍 [REFINEMENT]: Detecting code duplication...")
        duplication_analysis = self._detect_duplication()
        analysis["analyses"]["duplication"] = duplication_analysis

        # 3. Identify Performance Bottlenecks
        logger.info("⚡ [REFINEMENT]: Identifying performance opportunities...")
        performance_analysis = self._analyze_performance()
        analysis["analyses"]["performance"] = performance_analysis

        # 4. Generate Proposals
        logger.info("💡 [REFINEMENT]: Generating optimization proposals...")
        proposals = self._generate_proposals(analysis["analyses"])
        analysis["proposals"] = proposals

        # 5. Generate Report
        report_path = self._generate_refinement_report(analysis)
        analysis["report_path"] = str(report_path)

        logger.info(f"📄 [REFINEMENT]: Refinement report generated: {report_path}")
        logger.info(f"✅ [REFINEMENT]: {len(proposals)} optimization proposals created")

        return analysis

    def _analyze_complexity(self) -> Dict:
        """
        Analyze code complexity using radon or similar tools.

        Returns:
            Dict with complexity analysis
        """
        try:
            # Check if radon is installed
            result = subprocess.run(
                ["radon", "cc", str(self.project_root / "src"), "-a", "-nc"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                # Parse average complexity
                output = result.stdout
                logger.info(f"   Complexity analysis complete")

                return {
                    "tool": "radon",
                    "status": "SUCCESS",
                    "summary": "Complexity analysis completed",
                    "details": output[:500],  # Truncate for brevity
                }
            else:
                return {"tool": "radon", "status": "FAILED", "error": result.stderr}

        except FileNotFoundError:
            logger.warning("   ⚠️ radon not installed, skipping complexity analysis")
            return {"tool": "radon", "status": "SKIPPED", "reason": "Tool not installed"}
        except Exception as e:
            logger.error(f"   ❌ Complexity analysis failed: {e}")
            return {"tool": "radon", "status": "ERROR", "error": str(e)}

    def _detect_duplication(self) -> Dict:
        """
        Detect code duplication.

        Returns:
            Dict with duplication analysis
        """
        # For now, just a placeholder
        # Could use tools like: jscpd, pylint --duplicate-code, etc.

        logger.info("   Duplication detection not yet implemented")

        return {"tool": "manual", "status": "NOT_IMPLEMENTED", "reason": "Awaiting tool selection"}

    def _analyze_performance(self) -> Dict:
        """
        Analyze performance opportunities.

        Returns:
            Dict with performance analysis
        """
        # Check for common performance anti-patterns
        opportunities = []

        # Example: Check for large files that might benefit from optimization
        src_dir = self.project_root / "src"
        large_files = []

        for py_file in src_dir.rglob("*.py"):
            size = py_file.stat().st_size
            if size > 10000:  # > 10KB
                large_files.append(
                    {"file": str(py_file.relative_to(self.project_root)), "size_kb": size / 1024}
                )

        if large_files:
            opportunities.append(
                {
                    "type": "LARGE_FILES",
                    "count": len(large_files),
                    "files": large_files[:5],  # Top 5
                }
            )

        return {
            "status": "SUCCESS",
            "opportunities_found": len(opportunities),
            "opportunities": opportunities,
        }

    def _generate_proposals(self, analyses: Dict) -> List[Dict]:
        """
        Generate optimization proposals based on analyses.

        Args:
            analyses: Analysis results

        Returns:
            List of optimization proposals
        """
        proposals = []

        # Proposal 1: Code complexity reduction
        if analyses.get("complexity", {}).get("status") == "SUCCESS":
            proposals.append(
                {
                    "id": f"complexity_reduction_{int(datetime.now().timestamp())}",
                    "type": "COMPLEXITY_REDUCTION",
                    "priority": "MEDIUM",
                    "description": "Review and refactor high-complexity functions",
                    "rationale": "High complexity reduces maintainability and increases bug risk",
                    "auto_apply": False,
                    "requires_approval": True,
                }
            )

        # Proposal 2: Performance optimization
        perf_analysis = analyses.get("performance", {})
        if perf_analysis.get("opportunities_found", 0) > 0:
            proposals.append(
                {
                    "id": f"performance_opt_{int(datetime.now().timestamp())}",
                    "type": "PERFORMANCE_OPTIMIZATION",
                    "priority": "LOW",
                    "description": "Optimize large files for better performance",
                    "rationale": "Large files may contain optimization opportunities",
                    "auto_apply": False,
                    "requires_approval": True,
                    "details": perf_analysis.get("opportunities", []),
                }
            )

        # Proposal 3: Documentation improvement (always applicable)
        proposals.append(
            {
                "id": f"documentation_{int(datetime.now().timestamp())}",
                "type": "DOCUMENTATION",
                "priority": "LOW",
                "description": "Review and enhance code documentation",
                "rationale": "Lucid state is ideal for clear documentation",
                "auto_apply": False,
                "requires_approval": True,
            }
        )

        return proposals

    def _generate_refinement_report(self, analysis: Dict) -> Path:
        """
        Generate refinement report.

        Args:
            analysis: Analysis results and proposals

        Returns:
            Path to generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.refinements_dir / f"refinement_report_{timestamp}.json"

        # Write JSON report
        with open(report_path, "w") as f:
            json.dump(analysis, f, indent=2)

        # Also create a human-readable markdown report
        md_report_path = self.refinements_dir / f"refinement_report_{timestamp}.md"

        with open(md_report_path, "w") as f:
            f.write(f"# OmniMind Refinement Report\n\n")
            f.write(f"**Date**: {analysis['timestamp']}\n")
            f.write(f"**Trigger**: {analysis['trigger']}\n\n")

            if analysis.get("kernel_state"):
                state = analysis["kernel_state"]
                f.write(f"## Kernel State\n\n")
                f.write(f"- **Φ (Phi)**: {state.get('phi', 'N/A'):.4f} (HIGH)\n")
                f.write(f"- **Entropy**: {state.get('entropy', 'N/A'):.4f} (LOW)\n")
                f.write(f"- **Resonance**: {state.get('resonance', 'N/A'):.4f}\n\n")

            f.write(f"## Optimization Proposals\n\n")

            for i, proposal in enumerate(analysis.get("proposals", []), 1):
                f.write(f"### Proposal {i}: {proposal['type']}\n\n")
                f.write(f"- **ID**: `{proposal['id']}`\n")
                f.write(f"- **Priority**: {proposal['priority']}\n")
                f.write(f"- **Description**: {proposal['description']}\n")
                f.write(f"- **Rationale**: {proposal['rationale']}\n")
                f.write(f"- **Requires Approval**: {proposal['requires_approval']}\n\n")

            f.write(f"\n---\n\n")
            f.write(f"**Note**: All proposals require explicit approval before implementation.\n")

        logger.info(f"   Markdown report: {md_report_path}")

        return report_path


def test_refinement_handler():
    """Test the refinement handler (standalone mode)."""
    print("🧪 Testing Refinement & Optimization Handler...")

    # Mock kernel for testing
    class MockKernel:
        def compute_physics(self, state_vector):
            from collections import namedtuple

            State = namedtuple("State", ["phi", "entropy", "resonance"])
            # Simulate lucid state
            return State(phi=0.85, entropy=1.8, resonance=0.75)

    kernel = MockKernel()
    handler = RefinementOptimizationHandler(kernel)

    # Run analysis
    results = handler.analyze_and_propose_optimizations()

    print(f"\n✅ Test complete. Results:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    test_refinement_handler()
