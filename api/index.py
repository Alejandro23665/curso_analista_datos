"""Punto de entrada de la API para Vercel (función de Python).

Vercel ejecuta este archivo como función serverless y sirve la app ASGI `app`.
Todas las rutas /api/* se redirigen aquí desde vercel.json.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "backend"))

from app.main import app  # noqa: E402,F401
