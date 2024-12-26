# SearchInterface.py
import base64
import math
import requests
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QDialog, QListWidgetItem
from utils.ExportThread import ExportThread
from utils.UpdateTableThread import UpdateThread
from utils.ShowInfoBar import ShowInfoBar
from utils.config import cfg
from qfluentwidgets import (CardWidget, PushButton, SearchLineEdit, SpinBox, TableWidget,
                            PrimaryPushButton, StrongBodyLabel, SwitchButton, ProgressBar, ToolButton,
                            FluentIcon as FIF, ListWidget, qconfig)
from utils.IsAliveThread import UrlAliveCheckThread


class SearchInterface(QWidget):
    def __init__(self):  # 初始化方法
        super().__init__()  # 继承父类初始化方法
        self.setObjectName("SearchInterface")
        self.search_ui()
        self.searchInput.setFocus()
        self.current_page = 1  # 当前页码，初始化为1
        self.page_size = 20  # 固定每页显示20条数据
        self.searchHistory = cfg.history_list.value  # 初始历史记录

    def search_ui(self):
        layout = QVBoxLayout(self)
        card_widget = CardWidget(self)
        buttons_layout = QHBoxLayout(card_widget)

        # size调整控件
        self.sizeSpinBox = SpinBox(self)
        self.sizeSpinBox.setRange(1, 10000)
        self.sizeSpinBox.setValue(100)
        self.sizeSpinBox.setAccelerated(True)
        self.sizeSpinBox.setToolTip('设置查询条数')
        self.sizeSpinBox.setToolTipDuration(1000)
        self.sizeSpinBox.setMinimumWidth(150)

        # 搜索框
        self.searchInput = SearchLineEdit(self)
        self.searchInput.setPlaceholderText("输入查询条件")
        self.searchInput.searchSignal.connect(lambda text: self.get_search(text))
        self.searchInput.returnPressed.connect(lambda: self.searchInput.searchSignal.emit(self.searchInput.text()))
        self.searchInput.returnPressed.connect(self.add_to_history)
        self.searchInput.returnPressed.connect(self.save_history)
        self.searchInput.searchSignal.connect(self.add_to_history)
        self.searchInput.searchSignal.connect(self.save_history)

        # 历史按钮
        self.historyButton = ToolButton(FIF.HISTORY, self)
        self.historyButton.setToolTip("显示历史记录")
        self.historyButton.clicked.connect(self.show_history_popup)

        # 存活检测开关
        self.aliveButton = SwitchButton()
        self.aliveButton.setChecked(False)
        self.aliveButton.setOffText("False")
        self.aliveButton.setOnText("True")
        self.aliveButton.setToolTip('是否开启存活探测')
        self.aliveButton.setToolTipDuration(1000)

        # 导出按钮
        self.exportButton = PushButton("全量导出", self)
        self.exportButton.setEnabled(False)
        self.exportButton.clicked.connect(self.export_excel)

        # 添加table
        self.table_widget = TableWidget(self)
        self.table_widget.setBorderRadius(8)
        self.table_widget.setBorderVisible(True)


        # 进度条
        self.progressBar = ProgressBar(self)
        self.progressBar.setVisible(False)
        self.progressBar.setRange(0, self.sizeSpinBox.value())

        # 添加分页布局
        self.paginationWidget = QWidget(self)
        self.pagination_layout = QHBoxLayout(self.paginationWidget)
        self.prevButton = PrimaryPushButton('上一页', self)
        self.prevButton.setEnabled(False)
        self.prevButton.clicked.connect(self.prev_page)
        self.nextButton = PrimaryPushButton('下一页', self)
        self.nextButton.setEnabled(False)
        self.nextButton.clicked.connect(self.next_page)
        self.pageLabel = StrongBodyLabel(self)

        # 组件加入按钮布局
        buttons_layout.addWidget(self.sizeSpinBox)
        buttons_layout.addWidget(self.searchInput, 1)
        buttons_layout.addWidget(self.historyButton)
        buttons_layout.addWidget(self.aliveButton)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.exportButton)

        # 第一个布局（左侧：进度条）
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progressBar)
        progress_layout_widget = QWidget(self)
        progress_layout_widget.setLayout(progress_layout)

        # 第二个布局（右侧：分页按钮）
        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.prevButton, 2)
        pagination_layout.addWidget(self.pageLabel, 1)
        pagination_layout.addWidget(self.nextButton, 2)

        # 外层布局（水平布局，左侧占更多空间）
        layout_h = QHBoxLayout()
        layout_h.addWidget(progress_layout_widget, 3)  # 左侧占3份
        layout_h.addLayout(pagination_layout, 1)  # 右侧占1份

        # 添加布局到主布局
        layout.addWidget(card_widget)
        layout.addWidget(self.table_widget)
        layout.addLayout(layout_h)

        # self.setStyleSheet("SearchInterface {background: white;}")  # 确保背景为白色
        self.resize(1024, 650)

    def get_search(self, q):
        # 检查 API Key 是否为空
        if not cfg.apiKey.value.strip():  # 判断是否为空或仅包含空格
            ShowInfoBar.createErrorInfoBar(self, 'API Key 不能为空，请检查配置')
            return  # 中断方法执行

        qb = base64.b64encode(q.encode('utf-8')).decode('utf-8')
        url = f'https://fofa.info/api/v1/search/all?key={cfg.apiKey.value}&size={self.sizeSpinBox.value()}&full={cfg.full_status.value}&fields={cfg.fields_value.value}&qbase64={qb}'
        # print(url)      # 排错使用

        try:
            response = requests.get(url).json()
        except requests.RequestException as e:
            ShowInfoBar.createErrorInfoBar(self, f'请求失败: {e}')
            return

        # 判断返回结果中的错误信息
        if response.get("error"):
            ShowInfoBar.createErrorInfoBar(self, f'查询语法错误: {response.get("errmsg", "未知错误")}')
            return

        self.result_data = response.get('results', [])
        self.initial_lengths = len(self.result_data[0]) if self.result_data else 0  # 记录数据的初始长度

        if not self.result_data:  # 如果结果为空
            ShowInfoBar.createErrorInfoBar(self, '查询无结果请检查语法是否有误')
            return

        if self.aliveButton.isChecked():
            # 启动存活检测线程
            self.is_alive(self.result_data)
        else:
            # 如果不进行存活检测，直接使用结果数据
            self.final_data = self.result_data
            self.update_table(self.final_data)

    def update_table(self, data):
        # 启动 UpdateThread 来处理分页逻辑
        self.update_thread = UpdateThread(data, current_page=self.current_page, page_size=self.page_size)
        self.update_thread.update_finished.connect(self.on_update_finished)  # 连接信号
        self.update_thread.start()  # 启动线程

    def is_alive(self, data):
        # 启动 URL 存活检测线程
        self.progressBar.setVisible(True)  # 显示进度条
        self.check_thread = UrlAliveCheckThread(data, self.aliveButton.isChecked())
        self.check_thread.check_signal.connect(self.on_check_finished)
        self.check_thread.check_finished_signal.connect(self.on_check_finished_signal)
        self.check_thread.progressBar_value.connect(self.on_progressBar_value)
        self.check_thread.start()

    def on_check_finished(self, data):
        self.final_data = data  # 更新最终数据
        self.update_table(self.final_data)

    def on_check_finished_signal(self):
        # 当检测完成时启用按钮
        self.exportButton.setEnabled(True)
        self.progressBar.setVisible(False)  # 检测完成后隐藏进度条

    def on_progressBar_value(self, value):
        self.progressBar.setValue(value)

    def on_update_finished(self, page_data, current_page, total_pages):
        # 更新 UI（如表格和分页按钮）
        self.pageLabel.setText(f'第{current_page}页,共{total_pages}页')  # 设置显示页数
        self.prevButton.setEnabled(current_page > 1)
        self.nextButton.setEnabled(current_page < total_pages)

        # 更新表格
        self.table_widget.clear()
        headers_list = list(cfg.fields_value.value.split(','))
        if self.aliveButton.isChecked():
            headers_list.append('存活状态')
        self.table_widget.setColumnCount(len(headers_list))  # 设置列数
        self.table_widget.setRowCount(len(page_data))  # 设置行数
        self.table_widget.setHorizontalHeaderLabels(headers_list)
        for row, data in enumerate(page_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)

        # 在数据填充完毕后启用按钮
        self.exportButton.setEnabled(True)

        # 调整列宽和行高
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()


    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table(self.final_data)

    def next_page(self):
        total_pages = math.ceil(len(self.result_data) / self.page_size)  # 向上取整计算总页数
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_table(self.final_data)

    def export_excel(self):
        # 启动导出线程，传递 result_data 给线程
        headers_list = list(cfg.fields_value.value.split(','))
        if self.aliveButton.isChecked():
            headers_list.append('存活状态')
        self.export_thread = ExportThread(self.result_data, headers_list)  # 传递 result_data 给线程
        self.export_thread.export_finished.connect(self.on_export_finished)  # 连接信号
        self.export_thread.start()  # 启动线程

    def on_export_finished(self, message):
        # 处理导出完成后的消息
        ShowInfoBar.createSuccessInfoBar(self, message)

    def show_history_popup(self):
        """弹出历史记录浮屏"""
        if hasattr(self, 'popup') and self.popup.isVisible():
            return

        self.popup = QDialog(self)  # 替代 PopupWidget
        self.popup.setWindowTitle("历史记录")
        self.popup.setWindowFlag(Qt.WindowType.Popup)  # 设置为浮动窗口
        self.popup.setFixedSize(300, 200)

        # 列表显示历史记录
        self.historyList = ListWidget(self.popup)
        for history in self.searchHistory:
            item = QListWidgetItem(history)
            self.historyList.addItem(item)

        self.historyList.itemClicked.connect(lambda item: self.fill_input_from_history(item, self.popup))

        popupLayout = QVBoxLayout(self.popup)
        clearButton = PushButton('清空历史', self)
        clearButton.clicked.connect(self.clear_history)

        popupLayout.addWidget(self.historyList)
        # popupLayout.addStretch(1)
        popupLayout.addWidget(clearButton)
        self.popup.setLayout(popupLayout)

        # 显示在按钮下方
        button_pos = self.historyButton.mapToGlobal(QPoint(0, 0))
        self.popup.move(button_pos.x(), button_pos.y() + self.historyButton.height() + 5)
        self.popup.show()  # 模态弹窗替代 show()

    def fill_input_from_history(self, item: QListWidgetItem, popup: QDialog):
        """点击历史记录，填充到搜索框"""
        self.searchInput.setText(item.text())
        popup.close()

    def add_to_history(self):
        """将搜索内容添加到历史记录"""
        text = self.searchInput.text().strip()
        if text and text not in self.searchHistory:
            self.searchHistory.insert(0, text)  # 最新的记录放在最前面
            if len(self.searchHistory) > 10:  # 限制最多保存10条记录
                self.searchHistory.pop()

    def save_history(self):
        cfg.set(cfg.history_list, self.searchHistory)
        qconfig.load('config/config.json', cfg)

    def clear_history(self):
        self.searchHistory = []
        cfg.set(cfg.history_list, self.searchHistory)
        self.popup.close()

    def mousePressEvent(self, event: QMouseEvent):
        if hasattr(self, 'popup') and self.popup and self.popup.isVisible() and event.button() == Qt.MouseButton.LeftButton:
            self.popup.close()

        super().mousePressEvent(event)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = SearchInterface()
#     w.show()
#     sys.exit(app.exec())
