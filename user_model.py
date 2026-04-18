"""
Modelo de usuário responsável pelas operações de banco de dados
relacionadas a autenticação, cadastro e perfil do usuário.
"""

import hashlib
import os
from database import get_connection


def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Gera um hash seguro para a senha usando SHA-256 com salt.
    Se nenhum salt for fornecido, gera um novo aleatoriamente.
    Retorna uma tupla (hash_hex, salt).
    """
    if salt is None:
        salt = os.urandom(32).hex()
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return hashed, salt


def _verify_password(password: str, stored_hash: str) -> bool:
    """
    Verifica se a senha informada corresponde ao hash armazenado.
    O hash armazenado contém salt:hash separados por ':'.
    """
    try:
        salt, expected_hash = stored_hash.split(":", 1)
        actual_hash, _ = _hash_password(password, salt)
        return actual_hash == expected_hash
    except Exception:
        return False


class UserModel:
    """
    Classe responsável por todas as operações de banco de dados
    relacionadas ao usuário: cadastro, login e consulta de perfil.
    """

    def register(self, email: str, password: str, emergency_contact: str = "") -> tuple[bool, str]:
        """
        Cadastra um novo usuário no banco de dados.
        Verifica se o email já está em uso antes de inserir.
        Retorna (sucesso: bool, mensagem: str).
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE email = ?", (email.lower(),))
            if cursor.fetchone():
                return False, "Este email já está cadastrado."

            password_hash, salt = _hash_password(password)
            stored = f"{salt}:{password_hash}"
            contact = emergency_contact.strip() if emergency_contact else None

            cursor.execute(
                "INSERT INTO users (email, password_hash, emergency_contact) VALUES (?, ?, ?)",
                (email.lower(), stored, contact),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Cadastro realizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao cadastrar: {e}"

    def login(self, email: str, password: str) -> tuple[bool, dict | str]:
        """
        Autentica o usuário verificando email e senha.
        Retorna (sucesso: bool, dados_do_usuario | mensagem_de_erro).
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, email, password_hash, emergency_contact FROM users WHERE email = ?",
                (email.lower(),),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if not row:
                return False, "Email não encontrado."

            if not _verify_password(password, row["password_hash"]):
                return False, "Senha incorreta."

            return True, {
                "id": row["id"],
                "email": row["email"],
                "emergency_contact": row["emergency_contact"],
            }
        except Exception as e:
            return False, f"Erro ao fazer login: {e}"

    def get_by_id(self, user_id: int) -> dict | None:
        """
        Busca e retorna os dados de um usuário pelo seu ID.
        Retorna None se não encontrado.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, email, emergency_contact FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return dict(row) if row else None
        except Exception:
            return None
