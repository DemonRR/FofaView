import base64
import configparser
import os
import sys
import time
import pandas as pd
import requests
from PyQt6 import uic
from markdown2 import markdown
from PyQt6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QStatusBar, QMessageBox,
    QSpinBox, QTableWidget, QTableWidgetItem, QTextBrowser
)

# 获取资源文件路径（支持打包后使用）
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 加载配置文件，获取fofa的相关配置信息
def load_config():
    config = configparser.ConfigParser()
    config.read('fofa.ini', encoding='utf-8')
    fofa_key = config.get('info', 'key', fallback=None)
    fields = config.get('fields', 'fields')
    full = config.get('full', 'full', fallback='true').lower() == 'true'
    return fofa_key, fields, full

# 检查fofa的key是否有效，通过向fofa服务器发起请求验证
def check_status(key):
    url = f'https://fofa.info/api/v1/info/my?key={key}'
    try:
        response = requests.get(url).json()
        if response.get('error'):
            return False
        return True
    except requests.RequestException as e:
        show_error_message(f"发生请求异常: {str(e)}")
        return False

# 用于在状态栏显示相应的提示信息，设置文本和颜色
def statusbar(text, color, label: QLabel):
    label.setText(text)
    label.setStyleSheet(f"color: {color};")
    myStatusBar.addWidget(label)

# 获取fofa账户相关信息并在状态栏显示
def fofa_info(key: str):
    url = f'https://fofa.info/api/v1/info/my?key={key}'
    response = requests.get(url).json()
    text = f'用户名：{response["username"]}    VIP状态：{response["isvip"]}    VIP等级：{response.get("vip_level")}'
    color = 'black'
    statusbar(text, color, statusBarLabel)

# 更新表格内容
def update_table(table, result_data, field):
    headers_list = list(field.split(','))
    table.clearContents()
    table.setRowCount(len(result_data))
    table.setColumnCount(len(result_data[0]))
    table.setHorizontalHeaderLabels(headers_list)
    for row in range(len(result_data)):
        for col in range(len(result_data[0])):
            item = QTableWidgetItem(result_data[row][col])
            table.setItem(row, col, item)

# 清空表格内容
def clear_table(table):
    table.clearContents()
    table.setRowCount(0)
    table.setColumnCount(0)


# 查询主体与显示
def get_search(q, size, key, field, full, table: QTableWidget):
    qb = base64.b64encode(q.encode('utf-8')).decode('utf-8')
    url = f'https://fofa.info/api/v1/search/all?key={key}&size={size}&full={full}&fields={field}&qbase64={qb}'
    try:
        response = requests.get(url).json()
        result_data = response.get('results')
        if result_data:
            fofa_info(key)
            update_table(table, result_data, field)
            show_message(f'查询成功！ 共查询到{len(result_data)}数据', 'green')
            return result_data
        else:
            clear_table(table)
            show_message("查询无结果！请正确填写查询条件", 'red')
            show_error_message("查询无结果！请正确填写查询条件")
            return [], []
    except requests.RequestException as e:
        show_error_message(f"搜索请求发生异常: {str(e)}")
        return [], []

# 将搜索结果保存为Excel文件
def save_excel(result_data, headers_list):
    if result_data:
        df = pd.DataFrame(result_data, columns=headers_list)
        filename_time = f"查询结果_{int(time.time())}.xlsx"
        output_filename = filename_time
        df.to_excel(output_filename, index=False)
        show_message(f'查询成功！ 文件名为：{filename_time}数据', 'green')
    else:
        show_message("无内容可导出！请查询后在选择导出功能", 'red')
        show_error_message("无内容可导出！请查询后在选择导出功能")

# 统一显示错误消息的函数，通过弹出QMessageBox来提示用户错误信息
def show_error_message(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Warning)
    msg_box.setWindowTitle("报错提示")
    msg_box.setText(message)
    msg_box.exec()

# 统一显示成功消息的函数，通过状态栏显示给定的成功消息信息（可根据实际情况调整显示方式等）
def show_message(message, color):
    color = f'{color}'
    statusbar(message, color, messageBarLabel)

def load_markdown_file(file_path):
    try:
        # 读取 Markdown 文件内容
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_text = file.read()
        # 转换为 HTML
        html_content = markdown(markdown_text)
        # 添加 CSS 样式
        styled_html = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f9f9f9; padding: 20px; }}
                        table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f4f4f4; }}
                        tr:nth-child(even) {{ background-color: #f9f9f9; }}
                        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                        code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: "Courier New", monospace; }}
                    </style>
                </head>
                <body>{html_content}</body>
                </html>
                """
        textBrowser.setHtml(styled_html)
    except Exception as e:
        textBrowser.setText(f"无法加载文件:\n{e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = uic.loadUi(resource_path("fofaView.ui"))
    ui.setFixedSize(ui.width(), ui.height())

    # UI组件绑定
    searchLineEdit: QLineEdit = ui.lineEdit
    searchPushButton: QPushButton = ui.pushButton
    outputPushButton: QPushButton = ui.pushButton_2
    statusBarLabel = QLabel()
    messageBarLabel = QLabel()
    myStatusBar: QStatusBar = ui.statusBar
    sizeSpinBox: QSpinBox = ui.spinBox
    searchTableWidget: QTableWidget = ui.tableWidget
    textBrowser: QTextBrowser = ui.textBrowser

    # 加载配置
    fofa_key, fields, full = load_config()
    load_markdown_file(resource_path("README.md"))

    if check_status(fofa_key):
        fofa_info(fofa_key)
        searchPushButton.clicked.connect(lambda: get_search(searchLineEdit.text(), sizeSpinBox.value(), fofa_key, fields, full, searchTableWidget))
        outputPushButton.clicked.connect(lambda: save_excel(
            [
                [searchTableWidget.item(row, col).text() for col in range(searchTableWidget.columnCount())] for row in range(searchTableWidget.rowCount())
            ],
            [searchTableWidget.horizontalHeaderItem(col).text() for col in range(searchTableWidget.columnCount())]
        ))
    else:
        show_message('请检测配置文件是否填写正确！', 'red')
    ui.show()
    sys.exit(app.exec())