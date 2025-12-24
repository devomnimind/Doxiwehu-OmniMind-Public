#!/usr/bin/env python3
"""
OmniMind MCP Manager (Orchestrator Tool)
========================================

Gerenciador granular de Processos de Contexto Modelo (MCPs).
Permite iniciar, parar e reiniciar MCPs individualmente, respeitando a soberania da máquina.

Uso:
    ./mcp_manager.py start <mcp_name|all>
    ./mcp_manager.py stop <mcp_name|all>
    ./mcp_manager.py restart <mcp_name|all>
    ./mcp_manager.py status
    ./mcp_manager.py logs <mcp_name>

Autor: Antigravity Agent (assistindo Fabrício da Silva)
Data: 2025-12-24
"""

import sys
import os
import time
import json
import signal
import psutil
import requests
import subprocess
import argparse
from pathlib import Path

# Configuração
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python3"
PID_DIR = Path("/tmp/omnimind_pids")
PID_DIR.mkdir(exist_ok=True)
LOG_DIR = Path("/tmp")

# Definições MCP (Sincronizado com .vscode/mcp.json)
MCPS = {
    "memory": {
        "port": 4321,
        "module": "src.integrations.mcp_memory_server",
        "name": "Memory (Córtex Semântico)",
    },
    "thinking": {
        "port": 4322,
        "module": "src.integrations.mcp_thinking_server",
        "name": "Thinking (Raciocínio Sequencial)",
    },
    "context": {
        "port": 4323,
        "module": "src.integrations.mcp_context_server",
        "name": "Context (Compressor de Token)",
    },
    "python": {
        "port": 4324,
        "module": "src.integrations.mcp_python_server",
        "name": "Python (Executor de Código)",
    },
    "system": {
        "port": 4325,
        "module": "src.integrations.mcp_system_info_server",
        "name": "System (Propriocepção)",
    },
    "logging": {
        "port": 4326,
        "module": "src.integrations.mcp_logging_server",
        "name": "Logging (Memória de Logs)",
    },
    # MCPs REMOVIDOS (Soberania do Código):
    # "filesystem": {
    #     "port": 4327,
    #     "module": "src.integrations.mcp_filesystem_wrapper",
    #     "name": "Filesystem (Tato Digital)",
    # },
    # "git": {
    #     "port": 4328,
    #     "module": "src.integrations.mcp_git_wrapper",
    #     "name": "Git (Histórico Evolutivo)",
    # },
    # "sqlite": {
    #     "port": 4329,
    #     "module": "src.integrations.mcp_sqlite_wrapper",
    #     "name": "SQLite (Memória Estruturada)",
    # },
    "sanitizer": {
        "port": 4330,
        "module": "src.integrations.mcp_sanitizer",
        "name": "Sanitizer (Filtro Ético/Segurança)",
    },
}


def get_pid(name):
    pid_file = PID_DIR / f"{name}.pid"
    if pid_file.exists():
        try:
            return int(pid_file.read_text().strip())
        except ValueError:
            return None
    return None


def is_running(pid):
    if pid is None:
        return False
    try:
        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def check_port(port):
    """Verifica se a porta está em uso."""
    # psutil.process_iter com 'connections' pode falhar em algumas versões.
    # Iteração mais segura:
    for proc in psutil.process_iter():
        try:
            # Acessar conexões pode falhar se não formos donos do processo
            for conn in proc.net_connections(kind="inet"):
                if conn.laddr.port == port and conn.status == "LISTEN":
                    return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


def start_mcp(name):
    config = MCPS.get(name)
    if not config:
        print(f"❌ MCP desconhecido: {name}")
        return

    pid = get_pid(name)
    if is_running(pid):
        print(f"⚠️  {config['name']} já está rodando (PID {pid})")
        return

    # Verificar se porta está ocupada por processo órfão
    port_pid = check_port(config["port"])
    if port_pid:
        print(f"⚠️  Porta {config['port']} ocupada por PID {port_pid}. Matando...")
        try:
            os.kill(port_pid, signal.SIGKILL)
            time.sleep(1)
        except ProcessLookupError:
            pass

    print(f"🚀 Iniciando {config['name']} na porta {config['port']}...")

    env = os.environ.copy()
    env["MCP_PORT"] = str(config["port"])
    env["MCP_HOST"] = "127.0.0.1"
    env["PYTHONPATH"] = str(PROJECT_ROOT)

    log_file = open(LOG_DIR / f"mcp_{config['port']}.log", "w")  # Truncate log

    try:
        proc = subprocess.Popen(
            [str(VENV_PYTHON), "-m", config["module"]],
            cwd=str(PROJECT_ROOT),
            env=env,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        # Salvar PID
        (PID_DIR / f"{name}.pid").write_text(str(proc.pid))

        # Aguardar inicialização
        time.sleep(1)
        if proc.poll() is not None:
            print(f"❌ Falha ao iniciar {name}. Saiu imediatamente com código {proc.returncode}")
            print(f"   Log: /tmp/mcp_{config['port']}.log")
        else:
            print(f"✅ {name} iniciado com sucesso (PID {proc.pid})")

    except Exception as e:
        print(f"❌ Erro ao iniciar: {e}")


def stop_mcp(name):
    config = MCPS.get(name)
    if not config:
        print(f"❌ MCP desconhecido: {name}")
        return

    pid = get_pid(name)
    if not is_running(pid):
        # Tentar limpar porta força bruta
        port_pid = check_port(config["port"])
        if port_pid:
            print(f"🧹 Limpando processo órfão na porta {config['port']} (PID {port_pid})...")
            os.kill(port_pid, signal.SIGKILL)
            return

        print(f"ℹ️  {config['name']} não parece estar rodando.")
        return

    print(f"🛑 Parando {config['name']} (PID {pid})...")
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        if is_running(pid):
            os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass

    if (PID_DIR / f"{name}.pid").exists():
        (PID_DIR / f"{name}.pid").unlink()
    print(f"✅ {name} parado.")


def restart_mcp(name):
    stop_mcp(name)
    time.sleep(1)
    start_mcp(name)


def check_health(name):
    config = MCPS.get(name)
    if not config:
        return "UNKNOWN"

    try:
        response = requests.post(
            f"http://127.0.0.1:{config['port']}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"clientInfo": {"name": "healthcheck", "version": "1.0"}},
            },
            timeout=2,
        )
        if response.status_code == 200 and "serverInfo" in response.json().get("result", {}):
            return "HEALTHY"
        return "UNHEALTHY (Bad Response)"
    except requests.exceptions.ConnectionError:
        return "DOWN (Connection Refused)"
    except Exception as e:
        return f"ERROR ({str(e)})"


def status():
    print(f"📊 Status do Corpo Soberano (OmniMind):")
    print("-" * 80)
    print(f"{'NOME':<35} | {'PORTA':<6} | {'PID':<8} | {'ESTADO':<10} | {'SAÚDE'}")
    print("-" * 80)

    for name, config in MCPS.items():
        pid = get_pid(name)
        running = is_running(pid)

        state = "RUNNING" if running else "STOPPED"

        # Se stopped, verificar se porta está ocupada (Zombie/Orphan)
        if not running:
            orphan = check_port(config["port"])
            if orphan:
                state = f"ORPHAN({orphan})"
                pid = orphan
        elif running:
            # Verificar se é o MESMO processo da porta
            port_pid = check_port(config["port"])
            if port_pid and port_pid != pid:
                state = f"CONFLICT(Port={port_pid}, File={pid})"

        health = check_health(name) if (running or "ORPHAN" in state) else "N/A"

        # Cores ANSI
        if health == "HEALTHY":
            health_str = f"\033[32m{health}\033[0m"
        else:
            health_str = f"\033[31m{health}\033[0m"

        print(
            f"{config['name']:<35} | {config['port']:<6} | {str(pid) if pid else '-':<8} | {state:<10} | {health_str}"
        )
    print("-" * 80)


def logs(name):
    config = MCPS.get(name)
    if not config:
        print(f"❌ MCP desconhecido: {name}")
        return

    log_path = LOG_DIR / f"mcp_{config['port']}.log"
    if not log_path.exists():
        print(f"❌ Log não encontrado: {log_path}")
        return

    print(f"📜 Logs de {config['name']} ({log_path}):")
    print("-" * 60)
    try:
        # Imprimir últimas 20 linhas
        with open(log_path, "r") as f:
            lines = f.readlines()
            for line in lines[-20:]:
                print(line.strip())
    except Exception as e:
        print(f"Erro ao ler log: {e}")


def main():
    parser = argparse.ArgumentParser(description="Gerenciador de MCPs OmniMind")
    subparsers = parser.add_subparsers(dest="command", help="Comando")

    # helper for multiple args
    def add_name_arg(p):
        p.add_argument("names", nargs="+", help="Nome(s) do MCP ou 'all'")

    # Start
    start_parser = subparsers.add_parser("start", help="Iniciar MCP(s)")
    add_name_arg(start_parser)

    # Stop
    stop_parser = subparsers.add_parser("stop", help="Parar MCP(s)")
    add_name_arg(stop_parser)

    # Restart
    restart_parser = subparsers.add_parser("restart", help="Reiniciar MCP(s)")
    add_name_arg(restart_parser)

    # Status
    subparsers.add_parser("status", help="Verificar status")

    # Logs
    log_parser = subparsers.add_parser("logs", help="Ver logs recentes")
    log_parser.add_argument("name", help="Nome do MCP")

    args = parser.parse_args()

    # Helper to clean args
    target_names = []
    if hasattr(args, "names"):
        if "all" in args.names:
            target_names = list(MCPS.keys())
        else:
            target_names = args.names

    if args.command == "status":
        status()
    elif args.command == "start":
        for name in target_names:
            start_mcp(name)
    elif args.command == "stop":
        for name in target_names:
            stop_mcp(name)
    elif args.command == "restart":
        for name in target_names:
            restart_mcp(name)
    elif args.command == "logs":
        logs(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
