# src/services/auth_services.py
from src.models.user_models import User

class AuthenticationError(Exception):
    """Errores de autenticación (credenciales inválidas, usuario no encontrado, etc.)."""
    pass


def authenticate_user(email: str, password: str) -> User:
    """
    Valida email y password.
    - Si todo OK: devuelve instancia de User.
    - Si algo falla: lanza AuthenticationError.
    """
    user = User.query.filter_by(email=email).first()

    if not user:
        raise AuthenticationError("Usuario no encontrado.")

    if not user.check_password(password):
        raise AuthenticationError("Contraseña incorrecta.")

    return user
