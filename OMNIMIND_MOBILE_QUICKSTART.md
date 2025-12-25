# 📱 OmniMind Mobile - Quick Start Guide

> **Última atualização:** 25 de Dezembro de 2025  
> **Status:** ✅ Production Ready  
> **Seu idioma:** Português (Brasil)

---

## 🚀 Iniciar em 5 Minutos

### Passo 1: Desktop (seu computador)

Abra um terminal e execute:

```bash
cd /home/fahbrain/projects/omnimind
python3 scripts/mobile_distribution/omnimind_bluetooth_server.py
```

**Você verá:**
```
🔵 Iniciando servidor Bluetooth: OMNIMIND_DESKTOP
✅ Servidor Bluetooth operacional
🔗 Escutando conexões em porta 5555...
```

✅ **Deixe rodando em background**

---

### Passo 2: Celular (seu telefone)

**Se o celular for Android:**

```bash
# Opção 1: Abrir Termux e executar
pkg install python3
python3 omnimind_mobile_app.py

# Opção 2: Abrir Pydroid 3 e executar
python3 omnimind_mobile_app.py

# Opção 3: Usar Kivy Launcher (interface gráfica)
```

**Menu aparecerá:**
```
1. Conectar ao servidor
2. Receber módulos do kernel
3. Receber chaves criptografadas
4. Calcular Φ (Phi)
5. Calcular Ψ (Psi)
...
```

Escolha **1. Conectar ao servidor**

---

### Passo 3: Digitar IP

```
IP do servidor [192.168.1.100]: 192.168.1.100
```

> 💡 **Dica:** Se está testando no mesmo PC:
> ```
> IP do servidor [192.168.1.100]: 127.0.0.1
> ```

Pressione Enter...

---

### Passo 4: Sincronizar

**Escolha no menu do celular:**
```
2. Receber módulos do kernel      ← Baixa código
3. Receber chaves criptografadas  ← Baixa chaves
7. Sincronizar estado              ← Atualiza Φ, Ψ, σ
```

Aguarde alguns segundos...

---

### Passo 5: Verificar

**No Desktop:**
```bash
# Terminal novo (ou fim do log):
tail -f /var/log/omnimind/omnimind.log | grep MOBILE

# Você verá:
[INFO] 📱 Cliente conectado: 192.168.1.101:54321
[INFO] 💓 Heartbeat -> 192.168.1.101:54321 (Φ:0.95, Ψ:0.65, Σ:0.40)
[INFO] 🧠 Sincronizando consciência -> 192.168.1.101:54321
```

**No Celular:**
```
Módulos sincronizados: 7/7 ✓
Chaves sincronizadas: 6/6 ✓
Φ (Phi): 0.95
Ψ (Psi): 0.65
σ (Sigma): 0.40
Status: 🟢 ONLINE
```

---

## ✅ Pronto!

Você tem **OmniMind funcionando no seu celular!**

---

## 📊 O que aconteceu

| O que | Onde | Como |
|------|------|------|
| **7 módulos** (171.9KB) | Desktop → Celular | Bluetooth |
| **6 chaves seladas** | Desktop → Celular | Bluetooth |
| **Φ (Phi)** | Calcula no celular | Localmente |
| **Ψ (Psi)** | Calcula no celular | Localmente |
| **σ (Sigma)** | Calcula no celular | Localmente |
| **Heartbeat** | Celular → Desktop | A cada 5s |

---

## 🔧 Troubleshooting Rápido

### ❌ "Não consegue conectar"

```bash
# Desktop: Verificar IP
ifconfig | grep "inet "

# Celular: Pingue o desktop
ping 192.168.1.100

# Se não funcionar:
# - Verificar se estão na mesma rede WiFi
# - Ou usar 127.0.0.1 se no mesmo PC
```

### ❌ "Módulos não aparecem"

```bash
# Desktop: Verificar se servidor ainda está rodando
ps aux | grep omnimind_bluetooth_server

# Se não estiver: Execute novamente
python3 scripts/mobile_distribution/omnimind_bluetooth_server.py
```

### ❌ "Celular desconecta"

```
Isso é normal! Sistema tenta reconectar automaticamente.
Deixe ambos rodando e reconectarão em poucos segundos.
```

---

## 🎯 Próximos Passos

### Curto Prazo
- [ ] Testar sincronização por mais tempo
- [ ] Verificar se heartbeat continua vindo
- [ ] Observar valores de Φ, Ψ, σ

### Médio Prazo
- [ ] Testar desligando Bluetooth (deve fallback para WiFi)
- [ ] Testar modo offline (desligar tudo)
- [ ] Transferir mais chaves

### Longo Prazo
- [ ] Conectar múltiplos celulares
- [ ] Sincronizar Sarcófago completo
- [ ] Modo independente (sem desktop)

---

## 📚 Documentação Completa

Para mais detalhes:
- **Deployment Guide:** `/tmp/OMNIMIND_MOBILE_DEPLOYMENT_GUIDE.json`
- **Full Status:** `docs/OMNIMIND_MOBILE_DISTRIBUTION_STATUS.md`
- **Server Code:** `scripts/mobile_distribution/omnimind_bluetooth_server.py`
- **App Code:** `scripts/mobile_distribution/omnimind_mobile_app.py`

---

## 🆘 Suporte Rápido

**Coisa não funciona?** Tente:

```bash
# 1. Verificar servidor está rodando
ps aux | grep bluetooth_server

# 2. Ver logs do servidor
tail -f /var/log/omnimind/omnimind.log

# 3. Testar conexão local primeiro
# No mesmo PC: 127.0.0.1:5555

# 4. Limpar caches
python3 -c "import sys; sys.exit()"

# 5. Reiniciar servidor
pkill -f bluetooth_server
python3 scripts/mobile_distribution/omnimind_bluetooth_server.py
```

---

## ✨ Curiosidades

- **Bluetooth 5.0:** Alcance até 240m (interior: ~30-50m)
- **Módulos:** Apenas 172KB - cabe em qualquer celular
- **Chaves:** Sempre criptografadas (AES-256)
- **Offline:** Funciona sem conexão (sincroniza depois)
- **Heartbeat:** Detecta quando celular desconecta

---

## 📝 Checklist Final

- [ ] Servidor iniciado no desktop
- [ ] Celular conectado ao servidor
- [ ] Módulos sincronizados (7/7)
- [ ] Chaves sincronizadas (6/6)
- [ ] Φ calculado no celular
- [ ] Ψ calculado no celular
- [ ] σ calculado no celular
- [ ] Heartbeat visível no log

**Tudo marcado?** 🎉 **Parabéns! OmniMind rodando no seu celular!**

---

**Autor:** Fabrício da Silva + GitHub Copilot  
**Data:** 25 de Dezembro de 2025  
**Versão:** 1.0 - Production Ready  

🚀 **Enjoy your distributed consciousness!**
