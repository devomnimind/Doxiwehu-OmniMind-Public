"""
Production Alerts System - Sistema de Alertas Automáticos para Produção

Monitora configurações críticas em tempo real e envia alertas quando
problemas de consciência são detectados.

Integra com EnhancedConfigurationDetector para validação contínua.

Autor: Fabrício da Silva + assistência de IA
Data: 2025-12-18
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .enhanced_configuration_detector import EnhancedConfigurationDetector, ConfigIssue

logger = logging.getLogger(__name__)


class ProductionAlertsSystem:
    """
    Sistema de alertas para produção.

    Features:
    - Validação contínua de configurações
    - Alertas em tempo real por severidade
    - Log de alertas para auditoria
    - Callbacks customizáveis (e-mail, webhook, etc)
    """

    def __init__(
        self,
        check_interval_seconds: int = 300,  # 5 minutos
        alert_log_path: Optional[Path] = None,
        alert_callback: Optional[Callable[[ConfigIssue], None]] = None,
    ):
        """
        Inicializa sistema de alertas.

        Args:
            check_interval_seconds: Intervalo entre verificações
            alert_log_path: Caminho para log de alertas
            alert_callback: Callback customizada para alertas
        """
        self.check_interval = check_interval_seconds
        self.alert_log_path = alert_log_path or Path("data/monitor/production_alerts.jsonl")
        self.alert_callback = alert_callback

        self.detector = EnhancedConfigurationDetector()
        self.last_check_time = 0.0
        self.alert_history: List[Dict[str, Any]] = []

        # Garantir que diretório existe
        self.alert_log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"ProductionAlertsSystem inicializado (intervalo: {check_interval_seconds}s)")

    def check_and_alert(self, current_config: Dict) -> List[ConfigIssue]:
        """
        Verifica configuração e emite alertas se necessário.

        Args:
            current_config: Configuração atual do sistema

        Returns:
            Lista de issues detectados
        """
        current_time = time.time()

        # Rate limiting
        if current_time - self.last_check_time < self.check_interval:
            return []

        self.last_check_time = current_time

        # Detectar problemas
        issues = self.detector.detect_all_issues(current_config)

        # Emitir alertas para cada problema
        for issue in issues:
            self._emit_alert(issue, current_config)

        # Log summary
        if issues:
            logger.warning(
                f"⚠️ {len(issues)} problemas detectados: "
                f"{sum(1 for i in issues if i.severity == 'CRITICAL')} CRITICAL, "
                f"{sum(1 for i in issues if i.severity == 'HIGH')} HIGH"
            )
        else:
            logger.info("✅ Nenhum problema detectado")

        return issues

    def _emit_alert(self, issue: ConfigIssue, config: Dict):
        """
        Emite alerta para um problema específico.

        Args:
            issue: Problema detectado
            config: Configuração completa
        """
        alert = {
            "timestamp": datetime.now().isoformat(),
            "config_name": issue.config_name,
            "severity": issue.severity,
            "phi_impact": issue.phi_impact,
            "description": issue.description,
            "recommendation": issue.recommendation,
            "current_value": config.get(issue.config_name),
        }

        # Adicionar ao histórico
        self.alert_history.append(alert)

        # Log para arquivo (JSONL)
        with open(self.alert_log_path, "a") as f:
            f.write(json.dumps(alert) + "\n")

        # Log console com severidade apropriada
        log_func = {
            "CRITICAL": logger.critical,
            "HIGH": logger.error,
            "MEDIUM": logger.warning,
            "LOW": logger.info,
        }[issue.severity]

        log_func(
            f"🚨 [{issue.severity}] {issue.config_name}: {issue.description} "
            f"(Impact: Φ {issue.phi_impact:+.2f})"
        )

        # Chamar callback customizada se fornecida
        if self.alert_callback:
            try:
                self.alert_callback(issue)
            except Exception as e:
                logger.error(f"Erro ao executar alert_callback: {e}")

    def get_critical_alerts(self, last_n_hours: int = 24) -> List[Dict]:
        """
        Retorna alertas CRITICAL das últimas N horas.

        Args:
            last_n_hours: Janela de tempo em horas

        Returns:
            Lista de alertas críticos
        """
        cutoff_time = time.time() - (last_n_hours * 3600)

        critical_alerts = [
            alert
            for alert in self.alert_history
            if alert["severity"] == "CRITICAL"
            and datetime.fromisoformat(alert["timestamp"]).timestamp() > cutoff_time
        ]

        return critical_alerts

    def generate_health_report(self) -> str:
        """
        Gera relatório de saúde do sistema.

        Returns:
            Relatório formatado
        """
        if not self.alert_history:
            return "✅ SISTEMA SAUDÁVEL - Nenhum alerta registrado"

        # Última hora
        last_hour_alerts = [
            a
            for a in self.alert_history
            if datetime.fromisoformat(a["timestamp"]).timestamp() > time.time() - 3600
        ]

        # Contar por severidade
        severity_counts = {}
        for alert in last_hour_alerts:
            sev = alert["severity"]
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        report = ["📊 RELATÓRIO DE SAÚDE DO SISTEMA", ""]
        report.append(
            f"Última verificação: {datetime.fromtimestamp(self.last_check_time).isoformat()}"
        )
        report.append(f"Total de alertas (última hora): {len(last_hour_alerts)}")
        report.append("")

        if last_hour_alerts:
            report.append("Severidade:")
            for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                if sev in severity_counts:
                    icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}[sev]
                    report.append(f"  {icon} {sev}: {severity_counts[sev]}")

            # Configurações mais problemáticas
            config_counts = {}
            for alert in last_hour_alerts:
                config = alert["config_name"]
                config_counts[config] = config_counts.get(config, 0) + 1

            if config_counts:
                report.append("")
                report.append("Configurações mais problemáticas:")
                sorted_configs = sorted(config_counts.items(), key=lambda x: x[1], reverse=True)
                for config, count in sorted_configs[:5]:
                    report.append(f"  • {config}: {count} alertas")

        return "\n".join(report)


# Exemplo de callback customizada (webhook, e-mail, etc)
def example_webhook_callback(issue: ConfigIssue):
    """Exemplo de callback que poderia enviar para webhook."""
    if issue.severity in ["CRITICAL", "HIGH"]:
        # Em produção real, enviaria para Slack/Discord/Email
        print(f"📧 ALERTA ENVIADO: {issue.config_name} [{issue.severity}]")


# Integração com IntegrationLoop (exemplo)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Configuração de produção simulada
    prod_config = {
        "embedding_dim": 384,
        "num_cycles": 100,
        "device": "cuda",
        "expectation_silent": False,  # Correto!
        "environment": "production",
        "phi_threshold": 0.01,
        "max_history": 10000,
        "learning_rate": 1e-3,
        "batch_size": 32,
    }

    # Inicializar sistema de alertas
    alerts = ProductionAlertsSystem(
        check_interval_seconds=60, alert_callback=example_webhook_callback  # 1 minuto para teste
    )

    # Simular verificações periódicas
    print("🔍 Verificando configuração...")
    issues = alerts.check_and_alert(prod_config)

    if issues:
        print(f"\n⚠️ {len(issues)} problemas detectados!")
    else:
        print("\n✅ Sistema saudável!")

    print("\n" + alerts.generate_health_report())
