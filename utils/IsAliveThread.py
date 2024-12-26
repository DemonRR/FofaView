import requests
import urllib3
from PyQt6.QtCore import QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.config import cfg

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class UrlAliveCheckThread(QThread):
    check_signal = pyqtSignal(list)  # 用于传递结果
    check_finished_signal = pyqtSignal()  # 检测完成信号
    progressBar_value = pyqtSignal(int)  # 用于传递进度条的值

    def __init__(self, result_data, is_up, parent=None):
        super().__init__(parent)
        self.result_data = result_data
        self.is_up = is_up
        self.total_urls = len(result_data)  # 总 URL 数量
        self.checked_urls = 0  # 已检查 URL 数量

    def run(self):
        if self.is_up:
            # 获取 URL 列表中的“host”列索引
            index = list(cfg.fields_value.value.split(',')).index('host')

            # 创建线程池
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = []
                # 提交每个 URL 检查任务
                for i in range(len(self.result_data)):
                    url = self.result_data[i][index]
                    futures.append(executor.submit(self.check_status, url, i))

                # 等待所有任务完成
                for future in as_completed(futures):
                    i, value = future.result()
                    self.result_data[i].append(value)
                    self.checked_urls += 1
                    progress = int((self.checked_urls / self.total_urls) * 100)  # 计算进度
                    self.progressBar_value.emit(progress)  # 更新进度条

            # 完成检测后，发射信号通知主线程更新数据
            self.check_signal.emit(self.result_data)
            self.check_finished_signal.emit()  # 发射检测完成信号
        else:
            # 如果不进行存活检测，直接发射结果数据
            self.check_signal.emit(self.result_data)
            self.check_finished_signal.emit()  # 发射检测完成信号

    def check_status(self, url, index):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
        }

        # 如果 URL 没有以 http:// 或 https:// 开头，默认添加 http://
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        try:
            # 先尝试 http://
            response = requests.get(url, headers=headers, verify=False, timeout=5)
            if response.status_code == 200:
                return index, '是'  # http:// 访问成功，返回是
        except requests.RequestException:
            # 如果 http:// 访问失败，尝试 https://
            if not url.startswith("https://"):
                url = "https://" + url[7:]  # 如果已经是 http://，替换为 https://

            try:
                response = requests.get(url, headers=headers, verify=False, timeout=5)
                if response.status_code == 200:
                    return index, '是'  # https:// 访问成功，返回是
            except requests.RequestException:
                # 如果 https:// 也失败，返回否
                return index, '否'

        # 如果都不成功，返回 '否'
        return index, '否'
