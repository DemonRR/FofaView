# coding:utf-8
import sys

import requests
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from qfluentwidgets import FluentIcon as FIF, OptionsSettingCard, qconfig, setFont
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, PrimaryPushSettingCard,
                            ScrollArea, ExpandLayout)

from utils.ShowInfoBar import ShowInfoBar
from utils.config import cfg, FEEDBACK_URL, AUTHOR, VERSION, YEAR, LATEST_API


class SettingInterface(ScrollArea):
    """ 设置界面 """

    checkUpdateSig = pyqtSignal()  # 检查更新信号
    feedbackSig = pyqtSignal()  # 反馈信号

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingInterface")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)


        # 设置标签
        self.settingLabel = QLabel("设置", self)
        self.settingLabel.setObjectName("settingsLabel")
        setFont(self.settingLabel, 30)

        # 关于应用部分
        self.aboutGroup = SettingCardGroup("关于", self.scrollWidget)
        self.feedbackCard = PrimaryPushSettingCard(
            "提供反馈",
            FIF.FEEDBACK,
            "提供反馈",
            "通过提供反馈帮助我改进Fofa-View",
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            "检查更新",
            FIF.INFO,
            "关于",
            "©版权 " + f" {YEAR}, {AUTHOR}. " +
            "版本" + f" {VERSION}",
            self.aboutGroup
        )
        self.aboutCard.clicked.connect(self.click_update)

        # 软件更新部分
        self.updateSoftwareGroup = SettingCardGroup("软件更新", self.scrollWidget)
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            "在应用启动时检查更新",
            "新版本会更稳定并且有更多功能",
            configItem=cfg.checkUpdateAtStartUp
        )
        self.optioncard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            "应用主题",
            "调整你的应用外观",
            texts=["浅色", "深色", "跟随系统设置"],
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # 初始化布局
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(60, 63)

        # 将设置卡片组添加到布局中
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)
        self.aboutGroup.addSettingCard(self.optioncard)

        self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)

        # 将设置卡片组添加到布局中
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)

        self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __connectSignalToSlot(self):
        # 关于部分
        self.aboutCard.clicked.connect(self.checkUpdateSig)
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))

    def get_latest_version(self):
        token = ""
        headers = {
            "Authorization": f"token {token}"
        }
        url = LATEST_API
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                release_info = response.json()
                self.new_version = release_info["tag_name"]
            else:
                self.new_version = VERSION
        except requests.RequestException as e:
            ShowInfoBar.createWarningInfoBar(self, e)

    def check_update(self):
        self.get_latest_version()
        if cfg.checkUpdateAtStartUp.value and self.new_version > VERSION:
            return True
        else:
            return False

    def click_update(self):
        self.get_latest_version()
        if self.new_version > VERSION:
            ShowInfoBar.createWarningInfoBar(self, "有新版本可升级！")
        else:
            ShowInfoBar.createSuccessInfoBar(self, "当前已是最新版本！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SettingInterface()
    w.show()
    sys.exit(app.exec())

