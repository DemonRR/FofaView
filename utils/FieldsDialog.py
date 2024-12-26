from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout
from qfluentwidgets import MessageBoxBase, CheckBox, SubtitleLabel
from utils.config import cfg


class FieldsDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('设置Fields', self)
        self.selected_checkboxes = []  # 用于记录选中的CheckBox的文本
        self.setup_ui()

    def setup_ui(self):
        grid_layout = QGridLayout()

        checkbox_texts = ['host', 'title', 'ip', 'port', 'domain', 'country', 'province', 'city',
                          'country_name', 'header', 'server', 'protocol', 'banner', 'cert', 'isp',
                          'as_number', 'as_organization', 'latitude', 'longitude', 'structinfo',
                          'icp', 'fid', 'cname']

        # 默认选中的字段
        default_selected = list(cfg.fields_value.value.split(','))

        self.checkbox_list = []  # 用于保存创建的CheckBox实例，方便后续操作
        row, col = 0, 0
        for text in checkbox_texts:
            checkbox = CheckBox(text)
            self.checkbox_list.append(checkbox)

            # 如果字段在默认选中列表中，设置为已选中状态
            if text in default_selected:
                checkbox.setChecked(True)
                self.selected_checkboxes.append(text)  # 立即将默认选中的字段加入 selected_checkboxes

            # 设置特定字段为不可修改
            if text == 'host':
                checkbox.setChecked(True)  # 默认选中
                checkbox.setEnabled(False)  # 设置为不可修改
                self.selected_checkboxes.append(text)  # 确保 'host' 在选中列表中

            # 为每个CheckBox关联状态改变的信号槽
            checkbox.stateChanged.connect(lambda state, t=text: self.on_checkbox_state_changed(state, t))
            grid_layout.addWidget(checkbox, row, col)
            col += 1
            if col == 5:
                col = 0
                row += 1

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(grid_layout)

    def on_checkbox_state_changed(self, state, checkbox_text):
        """
        处理CheckBox状态改变的槽函数
        :param state: CheckBox的状态（选中为Qt.Checked，未选中为Qt.Unchecked）
        :param checkbox_text: CheckBox对应的文本
        """
        if state == Qt.CheckState.Checked.value:
            if checkbox_text not in self.selected_checkboxes:
                self.selected_checkboxes.append(checkbox_text)
        else:
            if checkbox_text in self.selected_checkboxes:
                self.selected_checkboxes.remove(checkbox_text)

    def get_selected_checkboxes_str(self):
        """
        获取以逗号分隔的选中的CheckBox文本字符串
        :return: 逗号分隔的选中的CheckBox文本字符串
        """
        return ','.join(self.selected_checkboxes)
