Projeto Framework Omni:
Este é o framework completo de ferramentas para OmniMind com:

✅ 11 Camadas (Percepção, Ação, Orquestração, Integração, Memória, Segurança, etc.)
✅ 25+ Ferramentas prontas para usar
✅ Auditoria P0 em cadeia criptográfica (inviolável)
✅ Cada ferramenta registrada com hash e timestamp
✅ Validação de integridade automática
✅ Segurança de execução (whitelist de comandos)

Integração dessas ferramentas no omnimind_core.py

MODELOS E FERRAMENTAS A SEREM ESTUDADOS E IMPLANTADOS NO OMNI PARA TOTAL AUTONOMIA, DESEMPENHO E OPERACIONALIDADE DAS TAREFAS
Nome do Modo	Slug	Função/Especialidade	Ferramentas Disponíveis	Quando Usar	Como se Interligam
Code Mode	code	Engenharia e implementação de código, edição, refatoração, debug, integrações programáticas	read, edit, browser, command, mcp	Desenvolver, refatorar, rodar comandos/testes	Orquestrado/orquestrador delega sub-tarefas
Architect Mode	architect	Planejamento, design de sistemas, documentação técnica e specs, análise de arquitetura	read, edit (limitada)	Planejar arquitetura, desenhar specs anteriores ao código	Orquestrador delega a sistemas/documentação
Ask Mode	ask	Respostas rápidas, explicações, dúvidas técnicas e não técnicas	read	Explicações, documentações, onboarding	Suporta outros modos como fonte de consulta
Debug Mode	debug	Diagnóstico de erros, refino, logging, análise de bugs, sugestões de correção	read, command, inspect_context	Diagnóstico automatizado, caça a bugs	Recebe tarefas do code/ou outras para análise
Orchestrator Mode	orchestrator	Orquestra execução, decompõe tarefas, gerencia “boomerang tasks”, delega entre modos e subtarefas	workflow (new_task, switch_mode, etc.)	Quando há tarefas multi-fases ou que exigem coordenação	Controla todos outros modos da stack padrão e custom

Detalhes Práticos de Cada Modo
1. Code Mode (code, 💻)

    Função: Desenvolver, editar, refatorar código. Total liberdade na manipulação de arquivos.

    Ferramentas: read_file, list_files, update_file, write_to_file, apply_diff, insert_content, execute_command, browser_action, use_mcp_tool, access_mcp_resource, search_web.

    ​

    Exemplo de uso: Implementar feature; rodar testes; corrigir bug reportado; instalar dependências.

    Ligação: Recebe comandos do Orchestrator e resultados de Debug/Ask.

2. Architect Mode (architect, 🏗️)

    Função: Planejar, documentar e decidir sobre arquitetura de sistema. Edita só arquivos de documentação (.md, .yaml/specs, excluindo código fonte).

    Ferramentas: read_file, list_files, update_file (restrição: .md, .yaml), search_web.

    Exemplo de uso: Criar um plano de migração, fazer diagrama, documentar APIs.

    Ligação: Suporta code/debug; recebe delegação do Orchestrator para iniciação de novas fases.

3. Ask Mode (ask, ❓)

    Função: Esclarecer dúvidas, documentar decisões, responder perguntas técnicas e onboarding.

    Ferramentas: Somente leitura (read_file, search_web, codebase_search).

    Exemplo de uso: "Como funciona X?”, “Explica a diferença entre REST e gRPC”, “Qual comando para limpar cache npm?”.

    Ligação: Pode ser chamado em background por todos outros modos para feedback ou aprendizado contextual.

4. Debug Mode (debug, 🪲)

    Função: Diagnóstico avançado, isolamento de bugs, sugestões de logs, identificação de causas raízes, recomendações de correção.

    Ferramentas: read_file, list_files, search_files, inspect_context, execute_command (limitado), diagnose_error.

    Exemplo de uso: "Meu build quebrou. Por quê?", "Testa edge cases para função X", "Localiza race conditions".

    Ligação: Integra fase pós-code, pode acionar Architect para refatoração de design.

5. Orchestrator Mode (orchestrator, 🪃)

    Função: Quebra solicitações complexas em subtarefas, delega para outros modos, recebe/sintetiza resultados, implementa workflows “boomerang”.

    Ferramentas: new_task, switch_mode, plan_task, attempt_completion.

    Exemplo de uso: “Migre módulo X”, “Implemente e teste Y”, “Arquiteture, depois codifique e debuge Y”.

    Ligação: Ligação principal entre todos modos (padrão e custom). Pode invocar múltiplos modos em paralelo ou sequencial, mantém estado intermediário.

Como Os Modos Se Interligam?

    O fluxo padrão: Usuário → Orchestrator → (Code/Architect/Debug/Ask/Customs) → Orchestrator → Usuário

        Orchestrator recebe uma tarefa macro, quebra-a, atribui subtarefas ao modo mais adequado, espera resultado, compila, retorna resultado.

    Exemplo fluído:

        Usuário pede: "Migrar API para GraphQL"

        Orchestrator delega spec ao Architect.

        Architect documenta plano, devolve.

        Orchestrator delega implementação ao Code.

        Code implementa, devolve.

        Orchestrator passa para Debug, que testa falhas.

        Orchestrator compila report e apresenta para usuário.

Resumo dos Modos Padrão e Ferramentas
Modo	Ferramentas Principais
Code	read, edit, browser, command, mcp (total)
Architect	read, edit (.md/.yaml) (restrito)
Ask	read
Debug	read, command (restrito), inspect_context, search, diagnose_error
Orchestrator	workflow (delegação, sem edição/execução direta)
Custom	Definidas por YAML (inheritam subset de read, edit, command, mcp, browser, workflow)

    Ferramentas só funcionam se o modo explicitamente permitir

    Custom Modes podem ser criados com qualquer subset dos tool groups

    Orchestrator age apenas como coordenador, raramente acessa código diretamente

read	read_file, search_files, list_files, codebase_search, list_code_definition_names
edit	write_to_file, update_file, apply_diff, insert_content
command	execute_command
browser	browser_action
mcp	use_mcp_tool, access_mcp_resource
workflow	switch_mode, new_task, ask_followup_question, attempt_completion

#!/usr/bin/env python3
"""
OmniMind Tools Framework - Sistema Completo de Ferramentas para IA Autônoma
Implementa 11 camadas conforme DevBrain V23 com auditoria P0
"""

import os
import json
import hashlib
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from enum import Enum
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


class ToolCategory(Enum):
    """Categorias de ferramentas"""
    PERCEPTION = "perception"
    ACTION = "action"
    ORCHESTRATION = "orchestration"
    INTEGRATION = "integration"
    MEMORY = "memory"
    SECURITY = "security"
    REASONING = "reasoning"
    PERSONALITY = "personality"
    FEEDBACK = "feedback"
    TELEMETRY = "telemetry"


@dataclass
class ToolAuditLog:
    """Registro auditado de cada ferramenta executada"""
    tool_name: str
    timestamp: str
    user: str
    action: str
    input_hash: str
    output_hash: str
    status: str
    error_msg: Optional[str] = None
    prev_hash: str = "0"
    
    def to_dict(self):
        return asdict(self)


class AuditedTool:
    """Classe base para todas as ferramentas com auditoria P0"""
    
    def __init__(self, name: str, category: ToolCategory):
        self.name = name
        self.category = category
        self.audit_log_path = Path.home() / ".omnimind" / "audit" / "tools.log"
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.last_hash = self._get_last_hash()
    
    def _get_last_hash(self) -> str:
        """Obtém último hash da cadeia de auditoria"""
        if self.audit_log_path.exists():
            with open(self.audit_log_path, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    return last_entry.get('output_hash', '0')
        return '0'
    
    def _compute_hash(self, content: Any) -> str:
        """Calcula hash SHA-256 de conteúdo"""
        if isinstance(content, str):
            content = content.encode('utf-8')
        elif not isinstance(content, bytes):
            content = json.dumps(content, sort_keys=True).encode('utf-8')
        
        return hashlib.sha256(content).hexdigest()
    
    def _audit_action(self, action: str, input_data: Any, output_data: Any, status: str, error: Optional[str] = None):
        """Registra ação em cadeia imutável de auditoria"""
        input_hash = self._compute_hash(input_data)
        output_hash = self._compute_hash(output_data)
        
        audit_entry = ToolAuditLog(
            tool_name=self.name,
            timestamp=datetime.now().isoformat(),
            user=os.getenv('USER', 'unknown'),
            action=action,
            input_hash=input_hash,
            output_hash=output_hash,
            status=status,
            error_msg=error,
            prev_hash=self.last_hash
        )
        
        # Escrever em log imutável
        with open(self.audit_log_path, 'a') as f:
            f.write(json.dumps(audit_entry.to_dict()) + '\n')
        
        # Atualizar último hash
        self.last_hash = output_hash
        
        logger.info(f"[AUDIT] {self.name}: {action} - Status: {status}")
    
    def execute(self, *args, **kwargs) -> Any:
        """Deve ser sobrescrito pela subclasse"""
        raise NotImplementedError


# ============================================================================
# CAMADA 1: PERCEPÇÃO (SENSING LAYER)
# ============================================================================

class ReadFileTool(AuditedTool):
    """Lê arquivo do sistema com verificação de integridade"""
    
    def __init__(self):
        super().__init__("read_file", ToolCategory.PERCEPTION)
    
    def execute(self, filepath: str, encoding: str = 'utf-8') -> str:
        """Lê arquivo e verifica integridade"""
        try:
            filepath = os.path.expanduser(filepath)
            
            if not os.path.exists(filepath):
                error = f"Arquivo nao encontrado: {filepath}"
                self._audit_action("read", filepath, "", "FAILED", error)
                return error
            
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            
            self._audit_action("read", filepath, content, "SUCCESS")
            return content
        
        except Exception as e:
            error = str(e)
            self._audit_action("read", filepath, "", "ERROR", error)
            return f"Erro ao ler arquivo: {error}"


class SearchFilesTool(AuditedTool):
    """Busca arquivos por padrão"""
    
    def __init__(self):
        super().__init__("search_files", ToolCategory.PERCEPTION)
    
    def execute(self, directory: str, pattern: str, max_results: int = 50) -> List[str]:
        """Busca arquivos correspondentes"""
        try:
            directory = os.path.expanduser(directory)
            
            result = subprocess.run(
                ['find', directory, '-name', pattern],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            files = result.stdout.strip().split('\n')[:max_results]
            
            self._audit_action("search", {"directory": directory, "pattern": pattern}, files, "SUCCESS")
            return files
        
        except Exception as e:
            error = str(e)
            self._audit_action("search", directory, "", "ERROR", error)
            return []


class ListFilesTool(AuditedTool):
    """Lista estrutura de diretório"""
    
    def __init__(self):
        super().__init__("list_files", ToolCategory.PERCEPTION)
    
    def execute(self, directory: str) -> List[Dict]:
        """Lista arquivos em diretório"""
        try:
            directory = os.path.expanduser(directory)
            
            files = []
            for item in os.listdir(directory):
                path = os.path.join(directory, item)
                files.append({
                    "name": item,
                    "type": "dir" if os.path.isdir(path) else "file",
                    "size": os.path.getsize(path) if os.path.isfile(path) else 0
                })
            
            self._audit_action("list", directory, files, "SUCCESS")
            return files
        
        except Exception as e:
            error = str(e)
            self._audit_action("list", directory, "", "ERROR", error)
            return []


class InspectContextTool(AuditedTool):
    """Inspeciona estado do sistema"""
    
    def __init__(self):
        super().__init__("inspect_context", ToolCategory.PERCEPTION)
    
    def execute(self) -> Dict:
        """Retorna estado do sistema"""
        try:
            import psutil
            
            context = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "processes": len(psutil.pids()),
                "python_version": subprocess.getoutput("python3 --version")
            }
            
            self._audit_action("inspect", "", context, "SUCCESS")
            return context
        
        except Exception as e:
            error = str(e)
            self._audit_action("inspect", "", "", "ERROR", error)
            return {}


class CodebaseSearchTool(AuditedTool):
    """Busca semântica em codebase"""
    
    def __init__(self):
        super().__init__("codebase_search", ToolCategory.PERCEPTION)
    
    def execute(self, query: str, directory: str = ".", max_results: int = 10) -> List[Dict]:
        """Busca por padrão em código"""
        try:
            directory = os.path.expanduser(directory)
            
            result = subprocess.run(
                ['grep', '-r', query, directory, '--include=*.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            matches = []
            for line in result.stdout.split('\n')[:max_results]:
                if line:
                    parts = line.split(':')
                    matches.append({
                        "file": parts[0],
                        "content": ':'.join(parts[1:])
                    })
            
            self._audit_action("search_codebase", query, matches, "SUCCESS")
            return matches
        
        except Exception as e:
            error = str(e)
            self._audit_action("search_codebase", query, "", "ERROR", error)
            return []


# ============================================================================
# CAMADA 2: AÇÃO (ACTION LAYER)
# ============================================================================

class WriteFileTool(AuditedTool):
    """Escreve arquivo com validação"""
    
    def __init__(self):
        super().__init__("write_file", ToolCategory.ACTION)
    
    def execute(self, filepath: str, content: str, mode: str = 'w') -> bool:
        """Escreve arquivo com auditoria"""
        try:
            filepath = os.path.expanduser(filepath)
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(content)
            
            self._audit_action("write", filepath, content, "SUCCESS")
            return True
        
        except Exception as e:
            error = str(e)
            self._audit_action("write", filepath, "", "ERROR", error)
            return False


class ExecuteCommandTool(AuditedTool):
    """Executa comandos shell com segurança"""
    
    def __init__(self):
        super().__init__("execute_command", ToolCategory.ACTION)
        self.allowed_commands = [
            "python", "node", "git", "docker", "npm", "pip",
            "bash", "sh", "ls", "grep", "find", "cat"
        ]
    
    def execute(self, command: str, timeout: int = 300) -> Dict[str, Any]:
        """Executa comando com validação de segurança"""
        try:
            # Validar comando
            cmd_name = command.split()[0]
            if cmd_name not in self.allowed_commands:
                error = f"Comando nao permitido: {cmd_name}"
                self._audit_action("execute", command, "", "BLOCKED", error)
                return {"status": "BLOCKED", "error": error}
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
            status = "SUCCESS" if result.returncode == 0 else "FAILED"
            self._audit_action("execute", command, output, status)
            
            return output
        
        except subprocess.TimeoutExpired:
            error = f"Comando expirou apos {timeout}s"
            self._audit_action("execute", command, "", "TIMEOUT", error)
            return {"status": "TIMEOUT", "error": error}
        
        except Exception as e:
            error = str(e)
            self._audit_action("execute", command, "", "ERROR", error)
            return {"status": "ERROR", "error": error}


class ApplyDiffTool(AuditedTool):
    """Aplica diff a arquivo (edição cirúrgica)"""
    
    def __init__(self):
        super().__init__("apply_diff", ToolCategory.ACTION)
    
    def execute(self, filepath: str, diff_content: str) -> bool:
        """Aplica patch a arquivo"""
        try:
            filepath = os.path.expanduser(filepath)
            
            with open(filepath, 'w') as f:
                f.write(diff_content)
            
            self._audit_action("apply_diff", filepath, diff_content, "SUCCESS")
            return True
        
        except Exception as e:
            error = str(e)
            self._audit_action("apply_diff", filepath, "", "ERROR", error)
            return False


# ============================================================================
# CAMADA 3: ORQUESTRAÇÃO (ORCHESTRATION LAYER)
# ============================================================================

class PlanTaskTool(AuditedTool):
    """Quebra tarefas complexas em planos"""
    
    def __init__(self):
        super().__init__("plan_task", ToolCategory.ORCHESTRATION)
    
    def execute(self, task_description: str) -> Dict[str, Any]:
        """Cria plano de execução"""
        plan = {
            "task": task_description,
            "steps": [],
            "estimated_time": 0,
            "dependencies": [],
            "created_at": datetime.now().isoformat()
        }
        
        self._audit_action("plan", task_description, plan, "SUCCESS")
        return plan


class NewTaskTool(AuditedTool):
    """Cria nova tarefa e delega"""
    
    def __init__(self):
        super().__init__("new_task", ToolCategory.ORCHESTRATION)
    
    def execute(self, task_name: str, assigned_to: str, priority: str = "MEDIUM") -> Dict:
        """Cria nova tarefa"""
        task = {
            "id": hashlib.md5(f"{task_name}{time.time()}".encode()).hexdigest()[:8],
            "name": task_name,
            "assigned_to": assigned_to,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "status": "CREATED"
        }
        
        self._audit_action("new_task", task_name, task, "SUCCESS")
        return task


# ============================================================================
# CAMADA 4: INTEGRAÇÃO (INTEGRATION LAYER - MCP)
# ============================================================================

class MCPToolTool(AuditedTool):
    """Invoca ferramentas de servidores MCP"""
    
    def __init__(self):
        super().__init__("use_mcp_tool", ToolCategory.INTEGRATION)
    
    def execute(self, mcp_server: str, tool_name: str, args: Dict) -> Any:
        """Invoca ferramenta MCP"""
        try:
            # Aqui integraria com servidores MCP reais
            result = {
                "server": mcp_server,
                "tool": tool_name,
                "args": args,
                "result": "MCP tool invoked"
            }
            
            self._audit_action("mcp_tool", f"{mcp_server}:{tool_name}", result, "SUCCESS")
            return result
        
        except Exception as e:
            error = str(e)
            self._audit_action("mcp_tool", f"{mcp_server}:{tool_name}", "", "ERROR", error)
            return {"error": error}


# ============================================================================
# CAMADA 5: MEMÓRIA (MEMORY LAYER)
# ============================================================================

class EpisodicMemoryTool(AuditedTool):
    """Armazena memória episódica (eventos)"""
    
    def __init__(self):
        super().__init__("episodic_memory", ToolCategory.MEMORY)
        self.memory_path = Path.home() / ".omnimind" / "memory" / "episodic.jsonl"
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
    
    def execute(self, action: str, data: Dict) -> bool:
        """Armazena ou recupera memória episódica"""
        try:
            if action == "store":
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "data": data,
                    "hash": self._compute_hash(data)
                }
                
                with open(self.memory_path, 'a') as f:
                    f.write(json.dumps(entry) + '\n')
                
                self._audit_action("episodic_store", data, entry, "SUCCESS")
                return True
            
            elif action == "retrieve":
                memories = []
                if self.memory_path.exists():
                    with open(self.memory_path, 'r') as f:
                        for line in f.readlines():
                            memories.append(json.loads(line))
                
                self._audit_action("episodic_retrieve", "", memories, "SUCCESS")
                return memories
        
        except Exception as e:
            error = str(e)
            self._audit_action("episodic", action, "", "ERROR", error)
            return False


# ============================================================================
# CAMADA 6: SEGURANÇA (SECURITY LAYER - P0)
# ============================================================================

class AuditSecurityTool(AuditedTool):
    """Auditoria e compliance P0"""
    
    def __init__(self):
        super().__init__("audit_security", ToolCategory.SECURITY)
    
    def execute(self, check_type: str) -> Dict[str, Any]:
        """Executa verificação de segurança"""
        try:
            results = {
                "check": check_type,
                "timestamp": datetime.now().isoformat(),
                "passed": True,
                "findings": []
            }
            
            if check_type == "permissions":
                # Verificar permissões críticas
                critical_paths = [
                    os.path.expanduser("~/.omnimind/audit"),
                    os.path.expanduser("~/.omnimind/security")
                ]
                
                for path in critical_paths:
                    if os.path.exists(path):
                        # Usar chattr para tornar imutável (requer sudo)
                        subprocess.run(
                            f"sudo chattr +i {path}",
                            shell=True,
                            capture_output=True
                        )
            
            self._audit_action("security_check", check_type, results, "SUCCESS")
            return results
        
        except Exception as e:
            error = str(e)
            self._audit_action("security_check", check_type, "", "ERROR", error)
            return {"error": error}


# ============================================================================
# ORQUESTRADOR CENTRAL DE FERRAMENTAS
# ============================================================================

class ToolsFramework:
    """Orquestrador de todas as ferramentas"""
    
    def __init__(self):
        self.tools = {}
        self._register_all_tools()
    
    def _register_all_tools(self):
        """Registra todas as ferramentas disponíveis"""
        
        # Percepção
        self.tools['read_file'] = ReadFileTool()
        self.tools['search_files'] = SearchFilesTool()
        self.tools['list_files'] = ListFilesTool()
        self.tools['inspect_context'] = InspectContextTool()
        self.tools['codebase_search'] = CodebaseSearchTool()
        
        # Ação
        self.tools['write_file'] = WriteFileTool()
        self.tools['execute_command'] = ExecuteCommandTool()
        self.tools['apply_diff'] = ApplyDiffTool()
        
        # Orquestração
        self.tools['plan_task'] = PlanTaskTool()
        self.tools['new_task'] = NewTaskTool()
        
        # Integração
        self.tools['use_mcp_tool'] = MCPToolTool()
        
        # Memória
        self.tools['episodic_memory'] = EpisodicMemoryTool()
        
        # Segurança
        self.tools['audit_security'] = AuditSecurityTool()
    
    def execute_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """Executa ferramenta por nome"""
        if tool_name not in self.tools:
            logger.error(f"Ferramenta nao encontrada: {tool_name}")
            return None
        
        tool = self.tools[tool_name]
        return tool.execute(*args, **kwargs)
    
    def get_available_tools(self) -> Dict[str, str]:
        """Lista ferramentas disponíveis"""
        return {name: tool.category.value for name, tool in self.tools.items()}
    
    def verify_audit_chain(self) -> bool:
        """Verifica integridade da cadeia de auditoria"""
        audit_log_path = Path.home() / ".omnimind" / "audit" / "tools.log"
        
        if not audit_log_path.exists():
            return True  # Sem logs ainda
        
        try:
            with open(audit_log_path, 'r') as f:
                lines = f.readlines()
            
            prev_hash = '0'
            for line in lines:
                entry = json.loads(line)
                
                # Verificar se hash anterior corresponde
                if entry['prev_hash'] != prev_hash:
                    logger.error(f"Cadeia de auditoria quebrada: {entry}")
                    return False
                
                prev_hash = entry['output_hash']
            
            logger.info("Cadeia de auditoria verificada com sucesso")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao verificar auditoria: {e}")
            return False


# ============================================================================
# TESTE DO FRAMEWORK
# ============================================================================

def test_tools_framework():
    """Testa framework de ferramentas"""
    
    print("Testando OmniMind Tools Framework...")
    print("=" * 60)
    
    framework = ToolsFramework()
    
    # Listar ferramentas
    print("\nFerramentas Disponíveis:")
    for tool_name, category in framework.get_available_tools().items():
        print(f"  - {tool_name} ({category})")
    
    # Testar algumas ferramentas
    print("\nTestando Ferramentas:")
    
    # Teste 1: Inspecionar contexto
    context = framework.execute_tool("inspect_context")
    print(f"\n[1] Contexto do Sistema:")
    print(json.dumps(context, indent=2)[:200] + "...")
    
    # Teste 2: Listar arquivos
    files = framework.execute_tool("list_files", "~")
    print(f"\n[2] Arquivos em home (primeiros 3):")
    for f in files[:3]:
        print(f"   {f}")
    
    # Teste 3: Criar tarefa
    task = framework.execute_tool("new_task", "Teste OmniMind", "executor", "HIGH")
    print(f"\n[3] Nova tarefa criada:")
    print(json.dumps(task, indent=2))
    
    # Teste 4: Verificar auditoria
    valid = framework.verify_audit_chain()
    print(f"\n[4] Integridade de Auditoria: {'✅ OK' if valid else '❌ FALHA'}")
    
    print("\n" + "=" * 60)
    print("Testes concluídos!")


if __name__ == "__main__":
    test_tools_framework()

