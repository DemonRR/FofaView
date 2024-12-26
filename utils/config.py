# coding:utf-8
import os
from qfluentwidgets import (qconfig, QConfig, ConfigItem, BoolValidator, FolderValidator)


class Config(QConfig):
    # 软件更新
    checkUpdateAtStartUp = ConfigItem(
        "Update", "CheckUpdateAtStartUp", True, BoolValidator())

    apiKey = ConfigItem(
        "ApiKey", "ApiKey", ""
    )

    full_status = ConfigItem(
        "FullStatus", "CheckFullStatus", False, BoolValidator()
    )

    fields_value = ConfigItem(
        "FieldsValue", "FieldsValue", 'host,protocol,ip,port,title,domain,country')

    export_path = ConfigItem(
        "ExportPath", "Export_Path", os.getcwd(), FolderValidator()
    )

    history_list = ConfigItem(
        "HistoryList", "HistoryList", []
    )


YEAR = 2024
AUTHOR = "Demon"
VERSION = '2.0.4'
owner = "DemonRR"
repo = "FofaView"
HELP_URL = f"https://github.com/{owner}/{repo}/issues"
FEEDBACK_URL = f"https://github.com/{owner}/{repo}/issues"
RELEASE_URL = f"https://github.com/{owner}/{repo}/releases/latest"
LATEST_API = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
STAR_URL = f"https://github.com/{owner}/{repo}"

cfg = Config()
qconfig.load('config/config.json', cfg)
