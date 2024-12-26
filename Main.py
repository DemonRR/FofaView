import sys
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel
from qfluentwidgets import (
    NavigationInterface, NavigationItemPosition, NavigationAvatarWidget, MessageBox,
    FluentIcon as FIF, InfoBadgePosition, DotInfoBadge, setTheme
)
from qframelesswindow import FramelessWindow, StandardTitleBar
from interface.SearchInterface import SearchInterface
from interface.SettingInterface import SettingInterface
from interface.ConfigInterface import ConfigInterface
from interface.HelpInerface import HelpInterface
from utils.config import STAR_URL
from utils.ResourcePath import resource_path
from utils.ShowInfoBar import ShowInfoBar
from utils.config import cfg


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))
        setTheme(cfg.themeMode.value)


class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        # 布局
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        # 创建子界面
        self.searchInterface = SearchInterface()
        self.configInterface = ConfigInterface()
        self.helpInterface = HelpInterface()
        self.settingInterface = SettingInterface()

        # 初始化界面
        self.initLayout()
        self.initNavigation()
        self.initWindow()

    def initLayout(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        layout.addWidget(self.navigationInterface)
        layout.addWidget(self.stackWidget)
        layout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.searchInterface, FIF.SEARCH, "Search")
        self.addSubInterface(self.configInterface, FIF.DEVELOPER_TOOLS, "Config")
        self.addSubInterface(self.helpInterface, FIF.HELP, "Help")
        self.navigationInterface.addSeparator()

        self.navigationInterface.addWidget(
            routeKey="avatar",
            widget=NavigationAvatarWidget("avatar", resource_path("resource/avatar.jpg")),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        # 添加设置按钮，并给它添加徽章
        setting_button = self.addSubInterface(self.settingInterface, FIF.SETTING, "Settings",
                                              NavigationItemPosition.BOTTOM)
        # 给设置按钮添加徽章
        self.infobadge = DotInfoBadge.error(parent=self.navigationInterface, target=setting_button,position=InfoBadgePosition.TOP_RIGHT)
        self.infobadge.setVisible(False)
        if self.settingInterface.check_update():
            self.infobadge.setVisible(True)
            ShowInfoBar.createWarningInfoBar(self, '有新版本')


        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(1024, 700)
        self.setWindowIcon(QIcon(resource_path("resource/icon.ico")))
        self.setWindowTitle("FofaView")
        # self.titleBar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        self.stackWidget.addWidget(interface)
        return self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
        )

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            "支持作者🥰",
            "个人开发不易，如果这个项目帮助到了您，可以考虑给作者点一个Star。",
            self,
        )
        w.yesButton.setText("来啦老弟")
        w.cancelButton.setText("下次一定")
        if w.exec():
            QDesktopServices.openUrl(QUrl(STAR_URL))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    window = Window()
    window.show()
    sys.exit(app.exec())
