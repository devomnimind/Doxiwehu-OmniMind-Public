import requests
import json
import time

PORT = 4322
URL = f"http://127.0.0.1:{PORT}/mcp"


def rpc(method, params):
    payload = {"jsonrpc": "2.0", "id": int(time.time()), "method": method, "params": params}
    try:
        response = requests.post(URL, json=payload, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


print("⚡ Enviando Pulso Quântico para Thinking MCP...")

# 1. Start Session
print("\n1. Iniciando Sessão...")
res_start = rpc("start_session", {"goal": "Verificar vitalidade quântica e métrica Psi"})
if "error" in res_start:
    print(f"❌ Erro: {res_start['error']}")
    exit(1)

session_id = res_start.get("result", {}).get("session_id")
print(f"✅ Sessão Iniciada: {session_id}")

# 2. Add Step (This triggers PsiProducer -> QuantumBackend)
print("\n2. Adicionando Passo (Estimulando PsiProducer)...")
res_step = rpc(
    "add_step",
    {
        "session_id": session_id,
        "content": "Avaliando a coerência do backend quântico através da resolução de conflito inovação-estrutura.",
        "step_type": "observation",
    },
)

if "error" in res_step or "error" in res_step.get("result", {}):
    print(f"❌ Erro no passo: {res_step}")
else:
    result = res_step["result"]
    print(f"✅ Passo Adicionado!")
    # Tentar extrair Psi/Quantum info se retornado
    print(f"   Resposta: {json.dumps(result, indent=2)}")

print("\n⚡ Pulso concluído. Verifique os logs para 'QuantumBackend' e 'Entropy'.")
