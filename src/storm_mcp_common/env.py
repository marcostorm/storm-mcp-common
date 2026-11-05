"""Helpers pra ler env vars obrigatórias/tipadas de forma consistente
entre os workers do Storm Lab (bot, watchdog, MCPs)."""
from __future__ import annotations

import os


def require_env(key: str) -> str:
    """Retorna `os.environ[key]` ou levanta `RuntimeError` descrevendo qual
    env está faltando. Env vazia vale como ausente (típico de `.env`
    gerado com placeholder em branco)."""
    val = os.environ.get(key)
    if not val:
        raise RuntimeError(f"missing env var: {key}")
    return val


def int_env(key: str, default: int) -> int:
    """`int(os.environ[key])` ou `default` se ausente/vazia. Não captura
    `ValueError` — deixa falhar explícito se valor não é numérico."""
    raw = os.environ.get(key)
    return int(raw) if raw else default


def bool_env(key: str, default: bool = False) -> bool:
    """Lê env como bool. Trata `1/true/yes/on` (case-insensitive) como
    `True`, `0/false/no/off` como `False`. Ausente/vazia = `default`."""
    raw = os.environ.get(key, "").strip().lower()
    if not raw:
        return default
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    return default
