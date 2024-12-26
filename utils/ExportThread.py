# export_thread.py
import csv
import os
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal
from utils.config import cfg


class ExportThread(QThread):
    export_finished = pyqtSignal(str)  # 定义一个信号，类型为 str

    def __init__(self, result_data, headers_list, parent=None):
        super().__init__(parent)
        self.result_data = result_data  # 保存主线程传来的数据
        self.headers_list = headers_list

    def run(self):
        try:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"查询数据_{current_time}.csv"
            file_path = os.path.join(cfg.export_path.value, file_name)

            # 执行导出操作
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers_list)
                writer.writerows(self.result_data)

            # 导出成功后，发出信号
            self.export_finished.emit(f"{file_path} 导出成功！")
        except Exception as e:
            # 如果出现异常，发出错误信息
            self.export_finished.emit(f"导出失败: {str(e)}")
