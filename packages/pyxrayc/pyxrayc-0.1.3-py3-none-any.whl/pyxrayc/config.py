from decouple import config

XRAY_CONFIG_PATH: str = config(
    "XRAY_CONFIG_PATH",
    default="/usr/local/etc/xray/config.json",
)
XRAY_BACKUP_PATH: str = config(
    "XRAY_BACKUP_PATH",
    default="/usr/local/etc/xray/backup.json",
)
