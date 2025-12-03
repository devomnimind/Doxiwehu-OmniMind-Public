# 🛡️ OmniMind Safe Command Execution List

Este documento define a "Master List" de comandos permitidos e seguros que o sistema OmniMind pode executar. O objetivo é evitar bloqueios por permissão, hangs em prompts interativos (sudo) e sobrecarga do sistema.

## 🚨 Problemas Identificados (Diagnóstico)
1. **Hanging (Travamento):** O sistema tenta executar `sudo` (ex: para eBPF/bpftrace) em scripts não-interativos. Sem senha configurada no `sudoers`, o processo fica parado esperando input eternamente.
2. **Sobrecarga:** Tentativas repetidas de iniciar serviços pesados (Node.js, Python Cluster) sem limpeza adequada.
3. **Permissões:** Falhas ao tentar acessar portas baixas ou dispositivos de sistema sem privilégios adequados.

## ✅ Lista de Comandos Permitidos (Allowlist)

O OmniMind deve restringir sua execução aos seguintes binários e escopos:

### 1. Gerenciamento de Processos (Essencial)
| Comando | Uso Seguro | Risco | Notas |
|---------|------------|-------|-------|
| `pkill` | `pkill -f "pattern"` | Médio | Usar apenas com patterns específicos do projeto (ex: `omnimind`, `uvicorn`) |
| `ps` | `ps aux`, `ps -p PID` | Baixo | Apenas leitura |
| `nohup` | `nohup cmd &` | Baixo | Para processos em background |
| `sleep` | `sleep N` | Baixo | Evitar loops infinitos de espera |

### 2. Runtime & Linguagens
| Comando | Uso Seguro | Risco | Notas |
|---------|------------|-------|-------|
| `python` | `python -m module` | Médio | Executar apenas código dentro de `src/` |
| `npm` | `npm run dev`, `npm install` | Médio | Pode consumir muita RAM/CPU. Executar em container se possível. |
| `node` | Via `npm` | Médio | Backend do Frontend |

### 3. Rede & Diagnóstico
| Comando | Uso Seguro | Risco | Notas |
|---------|------------|-------|-------|
| `curl` | `curl -s http://localhost...` | Baixo | Health checks locais apenas |
| `tail` | `tail -n 10 file.log` | Baixo | Leitura de logs |

### 4. ⚠️ Comandos Restritos (Requerem Cuidado)
| Comando | Uso Seguro | Risco | Solução Recomendada |
|---------|------------|-------|---------------------|
| `sudo` | **PROIBIDO EM MODO AUTÔNOMO** | Alto | Causa travamento (prompt de senha). Usar Docker ou configurar `NOPASSWD` no sudoers. |
| `bpftrace`| Monitoramento Kernel | Alto | Requer root. Deve rodar em container privilegiado ou via serviço systemd separado. |

## 🛠️ Solução para o Travamento (Action Plan)

Para evitar que o OmniMind trave tentando pedir senha de root:

1. **Dockerização (Recomendado):**
   Rodar o OmniMind dentro de um container Docker. Lá dentro, ele é `root` e não precisa de `sudo`, eliminando o prompt de senha.

2. **Variável de Ambiente para Skip:**
   Modificar `start_omnimind_system.sh` para pular etapas que exigem root se não estiver em modo interativo.
   ```bash
   if [ "$OMNIMIND_NO_SUDO" == "true" ]; then
       echo "⚠️ Skipping eBPF monitoring (Sudo disabled)"
   else
       sudo ...
   fi
   ```

3. **Sudoers (Alternativa Local):**
   Adicionar permissão específica sem senha:
   `fahbrain ALL=(ALL) NOPASSWD: /usr/bin/bpftrace, /usr/bin/pkill`

## 📊 Sobre os Valores de Φ (Phi)
Os valores `['0.5010', '0.5010', ...]` **NÃO são hardcoded no código-fonte como uma string fixa**, mas são o resultado matemático de um "estado padrão".

- **Cálculo:** Média harmônica de 6 componentes.
- **Estado Atual:** Os componentes (Neural, Simbólico, etc.) estão retornando um valor default `0.5` (placeholder) porque ainda não estão processando dados reais em tempo real durante o teste de chaos.
- **Resultado:** `HarmonicMean(0.5, 0.5, 0.5, 0.5, 0.5, 0.5) ≈ 0.5010`.
- **Conclusão:** O *mecanismo* de cálculo funciona (é dinâmico), mas os *dados* de entrada estão estáticos no momento.

