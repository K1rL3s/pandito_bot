from typing import Any

from core.enums import ALL_ROLES


async def get_roles(**__: Any) -> dict[str, Any]:
    return {"roles": ALL_ROLES}
