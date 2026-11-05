"""Validators pra nomes/args em MCPs do Storm Lab.

Regra padrão: alfanumérico + caracteres explicitamente whitelistados.
Bloqueia shell metachars (espaço, pipe, `;`, `&`, `>`, aspas, barras, `..`) e
caracteres non-ASCII suspeitos. Centralizado aqui pra evitar drift entre os
MCPs (`storm-vps`, `storm-projects`, outros) — antes cada um tinha a mesma
função em arquivos paralelos.
"""
from __future__ import annotations

_DEFAULT_EXTRA = "-_."


def is_safe_name(value: str, extra_chars: str = _DEFAULT_EXTRA) -> bool:
    """True se `value` é alfanumérico + chars em `extra_chars` apenas.

    `value` vazio ou `None` retorna `False`. `extra_chars` pode conter
    qualquer sequência de caracteres permitidos além do `isalnum`.
    """
    if not value:
        return False
    return value.translate(str.maketrans("", "", extra_chars)).isalnum()


def validate_name(value: str, kind: str, extra_chars: str = _DEFAULT_EXTRA) -> None:
    """Lança `ValueError` se `value` não é safe. `kind` entra na msg de erro."""
    if not is_safe_name(value, extra_chars):
        raise ValueError(f"{kind} inválido: {value!r}")


def validate_container_name(name: str) -> None:
    """Container Docker: alfanum + `-_.`."""
    validate_name(name, "nome de container", extra_chars="-_.")


def validate_loja_name(name: str) -> None:
    """Nome de loja do Storm Commerce: alfanum + `-_` (sem `.` pra não
    confundir com domínio)."""
    validate_name(name, "nome de loja", extra_chars="-_")


def validate_tag(tag: str) -> None:
    """Tag de imagem Docker: alfanum + `-_.`."""
    validate_name(tag, "tag", extra_chars="-_.")


def validate_run_id(run_id: str) -> None:
    """ID de run de deploy async: alfanum + `-_`."""
    validate_name(run_id, "run_id", extra_chars="-_")


def validate_identifier(name: str) -> None:
    """Identificador genérico: alfanum + `-_.`. Use quando nenhum validador
    específico se encaixa."""
    validate_name(name, "identificador", extra_chars="-_.")
