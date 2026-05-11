from __future__ import annotations

from typing import TYPE_CHECKING

from .schemas import UpdatePaymentIntentsParams
from ...shared.errors import ContextError, SDKError
from ...shared.transform import transform_tool_output

if TYPE_CHECKING:
    from ...api import CommercetoolsAPI
    from ...config import CTContext


async def update_payment_intents(
    params: UpdatePaymentIntentsParams,
    api: "CommercetoolsAPI",
    ctx: "CTContext",
) -> str:
    if not ctx.is_admin:
        raise ContextError("update_payment_intents", "isAdmin")
    try:
        body = {
            "actions": [a.model_dump(by_alias=True, exclude_none=True) for a in params.actions],
        }
        result = await api.post(f"/payments/{params.payment_id}/payment-intents", body=body)
        return transform_tool_output(result)
    except ContextError:
        raise
    except Exception as e:
        raise SDKError("update payment intents", e)
