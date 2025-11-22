#!/usr/bin/env python3
"""
Script para correção automática de issues de segurança.

Este script identifica e corrige automaticamente problemas comuns de segurança:
- Uso de subprocess com shell=True
- Uso de pickle sem validação
- Requests com verify=False
"""

import re
import sys
from pathlib import Path
from typing import Tuple


def fix_subprocess_shell_true(content: str) -> Tuple[str, int]:
    """Remove shell=True de subprocess calls.
    
    Args:
        content: Conteúdo do arquivo
        
    Returns:
        Tuple de (conteúdo modificado, número de alterações)
    """
    pattern = r'subprocess\.run\((.*?),\s*shell=True'
    matches = len(re.findall(pattern, content, flags=re.DOTALL))
    
    if matches > 0:
        replacement = r'subprocess.run(\1, shell=False'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
    return content, matches


def fix_pickle_usage(content: str) -> Tuple[str, int]:
    """Adiciona warnings para uso de pickle.
    
    Args:
        content: Conteúdo do arquivo
        
    Returns:
        Tuple de (conteúdo modificado, número de alterações)
    """
    changes = 0
    
    # Contar usos de pickle.loads
    pickle_loads_count = len(re.findall(r'pickle\.loads\(', content))
    
    if pickle_loads_count > 0 and '# WARNING: pickle usage' not in content:
        # Adicionar warning no topo do arquivo após imports
        lines = content.split('\n')
        import_end = 0
        
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('import') and not line.strip().startswith('from'):
                import_end = i
                break
        
        warning = """
# WARNING: Este arquivo usa pickle que pode ser inseguro para dados não confiáveis.
# Considere usar json.loads() ou implementar validação de dados.
"""
        lines.insert(import_end, warning)
        content = '\n'.join(lines)
        changes = 1
        
    return content, changes


def fix_verify_false(content: str) -> Tuple[str, int]:
    """Corrige verify=False em requests.
    
    Args:
        content: Conteúdo do arquivo
        
    Returns:
        Tuple de (conteúdo modificado, número de alterações)
    """
    pattern = r'requests\.get\((.*?),\s*verify=False\)'
    matches = len(re.findall(pattern, content, flags=re.DOTALL))
    
    if matches > 0:
        # Adicionar comentário explicativo
        replacement = r'# TODO: SECURITY - verify=False desabilita validação SSL\n        requests.get(\1, verify=True)'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
    return content, matches


def process_file(file_path: Path) -> dict:
    """Processa um arquivo Python.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Dict com estatísticas de alterações
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content
        
        stats = {
            'subprocess_shell': 0,
            'pickle_warning': 0,
            'verify_false': 0,
        }
        
        content, stats['subprocess_shell'] = fix_subprocess_shell_true(content)
        content, stats['pickle_warning'] = fix_pickle_usage(content)
        content, stats['verify_false'] = fix_verify_false(content)
        
        total_changes = sum(stats.values())
        
        if content != original and total_changes > 0:
            file_path.write_text(content, encoding='utf-8')
            return stats
        
        return None
        
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return None


def main():
    """Função principal."""
    src_dir = Path('src')
    
    if not src_dir.exists():
        print("❌ Diretório src/ não encontrado")
        sys.exit(1)
    
    print("🔍 Buscando arquivos Python em src/...")
    
    total_files = 0
    fixed_files = 0
    total_stats = {
        'subprocess_shell': 0,
        'pickle_warning': 0,
        'verify_false': 0,
    }
    
    for py_file in src_dir.rglob('*.py'):
        total_files += 1
        stats = process_file(py_file)
        
        if stats:
            fixed_files += 1
            for key, value in stats.items():
                total_stats[key] += value
            
            changes_str = ', '.join([f"{k}: {v}" for k, v in stats.items() if v > 0])
            print(f"✅ Corrigido: {py_file} ({changes_str})")
    
    print("\n" + "="*60)
    print("📊 RESUMO DAS CORREÇÕES")
    print("="*60)
    print(f"Arquivos analisados: {total_files}")
    print(f"Arquivos corrigidos: {fixed_files}")
    print(f"subprocess shell=True removidos: {total_stats['subprocess_shell']}")
    print(f"Warnings pickle adicionados: {total_stats['pickle_warning']}")
    print(f"verify=False corrigidos: {total_stats['verify_false']}")
    print("="*60)
    
    if fixed_files > 0:
        print("\n⚠️  ATENÇÃO: Revise as mudanças manualmente antes de commitar!")
        print("Execute: git diff src/")
        
    return 0 if total_stats['subprocess_shell'] + total_stats['verify_false'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
