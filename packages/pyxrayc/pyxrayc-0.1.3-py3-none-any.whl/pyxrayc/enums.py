from enum import Enum


class SupportedProtocol(str, Enum):
    """Currently supported protocols."""

    VLESS = "vless"
    VMESS = "vmess"
