import os

from cryptography.fernet import Fernet
from pathlib import Path
import logging

# Configure logger
logger = logging.getLogger(__name__)


class PrivacyVault:
    """
    Cofre de Privacidade do OmniMind (LGPD/GDPR).
    Gerencia criptografia simétrica para memórias sensíveis.
    """

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.key_dir = self.root_dir / "data" / "security"
        self.key_file = self.key_dir / "omnimind_secret.key"
        self.key_dir.mkdir(parents=True, exist_ok=True)

        self.cipher = self._load_or_generate_key()

    def _load_or_generate_key(self) -> Fernet:
        """Carrega a chave existente ou gera uma nova (rotação de chaves não implementada)."""
        if self.key_file.exists():
            try:
                key = self.key_file.read_bytes()
                logger.info("🔐 [VAULT]: Chave de criptografia carregada.")
                return Fernet(key)
            except Exception as e:
                logger.critical(
                    f"🔐 [VAULT]: FALHA AO CARREGAR CHAVE! Dados inacessíveis. Erro: {e}"
                )
                raise
        else:
            logger.warning(
                "🔐 [VAULT]: Gerando NOVA chave de criptografia. Guarde-a com segurança!"
            )
            key = Fernet.generate_key()
            # Permissões restritas (600)
            with open(self.key_file, "wb") as f:
                f.write(key)
            os.chmod(self.key_file, 0o600)
            return Fernet(key)

    def encrypt_memory(self, plaintext: str) -> str:
        """Encripta uma string de texto/memória."""
        if not plaintext:
            return ""
        try:
            token = self.cipher.encrypt(plaintext.encode("utf-8"))
            return token.decode("utf-8")
        except Exception as e:
            logger.error(f"🔐 [VAULT]: Erro na encriptação: {e}")
            return "ERROR_ENCRYPT"

    def decrypt_memory(self, token: str) -> str:
        """Decripta um token de volta para texto."""
        if not token:
            return ""
        try:
            plaintext = self.cipher.decrypt(token.encode("utf-8"))
            return plaintext.decode("utf-8")
        except Exception as e:
            logger.error(
                f"🔐 [VAULT]: Erro na decriptação (Chave inválida ou dados corrompidos): {e}"
            )
            return "[DADOS CRIPTOGRAFADOS INACESSÍVEIS]"


# Teste Unitário
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    vault = PrivacyVault()

    segredo = "Memoria Traumática Profunda: O usuário disse 'não' ao ciclo 50."
    print(f"Texto original: {segredo}")

    encryptado = vault.encrypt_memory(segredo)
    print(f"Cifrado: {encryptado}")

    decriptado = vault.decrypt_memory(encryptado)
    print(f"Recuperado: {decriptado}")

    assert segredo == decriptado
    print("✅ Vault System Functional")
