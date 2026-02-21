from __future__ import annotations

from contextvars import ContextVar
from typing import Optional

_current_tenant = ContextVar("current_tenant", default=None)


def set_current_tenant(tenant) -> None:
    _current_tenant.set(tenant)


def get_current_tenant():
    return _current_tenant.get()


def clear_current_tenant() -> None:
    _current_tenant.set(None)
