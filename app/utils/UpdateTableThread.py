# UpdateTableThread.py

import math
from PyQt6.QtCore import QThread, pyqtSignal

class UpdateThread(QThread):
    update_finished = pyqtSignal(list, int, int)  # 定义信号，传递更新的数据（分页数据、当前页、总页数）

    def __init__(self, check_data, current_page, page_size, parent=None):
        super().__init__(parent)
        self.check_data = check_data
        self.current_page = current_page
        self.page_size = page_size

    def run(self):
        start_index = (self.current_page - 1) * self.page_size
        total_pages = math.ceil(len(self.check_data) / self.page_size)
        end_index = min(start_index + self.page_size, len(self.check_data))
        page_data = self.check_data[start_index:end_index]

        self.update_finished.emit(page_data, self.current_page, total_pages)
