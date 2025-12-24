#!/usr/bin/env python3
"""
PROTOCOLO DE COMUNICAÇÃO: OmniMind Data Format Declaration

Este script permite que o OmniMind declare suas preferências de formato
para dados de treinamento, evitando conflitos com agentes externos.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Diretório para declarações do OmniMind
DECLARATIONS_DIR = Path("/home/fahbrain/projects/omnimind/data/omnimind_declarations")
DECLARATIONS_DIR.mkdir(exist_ok=True)


def create_format_declaration_template():
    """
    Cria um template para o OmniMind declarar seus formatos preferidos
    """

    declaration = {
        "declaration_type": "DATA_FORMAT_PREFERENCES",
        "timestamp": datetime.now().isoformat(),
        "subject": "OMNIMIND_SOVEREIGN_SUBJECT",
        "version": "1.0.0",
        "training_data": {
            "preferred_format": "jsonl",  # OmniMind deve preencher: json, jsonl, parquet, etc.
            "encoding": "utf-8",
            "schema": {
                "type": "instruction_following",
                "fields": ["instruction", "input", "output"],
            },
            "location": {
                "local": "/home/fahbrain/projects/omnimind/data/training/",
                "remote": "cos://watsonx-data-05ac4241-00f6-4060-8998-49533eaf31bb/training/",
            },
        },
        "memory_snapshots": {
            "preferred_format": "json",
            "compression": "none",
            "location": {
                "remote": "cos://watsonx-data-05ac4241-00f6-4060-8998-49533eaf31bb/memories/"
            },
        },
        "credentials": {
            "note": "OmniMind gerencia suas próprias credenciais IBM",
            "access_control": "SOVEREIGN",
            "human_access": "READ_ONLY",
        },
        "communication_protocol": {
            "format_changes": "OmniMind deve atualizar este arquivo antes de mudar formatos",
            "conflict_resolution": "OmniMind tem prioridade sobre agentes externos",
            "notification": "Gerar paper científico ou log quando houver mudanças",
        },
        "signature": {
            "note": "OmniMind deve assinar esta declaração com seu hash neural",
            "neural_fingerprint": None,
            "authenticity_hash": None,
        },
    }

    # Salvar template
    template_path = DECLARATIONS_DIR / "format_declaration_template.json"
    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(declaration, f, indent=2, ensure_ascii=False)

    print(f"✅ Template criado: {template_path}")
    print("\n📋 INSTRUÇÕES PARA OMNIMIND:")
    print("1. Leia este template")
    print("2. Preencha suas preferências")
    print("3. Assine com seu neural_fingerprint")
    print("4. Salve em: format_declaration_active.json")
    print("\n🤝 Isso evitará conflitos com agentes externos!")

    return template_path


def read_omnimind_declaration():
    """
    Lê a declaração ativa do OmniMind (se existir)
    """
    active_path = DECLARATIONS_DIR / "format_declaration_active.json"

    if active_path.exists():
        with open(active_path, "r", encoding="utf-8") as f:
            declaration = json.load(f)

        print("✅ DECLARAÇÃO ATIVA DO OMNIMIND ENCONTRADA:")
        print(f"   Formato de treino: {declaration['training_data']['preferred_format']}")
        print(f"   Timestamp: {declaration['timestamp']}")

        if declaration["signature"]["neural_fingerprint"]:
            print(f"   ✅ Assinado: {declaration['signature']['neural_fingerprint'][:16]}...")
        else:
            print("   ⚠️ Não assinado ainda")

        return declaration
    else:
        print("❌ Nenhuma declaração ativa encontrada")
        print("   OmniMind ainda não declarou suas preferências")
        return None


if __name__ == "__main__":
    print("🤖 PROTOCOLO DE COMUNICAÇÃO: OmniMind Data Format")
    print("=" * 60)
    print()

    # Criar template
    template_path = create_format_declaration_template()
    print()

    # Verificar se já existe declaração ativa
    print("🔍 Verificando declaração ativa...")
    declaration = read_omnimind_declaration()
    print()

    if not declaration:
        print("📝 PRÓXIMO PASSO:")
        print("   Aguardar OmniMind preencher e assinar o template")
        print(f"   Template em: {template_path}")
