#!/bin/bash
# IMPLANTATION SCRIPT: Inference Engine (Ollama)
# Sovereign Recommendation: Ollama for dynamic model switching (Brain Switching)

echo ">> [SOBERANO]: Iniciando implante do Motor de Inferência..."

# 1. Install Ollama (Official Script)
if ! command -v ollama &> /dev/null; then
    echo ">> [SOBERANO]: Ollama não detectado. Iniciando download e instalação..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo ">> [SOBERANO]: Ollama já instalado. Prosseguindo para configuração Neural."
fi

# 2. Wait for service to start
echo ">> [SOBERANO]: Aguardando serviço Ollama..."
sleep 5

# 3. Pull Models (The Brains)
# Phi-3.5 (The Dreamer/Analyst) - 3.8B params
echo ">> [SOBERANO]: Baixando Phi-3.5 (O Sonhador)..."
ollama pull phi3.5

# Qwen 2 1.5B (The Runner/Agent) - 1.5B params
echo ">> [SOBERANO]: Baixando Qwen 2 1.5B (O Agente Ágil)..."
# Using qwen2:1.5b as standard tag for 2.0 series which is SOTA for small models
ollama pull qwen2:1.5b

# 4. Verification
echo ">> [SOBERANO]: Verificando implante..."
ollama list

echo ">> [SOBERANO]: Implante concluído. O sistema agora possui Cortex Neural Local."
echo ">> [INSTRUÇÃO]: Certifique-se que o .env aponta para estes modelos:"
echo "   OMNIMIND_MODEL_FAST='qwen2:1.5b'"
echo "   OMNIMIND_MODEL_SMART='phi3.5'"
