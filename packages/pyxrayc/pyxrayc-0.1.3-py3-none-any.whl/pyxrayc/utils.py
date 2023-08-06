import re
import shutil
import subprocess as sp
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast
from uuid import uuid4

if TYPE_CHECKING:
    from pyxrayc.types import InboundUser
    from pyxrayc.enums import SupportedProtocol

import ujson

from pyxrayc.config import XRAY_BACKUP_PATH, XRAY_CONFIG_PATH

EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def load_config() -> Dict[str, Any]:
    with open(XRAY_CONFIG_PATH) as f:
        return ujson.load(f)


def save_config(config: Dict[str, Any]) -> None:
    with open(XRAY_CONFIG_PATH, "w") as f:
        ujson.dump(config, f, indent=4)


def save_backup() -> None:
    shutil.copy(f"{XRAY_CONFIG_PATH}", XRAY_BACKUP_PATH)


def rollback() -> None:
    shutil.copy(f"{XRAY_BACKUP_PATH}", XRAY_CONFIG_PATH)


def validate_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email))


def restart_xray() -> None:
    sp.run(["service", "xray", "restart"], check=True)


def create_user(
    email: str,
    flow: str = "xtls-rprx-direct",
    level: int = 0,
) -> "InboundUser":
    return {
        "id": str(uuid4()),
        "flow": flow,
        "level": level,
        "email": email,
        "created_at": datetime.utcnow().isoformat(),
    }


def get_user(email: str, users: List["InboundUser"]) -> Optional["InboundUser"]:
    for user in users:
        if user["email"] == email:
            return user
    return None


def get_users(
    config: Dict[str, Any],
    proto: "SupportedProtocol",
    port: int,
) -> List["InboundUser"]:
    config = load_config()
    inbounds = config["inbounds"]
    for inbound in inbounds:
        if inbound["protocol"] == proto.lower() and inbound["port"] == port:
            return cast(List["InboundUser"], inbound["settings"]["clients"])
    return []
