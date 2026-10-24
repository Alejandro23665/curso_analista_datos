"""Acceso con contraseña única (la app es de un solo usuario).

Si APP_PASSWORD está vacía (uso local), no se pide nada. Si está definida, el navegador recibe una
cookie HttpOnly firmada con HMAC tras introducir la contraseña correcta.
"""
import hashlib
import hmac

from .config import APP_PASSWORD

COOKIE_NAME = "datapath_session"
COOKIE_MAX_AGE = 60 * 60 * 24 * 60  # 60 días


def enabled() -> bool:
    return bool(APP_PASSWORD)


def session_token() -> str:
    return hmac.new(APP_PASSWORD.encode(), b"datapath-session-v1", hashlib.sha256).hexdigest()


def is_authenticated(cookie_value) -> bool:
    if not enabled():
        return True
    return hmac.compare_digest((cookie_value or "").encode(), session_token().encode())


def check_password(password: str) -> bool:
    return enabled() and hmac.compare_digest((password or "").encode(), APP_PASSWORD.encode())
