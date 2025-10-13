import requests

from ..common.config import cfg
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import (RoundMenu, FluentIcon, Action, AvatarWidget, BodyLabel,
                          CaptionLabel, setFont, isDarkTheme)
from ..utils import ShowInfoBar


class ProfileCard(QWidget):
    """ Profile card """

    def __init__(self, avatarPath: str, name: str, email: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name, self)
        self.emailLabel = CaptionLabel(email, self)

        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.emailLabel.setStyleSheet('QLabel{color: '+color.name()+'}')

        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: '+color.name()+'}')
        setFont(self.emailLabel, 13)
        setFont(self.nameLabel, 13)

        self.setFixedSize(160, 82)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.emailLabel.move(64, 32)


def show_custom_menu(parent, pos):
    try:
        if not cfg.apiKey.value.strip():  # 判断是否为空或仅包含空格
            ShowInfoBar.createErrorInfoBar(parent, 'API Key 不能为空，请检查配置')
            return  # 中断方法执行

        url = f"https://fofa.info/api/v1/info/my?key={cfg.apiKey.value}"

        try:
            response = requests.get(url).json()
        except requests.RequestException as e:
            ShowInfoBar.createErrorInfoBar(parent, f'请求失败: {e}')
            return

        # 判断返回结果中的错误信息
        if response.get("error"):
            ShowInfoBar.createErrorInfoBar(parent, f'查询语法错误: {response.get("errmsg", "未知错误")}')
            return
        else:
            username = response.get('username')
            email = response.get('email')
            isvip = response.get('isvip')
            vip_level = response.get('vip_level')
            fofa_point = response.get('fofa_point')

        # 确保父窗口是有效的
        if parent is None:
            raise ValueError("Parent window is None, can't show menu")

        # 创建菜单并添加内容
        menu = RoundMenu(parent=parent)
        card = ProfileCard((':/app/images/missing.jpg'), username, email, menu)
        card.setFixedHeight(55)
        menu.addWidget(card, selectable=False)
        menu.addSeparator()
        menu.addActions([
            Action(FluentIcon.PEOPLE, f'会员状态：{isvip}'),
            Action(FluentIcon.SHOPPING_CART, f'F点剩余：{fofa_point}'),
            Action(FluentIcon.SPEED_OFF, f'会员等级：{vip_level}'),
        ])

        # 在指定位置显示菜单
        menu.move(pos)  # 显式设置菜单位置
        menu.exec(pos)  # 使用exec()来弹出菜单

        return menu
    except Exception as e:
        # 捕获异常并显示错误
        ShowInfoBar.createErrorInfoBar(parent, f'发生未知错误: {str(e)}')
