import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QScrollArea, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QHeaderView, QLabel
from qfluentwidgets import TableWidget, CardWidget, ScrollArea, setFont


class HelpInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("HelpInterface")
        self.init_ui()


    def init_ui(self):
        # 创建主窗口的垂直布局
        main_layout = QVBoxLayout(self)

        # --- 创建顶部固定显示区域 ---
        card_widget = CardWidget(self)
        buttons_layout = QHBoxLayout(card_widget)

        # 添加固定显示的内容
        buttons_layout.addWidget(self.create_fixed_area())

        # --- 创建滚动区域 ---
        scroll_area = ScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


        # 创建用于放置表格的垂直布局
        tables_layout = QVBoxLayout()

        # 添加表格及其标题
        tables_layout.addWidget(self.create_table_with_title("高级搜索语法", self.create_advanced_search_table(self)))
        tables_layout.addWidget(self.create_table_with_title("基础类", self.create_basic_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title("标记类", self.create_tags_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title("协议类", self.create_protocol_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title("网站类", self.create_website_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title("地理位置", self.create_location_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title("证书类", self.create_certificate_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title("时间类", self.create_time_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title("独立IP语法", self.create_ip_class_table(self)))

        # 创建一个容器部件，将表格布局设置给它
        container_widget = QWidget()
        container_widget.setLayout(tables_layout)

        # 将容器部件设置到滚动区域内
        scroll_area.setWidget(container_widget)

        # 将顶部区域和滚动区域添加到主布局中
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(card_widget)
        main_layout.addWidget(scroll_area)


    def create_fixed_area(self):
        """
        创建固定显示区域的内容。
        :return: 固定区域的小部件
        """
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        # 这里可以放置任何你想固定显示的控件
        from PyQt6.QtWidgets import QLabel
        label = QLabel("Fofa 官方查询语法参考", widget)
        setFont(label, 20)
        layout.addWidget(label)

        return widget

    def create_table_with_title(self, title, table):
        """
        创建一个带标题和表格的组合部件
        :param title: 表格标题
        :param table: 表格组件
        :return: 包含标题和表格的部件
        """
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        # 创建标题标签
        title_label = QLabel(title, widget)
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title_label)

        # 将表格添加到布局中
        layout.addWidget(table)

        return widget

    def create_advanced_search_table(self, parent):
        """
        创建一个展示高级搜索语法的表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(7)
        table.setColumnCount(5)
        table.setFixedHeight(250)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['=', ' 匹配，="" 时，可查询不存在字段或者值为空的情况。', '✓', '✓', '✓'],
            ['==', ' 完全匹配，=="" 时，可查询存在且值为空的情况。', '✓', '✓', '✓'],
            ['&&', ' 与 ',  '✓', '✓', '✓'],
            ['||', ' 或 ',  '✓', '✓', '✓'],
            ['!=', ' 不匹配，!="" 时，可查询值不为空的情况。', '✓', '✓', '✓'],
            ['=', ' 模糊匹配，使用或者？进行搜索，比如 banner*="mys??" (个人版及以上可用)。', '✓', '✓', '✓'],
            ['()', ' 确认查询优先级，括号内容优先级最高。', '✓', '✓', '✓']
        ]

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['逻辑连接符', '具体含义', '=', '!=', '*='])
        table.setFixedHeight(305)
        return table

    def create_basic_class_table(self, parent):
        """
        创建一个展示基础类的表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(14)
        table.setColumnCount(6)
        # table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        data = [
            ['ip', 'ip="1.1.1.1"', '通过单一 IPv4 地址进行查询', '✓', '✓', '-'],
            ['ip', 'ip="220.181.111.1/24"', '通过 IPv4 C 段进行查询', '✓', '✓', '-'],
            ['ip', 'ip="2600:9000:202a:2600:18:4ab7:f600:93a1"', ' 通过单一 Ipv6 地址进行查询 ', '✓', '✓', '-'],
            ['port', 'port="6379"', '通过端口号进行查询', '✓', '✓', '✓'],
            ['domain', 'domain="qq.com"', '通过根域名进行查询', '✓', '✓', '✓'],
            ['host', 'host=".fofa.info"', '通过主机名进行查询', '✓', '✓', '✓'],
            ['os', 'os="centos"', '通过操作系统进行查询', '✓', '✓', '✓'],
            ['server', 'server="Microsoft-IIS/10"', '通过服务器进行查询', '✓', '✓', '✓'],
            ['asn', 'asn="19551"', ' 通过自治系统号进行搜索', '✓', '✓', '✓'],
            ['org', 'org="LLC Baxet"', '通过所属组织进行查询', '✓', '✓', '✓'],
            ['is_domain', 'is_domain=true', '筛选拥有域名的资产', '✓', '-', '-'],
            ['is_domain', 'is_domain=false', '筛选没有域名的资产', '✓', '-', '-'],
            ['is_ipv6', 'is_ipv6=true', '筛选是 ipv6 的资产', '✓', '-', '-'],
            ['is_ipv6', 'is_ipv6=false', '筛选是 ipv4 的资产', '✓', '-', '-']
        ]
        table.setSpan(0, 0, 3, 1)
        table.setSpan(10, 0, 2, 1)
        table.setSpan(11, 0, 2, 1)
        table.setSpan(12, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['语法', '例句', '用途说明', '=', '!=', '*='])
        table.setFixedHeight(570)
        return table

    def create_tags_class_table(self, parent):
        """
        创建一个展示标记类的表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(13)
        table.setColumnCount(6)
        table.setFixedHeight(550)
        # table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['app', 'app="Microsoft-Exchange"', '通过FOFA整理的规则进行查询', '✓', '-', '-'],
            ['fid', 'fid="sSXXGNUO2FefBTcCLIT/2Q=="', '通过FOFA聚合的站点指纹进行查询', '✓', '✓', '-'],
            ['product', 'product="NGINX"', '通过FOFA标记的产品名进行查询', '✓', '✓', '-'],
            ['category', 'category="服务"', '通过FOFA标记的分类进行查询', '✓', '✓', '-'],
            ['type', 'type="service"', '筛选协议资产', '✓', '-', '-'],
            ['type', 'type="subdomain"', '筛选服务（网站类）资产', '✓', '-', '-'],
            ['cloud_name', 'cloud_name="Aliyundun"', '通过云服务商进行查询', '✓', '✓', '✓'],
            ['is_cloud', 'is_cloud=true', '筛选是云服务的资产', '✓', '-', '-'],
            ['is_cloud', 'is_cloud=false', '筛选不是云服务的资产', '✓', '-', '-'],
            ['is_fraud', 'is_fraud=true', '筛选是仿冒垃圾站群的资产 （专业版及以上）', '✓', '-', '-'],
            ['is_fraud', 'is_fraud=false', '筛选不是仿冒垃圾站群的资产（已默认筛选）', '✓', '-', '-'],
            ['is_honeypot', 'is_honeypot=true', '筛选是蜜罐的资产 （专业版及以上）', '✓', '-', '-'],
            ['is_honeypot', 'is_honeypot=false', '筛选不是蜜罐的资产（已默认筛选）', '✓', '-', '-']
        ]

        table.setSpan(4, 0, 2, 1)
        table.setSpan(7, 0, 2, 1)
        table.setSpan(9, 0, 2, 1)
        table.setSpan(11, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['语法', '例句', '用途说明', '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table

    def create_protocol_class_table(self, parent):
        """
        创建一个展示协议类的表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(4)
        table.setColumnCount(6)
        table.setFixedHeight(200)
        # table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['protocol', 'protocol="quic"', '通过协议名称进行查询', '✓', '✓', '✓'],
            ['banner', 'banner="users"', '通过协议返回信息进行查询', '✓', '✓', '✓'],
            ['base_protocol', 'base_protocol="udp"', '查询传输层为udp协议的资产', '✓', '✓', '-'],
            ['base_protocol', 'base_protocol="tcp"', '查询传输层为tcp协议的资产', '✓', '✓', '-']
        ]
        table.setSpan(2, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['语法', '例句', '用途说明', '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table

    def create_website_class_table(self, parent):
        """
        创建一个展示网站类的表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(13)
        table.setColumnCount(6)
        table.setFixedHeight(550)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['title', 'title="beijing"', ' 通过网站标题进行查询 ', '✓', '✓', '✓'],
            ['header', 'header="elastic"', ' 通过响应标头进行查询 ', '✓', '✓', '✓'],
            ['header_hash', 'header_hash="1258854265"', ' 通过 http/https 响应头计算的 hash 值进行查询 （个人版及以上）',
             '✓', '✓', '✓'],
            ['body', 'body="网络空间测绘"', ' 通过 HTML 正文进行查询 ', '✓', '✓', '-'],
            ['body_hash', 'body_hash="-2090962452"', ' 通过 HTML 正文计算的 hash 值进行查询 ', '✓', '✓', '-'],
            ['js_name', 'js_name="js/jquery.js"', ' 通过 HTML 正文包含的 JS 进行查询 ', '✓', '✓', '✓'],
            ['js_md5', 'js_md5="82ac3f14327a8b7ba49baa208d4eaa15"', ' 通过 JS 源码进行查询 ', '✓', '✓', '✓'],
            ['cname', 'cname="ap21.inst.siteforce.com"', ' 通过别名记录进行查询 ', '✓', '✓', '✓'],
            ['cname_domain', 'cname_domain="siteforce.com"', ' 通过别名记录解析的主域名进行查询 ', '✓', '✓', '✓'],
            ['icon_hash', 'icon_hash="-247388890"', ' 通过网站图标的 hash 值进行查询 ', '✓', '✓', '-'],
            ['status_code', 'status_code="402"', ' 筛选服务状态为 402 的服务（网站）资产 ', '✓', '✓', '-'],
            ['icp', 'icp="京 ICP 证 030173 号"', ' 通过 HTML 正文包含的 ICP 备案号进行查询 ', '✓', '✓', '✓'],
            ['sdk_hash', 'sdk_hash=="Mkb4Ms4R96glv/T6TRzwPWh3UDatBqeF"',
             ' 通过网站嵌入的第三方代码计算的 hash 值进行查询 （商业版及以上）', '✓', '✓', '-']
        ]

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['语法', '例句', '用途说明', '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table

    def create_location_class_table(self, parent):
        """
        创建地理位置的表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(5)
        table.setColumnCount(6)
        table.setFixedHeight(235)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['country', 'country="CN"', ' 通过国家的简称代码进行查询 ', '✓', '✓', '-'],
            ['country', 'country="中国"', ' 通过国家中文名称进行查询 ', '✓', '✓', '-'],
            ['region', 'region="Zhejiang"', ' 通过省份 / 地区英文名称进行查询 ', '✓', '✓', '-'],
            ['region', 'region="浙江"', ' 通过省份 / 地区中文名称进行查询（仅支持中国地区）', '✓', '✓', '-'],
            ['city', 'city="Hangzhou"', ' 通过城市英文名称进行查询 ', '✓', '✓', '-']
        ]
        table.setSpan(0, 0, 2, 1)
        table.setSpan(2, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['语法', '例句', '用途说明', '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table

    def create_certificate_class_table(self, parent):
        """
        创建证书类的表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(19)
        table.setColumnCount(6)
        table.setFixedHeight(775)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['cert', 'cert="baidu"', ' 通过证书进行查询 ', '✓', '✓', '✓'],
            ['cert.subject', 'cert.subject="Oracle Corporation"', ' 通过证书的持有者进行查询 ', '✓', '✓', '✓'],
            ['cert.issuer', 'cert.issuer="DigiCert"', ' 通过证书的颁发者进行查询 ', '✓', '✓', '✓'],
            ['cert.subject.org', 'cert.subject.org="Oracle Corporation"', ' 通过证书持有者的组织进行查询 ', '✓', '✓',
             '✓'],
            ['cert.subject.cn', 'cert.subject.cn="baidu.com"', ' 通过证书持有者的通用名称进行查询 ', '✓', '✓', '✓'],
            ['cert.issuer.org', 'cert.issuer.org="cPanel, Inc."', ' 通过证书颁发者的组织进行查询 ', '✓', '✓', '✓'],
            ['cert.issuer.cn', 'cert.issuer.cn="Synology Inc. CA"', ' 通过证书颁发者的通用名称进行查询 ', '✓', '✓',
             '✓'],
            ['cert.domain', 'cert.domain="huawei.com"', ' 通过证书持有者的根域名进行查询 ', '✓', '✓', '✓'],
            ['cert.is_equal', 'cert.is_equal=true', ' 筛选证书颁发者和持有者匹配的资产 （个人版及以上）', '✓', '-', '-'],
            ['cert.is_equal', 'cert.is_equal=false', ' 筛选证书颁发者和持有者不匹配的资产 （个人版及以上）', '✓', '-',
             '-'],
            ['cert.is_valid', 'cert.is_valid=true', ' 筛选证书是有效证书的资产 （个人版及以上）', '✓', '-', '-'],
            ['cert.is_valid', 'cert.is_valid=false', ' 筛选证书是无效证书的资产 （个人版及以上）', '✓', '-', '-'],
            ['cert.is_match', 'cert.is_match=true', ' 筛选证书和域名匹配的资产 （个人版及以上）', '✓', '-', '-'],
            ['cert.is_match', 'cert.is_match=false', ' 筛选证书和域名不匹配的资产 （个人版及以上）', '✓', '-', '-'],
            ['cert.is_expired', 'cert.is_expired=true', ' 筛选证书已过期的资产 （个人版及以上）', '✓', '-', '-'],
            ['cert.is_expired', 'cert.is_expired=false', ' 筛选证书未过期的资产 （个人版及以上）', '✓', '-', '-'],
            ['jarm', 'jarm="2ad2ad0002ad2ad22c2ad2ad2ad2ad2eac92ec34bcc0cf7520e97547f83e81"',
             ' 通过 JARM 指纹进行查询 ', '✓', '✓', '✓'],
            ['tls.version', 'tls.version="TLS 1.3"', ' 通过 tls 的协议版本进行查询 ', '✓', '✓', '-'],
            ['tls.ja3s', 'tls.ja3s="15af977ce25de452b96affa2addb1036"', ' 通过 tls 的 ja3s 指纹进行查询 ', '✓', '✓',
             '✓']
        ]

        table.setSpan(8, 0, 2, 1)
        table.setSpan(10, 0, 2, 1)
        table.setSpan(12, 0, 2, 1)
        table.setSpan(14, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['语法', '例句', '用途说明', '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table

    def create_time_class_table(self, parent):
        """
        创建时间类的表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(3)
        table.setColumnCount(6)
        table.setFixedHeight(154)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['after', 'after="2023-01-01"', ' 筛选某一时间之后有更新的资产 ', '✓', '-', '-'],
            ['before', 'before="2023-12-01"', ' 筛选某一时间之前有更新的资产 ', '✓', '-', '-'],
            ['after&before', 'after="2023-01-01" && before="2023-12-01"', ' 筛选某一时间区间有更新的资产 ', '✓', '-', '-']
        ]

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['语法', '例句', '用途说明', '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table

    def create_ip_class_table(self, parent):
        """
        创建独立IP语法表格
        """
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setRowCount(9)
        table.setColumnCount(6)
        table.setFixedHeight(390)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['port_size', 'port_size="6"', ' 筛选开放端口数量等于 6 个的独立 IP （个人版及以上）', '✓', '✓', '-'],
            ['port_size_gt', 'port_size_gt="6"', ' 筛选开放端口数量大于 6 个的独立 IP （个人版及以上）', '✓', '-', '-'],
            ['port_size_lt', 'port_size_lt="12"', ' 筛选开放端口数量小于 12 个的独立 IP （个人版及以上）', '✓', '-', '-'],
            ['ip_ports', 'ip_ports="80,161"', ' 筛选同时开放不同端口的独立 IP', '✓', '-', '-'],
            ['ip_country', 'ip_country="CN"', ' 通过国家的简称代码进行查询独立 IP', '✓', '-', '-'],
            ['ip_region', 'ip_region="Zhejiang"', ' 通过省份 / 地区英文名称进行查询独立 IP', '✓', '-', '-'],
            ['ip_city', 'ip_city="Hangzhou"', ' 通过城市英文名称进行查询独立 IP', '✓', '-', '-'],
            ['ip_after', 'ip_after="2021-03-18"', ' 筛选某一时间之后有更新的独立 IP', '✓', '-', '-'],
            ['ip_before', 'ip_before="2019-09-09"', ' 筛选某一时间之前有更新的独立 IP', '✓', '-', '-']
        ]

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels(['语法', '例句', '用途说明', '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = HelpInterface()
#     window.setWindowTitle("Fofa 搜索语法帮助")
#     window.setFixedSize(900, 600)  # 设置窗口固定大小
#     window.show()
#     sys.exit(app.exec())
