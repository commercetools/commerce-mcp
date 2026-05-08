from __future__ import annotations

from typing import TYPE_CHECKING
from .schemas import ReadAssociateRoleParams
from ...shared.errors import SDKError

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext

from .admin_functions import read_associate_role as _admin_read


async def read_associate_role(
    params: ReadAssociateRoleParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    # Associate roles are global (no /as-associate/ path) — same URL as admin read.
    try:
        return await _admin_read(params, api, ctx)
    except Exception as e:
        raise SDKError("read associate role as associate", e)
