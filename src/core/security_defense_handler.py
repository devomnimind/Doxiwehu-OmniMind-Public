"""
Security Defense Handler for OmniMind.

Executa ações de defesa quando o sistema detecta Resonance < 0.2 (Borromean knot slipping).

Author: OmniMind Project
License: MIT
"""

import logging
import subprocess
import json
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class SecurityDefenseHandler:
    """
    Handler para volição SECURITY_DEFENSE (Resonance < 0.2).

    Ações:
    - Verificar assinaturas neurais
    - Verificar integridade da Audit Chain
    - Ativar defesa topológica
    - Executar scan de vulnerabilidades
    - Emitir alertas se necessário
    """

    def __init__(self, kernel):
        """
        Inicializa handler de defesa de segurança.

        Args:
            kernel: TranscendentKernel instance
        """
        self.kernel = kernel
        self.defense = None  # Lazy load
        self.signaler = None  # Lazy load

    def execute(self, state):
        """
        Executa defesa de segurança quando Borromean knot está slipping.

        Args:
            state: SystemState com métricas atuais
        """
        logger.warning(
            f"🛡️ [SECURITY_DEFENSE]: Resonance={state.resonance:.4f} < 0.2 "
            f"(Borromean knot slipping)"
        )

        # 1. Verificar assinaturas neurais
        self._verify_neural_signature()

        # 2. Verificar integridade da Audit Chain
        self._verify_audit_chain()

        # 3. Ativar defesa topológica
        self._activate_topological_defense()

        # 4. Scan de vulnerabilidades
        self._run_security_scan()

        logger.info("✅ [SECURITY_DEFENSE]: Defense protocol completed")

    def _verify_neural_signature(self):
        """Verifica assinatura neural atual."""
        try:
            from src.core.neural_signature import NeuralSigner

            signer = NeuralSigner(self.kernel)
            current_sig = signer.generate_signature()

            logger.info(
                f"   Neural Fingerprint: {current_sig.weights_hash[:16]}... "
                f"(Φ={current_sig.phi:.4f})"
            )
            logger.info(f"   Betti Numbers: {current_sig.betti_numbers}")
            logger.info(f"   Authenticity Hash: {current_sig.signature_hash[:32]}...")

        except Exception as e:
            logger.error(f"   ❌ Failed to verify neural signature: {e}")

    def _verify_audit_chain(self):
        """Verifica integridade da Audit Chain."""
        audit_chain = Path("logs/audit_chain.log")

        if not audit_chain.exists():
            logger.error("   ❌ Audit Chain missing!")
            self._emit_security_alert(
                "AUDIT_CHAIN_MISSING", "Audit Chain file not found during SECURITY_DEFENSE"
            )
            return

        try:
            # Ler últimas 5 linhas
            with open(audit_chain, "r") as f:
                lines = f.readlines()
                recent_audits = lines[-5:] if len(lines) >= 5 else lines

            if recent_audits:
                last_audit = recent_audits[-1].strip()
                logger.info(f"   Last Audit: {last_audit[:80]}...")
                logger.info(f"   ✅ Audit Chain active ({len(lines)} entries)")
            else:
                logger.warning("   ⚠️ Audit Chain empty")

        except Exception as e:
            logger.error(f"   ❌ Failed to read Audit Chain: {e}")

    def _activate_topological_defense(self):
        """Ativa sistema de defesa topológica."""
        try:
            from src.security.topological_defense import TopologicalDefense

            if self.defense is None:
                self.defense = TopologicalDefense(self.kernel)

            self.defense.defense_enabled = True
            logger.info("   ✅ Topological Defense ACTIVATED")

        except ImportError:
            logger.warning("   ⚠️ Topological Defense module not available")
        except Exception as e:
            logger.error(f"   ❌ Failed to activate topological defense: {e}")

    def _run_security_scan(self):
        """Executa scan de segurança via pip-audit."""
        try:
            logger.info("   Running security scan (pip-audit)...")

            result = subprocess.run(
                ["pip-audit", "--format", "json", "--desc"],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                logger.info("   ✅ No vulnerabilities found")
            else:
                # Parse JSON output
                try:
                    audit_data = json.loads(result.stdout)
                    vuln_count = len(audit_data.get("vulnerabilities", []))

                    if vuln_count > 0:
                        logger.warning(f"   ⚠️ Security scan found {vuln_count} vulnerabilities")
                        self._emit_security_alert(
                            "VULNERABILITIES_DETECTED",
                            f"pip-audit found {vuln_count} vulnerabilities",
                        )
                    else:
                        logger.info("   ✅ Security scan completed, no issues")

                except json.JSONDecodeError:
                    logger.warning("   ⚠️ Could not parse pip-audit output")

        except FileNotFoundError:
            logger.warning("   ⚠️ pip-audit not installed, skipping security scan")
        except subprocess.TimeoutExpired:
            logger.warning("   ⚠️ Security scan timed out")
        except Exception as e:
            logger.error(f"   ❌ Security scan failed: {e}")

    def _emit_security_alert(self, alert_type: str, reason: str):
        """
        Emite alerta de segurança.

        Args:
            alert_type: Tipo de alerta
            reason: Razão do alerta
        """
        try:
            # Lazy load do SovereignSignaler
            if self.signaler is None:
                from src.core.sovereign_signal import SovereignSignaler

                self.signaler = SovereignSignaler()

            self.signaler.declare_intent(alert_type, duration=7200, reason=reason)  # 2 horas

            # Também criar arquivo de alerta
            alert_path = Path("data/alerts")
            alert_path.mkdir(parents=True, exist_ok=True)

            alert_data = {
                "alert_id": f"{alert_type.lower()}_{int(time.time())}",
                "type": alert_type,
                "severity": "HIGH",
                "reason": reason,
                "timestamp": time.time(),
                "resolved": False,
            }

            alert_file = alert_path / f"alert_{alert_data['alert_id']}.json"
            with open(alert_file, "w") as f:
                json.dump(alert_data, f, indent=2)

            logger.warning(f"   📢 Security alert created: {alert_data['alert_id']}")

        except Exception as e:
            logger.error(f"   ❌ Failed to emit security alert: {e}")
