import sys
from typing import TypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired  # noqa
else:
    from typing_extensions import NotRequired


class InboundUser(TypedDict):
    id: str
    flow: str
    level: int
    email: str
    created_at: NotRequired[str]
