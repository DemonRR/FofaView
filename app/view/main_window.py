# coding: utf-8
from PyQt6.QtCore import QUrl, QSize
from PyQt6.QtGui import QIcon, QColor, QDesktopServices
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import NavigationItemPosition, FluentWindow, SplashScreen,  InfoBadgePosition, \
    MessageBox, NavigationAvatarWidget, InfoBadge
from qfluentwidgets import FluentIcon as FIF

from .search_interface import SearchInterface
from .help_interface import HelpInterface
from .config_interface import ConfigInterface
from .setting_interface import SettingInterface
from ..common.config import cfg
from ..common.icon import Icon
from ..common.setting import STAR_URL
from ..common.signal_bus import signalBus
from ..common import resource
from ..utils.ShowInfoBar import ShowInfoBar


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()


        # TODO: create sub interface
        # self.homeInterface = HomeInterface(self)
        self.helpInterface = HelpInterface()
        self.settingInterface = SettingInterface(self)
        self.configInterface = ConfigInterface()
        self.searchInterface = SearchInterface()

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def initNavigation(self):
        # self.navigationInterface.setAcrylicEnabled(True)

        # TODO: add navigation items
        # self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))

        # add custom widget to bottom
        self.addSubInterface(self.searchInterface, FIF.SEARCH, self.tr('Search'))
        self.addSubInterface(self.configInterface, FIF.DEVELOPER_TOOLS, self.tr('Config'))
        self.addSubInterface(self.helpInterface, FIF.HELP, self.tr('Help'))

        self.navigationInterface.addWidget(
            routeKey="avatar",
            widget=NavigationAvatarWidget(self.tr("avatar"), ":/app/images/avatar.jpg"),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM
        )

        setting_button = self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

        # 给设置按钮添加徽章
        if self.settingInterface.check_update():
            InfoBadge.attension(
                text=1,
                parent=setting_button.parent(),
                target=setting_button,
                position=InfoBadgePosition.NAVIGATION_ITEM
            )
            ShowInfoBar.createWarningInfoBar(self, self.tr('There is a new version to update!'))

        self.navigationInterface.setCurrentItem(self.searchInterface)
        self.splashScreen.finish()

    def initWindow(self):
        self.resize(1024, 768)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/app/images/logo.png'))
        self.setWindowTitle('FofaView')

        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def showMessageBox(self):
        w = MessageBox(
            self.tr("Supporting Author🥰"),
            self.tr("Personal development is not easy. If this project helped you, consider giving the author a Star."),
            self,
        )
        w.yesButton.setText(self.tr("Yes"))
        w.cancelButton.setText(self.tr("No"))
        if w.exec():
            QDesktopServices.openUrl(QUrl(STAR_URL))