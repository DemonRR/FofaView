import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QFileDialog
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (GroupHeaderCardWidget, SearchLineEdit, IconWidget, InfoBarIcon,
                            BodyLabel, PrimaryPushButton, FluentIcon, LineEdit, SwitchButton,
                            HorizontalSeparator, PushButton)

from utils.FieldsDialog import FieldsDialog
from utils.ShowInfoBar import ShowInfoBar
from utils.config import cfg


class ConfigInterface(GroupHeaderCardWidget):
    def __init__(self):
        super().__init__()
        self.setTitle("基本设置")
        self.setBorderRadius(8)

        self.keyLineEdit = LineEdit(self)
        self.keyLineEdit.setText(cfg.apiKey.value)
        self.fullButton = SwitchButton()
        self.fullButton.setChecked(cfg.full_status.value)
        self.fullButton.setOffText("False")
        self.fullButton.setOnText("True")
        self.fieldsLineEdit = LineEdit(self)
        self.fieldsLineEdit.setPlaceholderText("点击加号进行选择")
        self.fieldsLineEdit.setText(cfg.fields_value.value)
        self.fieldsLineEdit.setClearButtonEnabled(True)
        action1 = QAction(FluentIcon.ADD_TO.qicon(), "", triggered=self.showDialog)
        self.fieldsLineEdit.addAction(action1, QLineEdit.ActionPosition.TrailingPosition)
        self.exportPathButton = PushButton("选择")
        self.exportPathButton.clicked.connect(self.save_path)

        self.lineEdit = SearchLineEdit()

        self.saveIcon = IconWidget(InfoBarIcon.INFORMATION)
        self.saveLabel = BodyLabel("点击按钮进行保存 👉")
        self.saveButton = PrimaryPushButton(FluentIcon.SEND, "保存")
        self.bottomLayout = QHBoxLayout()

        self.keyLineEdit.setFixedWidth(320)
        self.fieldsLineEdit.setFixedWidth(520)

        self.line = HorizontalSeparator()

        # 设置底部工具栏布局
        self.saveIcon.setFixedSize(16, 16)
        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomLayout.addWidget(self.saveIcon, 0, Qt.AlignmentFlag.AlignLeft)
        self.bottomLayout.addWidget(self.saveLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.saveButton, 0, Qt.AlignmentFlag.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # 添加组件到分组中
        self.addGroup(FIF.VPN, "Fofa key", "填入你的Fofa key", self.keyLineEdit)
        self.addGroup(FIF.IOT, "full", "默认搜索一年内的数据，指定为true即可搜索全部数据", self.fullButton)
        self.addGroup(FIF.LIBRARY, "fields", "选择查询字段", self.fieldsLineEdit)

        self.group = self.addGroup(FIF.FOLDER_ADD, "选择导出保存路径", f"{cfg.export_path.value}", self.exportPathButton)
        self.saveButton.clicked.connect(self.save_settings)
        self.group.setSeparatorVisible(True)

        # 添加底部工具栏
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.line)
        self.vBoxLayout.addLayout(self.bottomLayout)

    def showDialog(self):
        w = FieldsDialog(self)
        if w.exec():
            self.fieldsLineEdit.setText(w.get_selected_checkboxes_str())

    def save_path(self):
        file_dialog = QFileDialog()
        self.selected_directory = file_dialog.getExistingDirectory(self, "选择文件夹", os.getcwd())
        if self.selected_directory:
            self.group.setContent(self.selected_directory)


    def save_settings(self):
        # 获取选定的目录，如果没有选定，则使用默认目录
        export_path = self.group.content() or os.getcwd()  # 使用当前工作目录作为默认路径
        # 设置配置项
        if not self.keyLineEdit.text() or not self.fieldsLineEdit.text():
            ShowInfoBar.createErrorInfoBar(self, "Key和fields为必填项")
        else:
            cfg.set(cfg.apiKey, self.keyLineEdit.text().strip())
            cfg.set(cfg.full_status, self.fullButton.isChecked())
            cfg.set(cfg.fields_value, self.fieldsLineEdit.text())
            cfg.set(cfg.export_path, export_path)
            ShowInfoBar.createSuccessInfoBar(self,'保存成功！')


