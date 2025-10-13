from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QLabel
from qfluentwidgets import TableWidget, CardWidget, ScrollArea
from ..common.style_sheet import StyleSheet
from ..common.config import cfg, Language


class HelpInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("helpInterface")
        StyleSheet.HELP_INTERFACE.apply(self)
        self.init_ui()


    def init_ui(self):
        # 创建主窗口的垂直布局
        main_layout = QVBoxLayout(self)

        # --- 创建顶部固定显示区域 ---
        self.titleLabel = QLabel(self)
        card_widget = CardWidget(self)
        buttons_layout = QHBoxLayout()

        # 添加固定显示的内容
        buttons_layout.addWidget(self.create_fixed_area())

        # --- 创建滚动区域 ---
        scroll_area = ScrollArea(self)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


        # 创建用于放置表格的垂直布局
        tables_layout = QVBoxLayout()

        # 添加表格及其标题
        tables_layout.addWidget(self.create_table_with_title(self.tr("Advanced Search"), self.create_advanced_search_table(self)))
        tables_layout.addWidget(self.create_table_with_title(self.tr("General"), self.create_basic_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title(self.tr("Special Label"), self.create_tags_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title(self.tr("None Web"), self.create_protocol_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title(self.tr("Website"), self.create_website_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title(self.tr("Location"), self.create_location_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title(self.tr("Certificate"), self.create_certificate_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title(self.tr("Last Update Time"), self.create_time_class_table(self)))
        tables_layout.addWidget(self.create_table_with_title(self.tr("Unique IP View"), self.create_ip_class_table(self)))

        # 创建一个容器部件，将表格布局设置给它
        container_widget = QWidget()
        container_widget.setLayout(tables_layout)

        # 将容器部件设置到滚动区域内
        scroll_area.setWidget(container_widget)

        # 将顶部区域和滚动区域添加到主布局中
        main_layout.addLayout(buttons_layout)
        # main_layout.addLayout(self.titleLabel)
        main_layout.addWidget(card_widget)
        main_layout.addWidget(scroll_area)


    def create_fixed_area(self):
        """
        创建固定显示区域的内容。
        :return: 固定区域的小部件
        """
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        widget.setObjectName("fixedAreaWidget")


        # 这里可以放置任何你想固定显示的控件
        label = QLabel(self.tr("Fofa Official query syntax reference"), widget)
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
        table.setColumnCount(2)
        table.setFixedHeight(250)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        data = [
            ['=', self.tr('Equal matching. When syntax="", it can be queried that the field does not exist or the value is empty.')],
            ['==', self.tr('Complete matching. When syntax=="", it can be queried that field dose exist or the value is empty.')],
            ['&&', self.tr('And')],
            ['||', self.tr('Or')],
            ['!=', self.tr('Mismatching, When syntax!="", it can be queried that the value is not empty.')],
            ['=', self.tr('Fuzzy Search，Use * or? to query, such as banner*="mys??" (Member and above).')],
            ['()', self.tr('Confirm the query priority. The parentheses have the highest priority.')]
        ]

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels([self.tr('Logic Operator'), self.tr('Description')])
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
            ['ip', 'ip="1.1.1.1"', self.tr('Query by a IPv4 address.'), '✓', '✓', '-'],
            ['ip', 'ip="220.181.111.1/24"', self.tr('Query by IPv4 C segment.'), '✓', '✓', '-'],
            ['ip', 'ip="2600:9000:202a:2600:18:4ab7:f600:93a1"', self.tr('Query by a IPv6 address.'), '✓', '✓', '-'],
            ['port', 'port="6379"', self.tr('Query by open port number.'), '✓', '✓', '✓'],
            ['domain', 'domain="qq.com"', self.tr('Query by domain.'), '✓', '✓', '✓'],
            ['host', 'host=".fofa.info"', self.tr('Query by hostname.'), '✓', '✓', '✓'],
            ['os', 'os="centos"', self.tr('Query by operating system.'), '✓', '✓', '✓'],
            ['server', 'server="Microsoft-IIS/10"', self.tr('Query by server.'), '✓', '✓', '✓'],
            ['asn', 'asn="19551"', self.tr('Query by autonomous system number.'), '✓', '✓', '✓'],
            ['org', 'org="LLC Baxet"', self.tr('Query by affiliated organization.'), '✓', '✓', '✓'],
            ['is_domain', 'is_domain=true', self.tr('Filter assets that own a domain.'), '✓', '-', '-'],
            ['is_domain', 'is_domain=false', self.tr('Filter assets that do not own a domain.'), '✓', '-', '-'],
            ['is_ipv6', 'is_ipv6=true', self.tr('Filter assets that are IPv6.'), '✓', '-', '-'],
            ['is_ipv6', 'is_ipv6=false', self.tr('Filter assets that are IPv4.'), '✓', '-', '-']
        ]
        table.setSpan(0, 0, 3, 1)
        table.setSpan(10, 0, 2, 1)
        table.setSpan(11, 0, 2, 1)
        table.setSpan(12, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels([self.tr('Syntax'), self.tr('Example'), self.tr('Description'), '=', '!=', '*='])
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
            ['app', 'app="Microsoft-Exchange"', self.tr('Query by fingerprint organized by FOFA.'), '✓', '-', '-'],
            ['fid', 'fid="sSXXGNUO2FefBTcCLIT/2Q=="', self.tr('Query by FeatureID aggregated by FOFA.'), '✓', '✓', '-'],
            ['product', 'product="NGINX"', self.tr('Query by product names tagged by FOFA.'), '✓', '✓', '-'],
            ['category', 'category="服务"', self.tr('Query by categories marked by FOFA	'), '✓', '✓', '-'],
            ['type', 'type="service"', self.tr('Filter protocol assets.'), '✓', '-', '-'],
            ['type', 'type="subdomain"', self.tr('Filter website type assets.'), '✓', '-', '-'],
            ['cloud_name', 'cloud_name="Aliyundun"', self.tr('Query by cloud service provider.'), '✓', '✓', '✓'],
            ['is_cloud', 'is_cloud=true', self.tr('Filter assets that are cloud services.'), '✓', '-', '-'],
            ['is_cloud', 'is_cloud=false', self.tr('Filter assets that are not cloud services.'), '✓', '-', '-'],
            ['is_fraud', 'is_fraud=true', self.tr('Filter assets that are phishing spam site. (Professional and above)'), '✓', '-', '-'],
            ['is_fraud', 'is_fraud=false', self.tr('Filter assets that are not phishing spam sites (default filtered)'), '✓', '-', '-'],
            ['is_honeypot', 'is_honeypot=true', self.tr('Filter assets that are honeypots. (Professional and above)'), '✓', '-', '-'],
            ['is_honeypot', 'is_honeypot=false', self.tr('Filter assets that are not honeypots (default filtered).'), '✓', '-', '-']
        ]

        table.setSpan(4, 0, 2, 1)
        table.setSpan(7, 0, 2, 1)
        table.setSpan(9, 0, 2, 1)
        table.setSpan(11, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels([self.tr('Syntax'), self.tr('Example'), self.tr('Description'), '=', '!=', '*='])
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
            ['protocol', 'protocol="quic"', self.tr('Query by protocol name.'), '✓', '✓', '✓'],
            ['banner', 'banner="users"', self.tr('Query by protocol response information.'), '✓', '✓', '✓'],
            ['base_protocol', 'base_protocol="udp"', self.tr('Query assets with UDP as the transport layer protocol.'), '✓', '✓', '-'],
            ['base_protocol', 'base_protocol="tcp"', self.tr('Query assets with TCP as the transport layer protocol.'), '✓', '✓', '-']
        ]
        table.setSpan(2, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels([self.tr('Syntax'), self.tr('Example'), self.tr('Description'), '=', '!=', '*='])
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
            ['title', 'title="beijing"', self.tr('Query by website title.'), '✓', '✓', '✓'],
            ['header', 'header="elastic"', self.tr('Query by response headers.'), '✓', '✓', '✓'],
            ['header_hash', 'header_hash="1258854265"', self.tr('Query by hash value calculated from http/https response headers. (Personal and above)'), '✓', '✓', '✓'],
            ['body', 'body="网络空间测绘"', self.tr('Query by HTML body.'), '✓', '✓', '-'],
            ['body_hash', 'body_hash="-2090962452"', self.tr('Query by hash value calculated from HTML body.'), '✓', '✓', '-'],
            ['js_name', 'js_name="js/jquery.js"', self.tr('Query by JS included in HTML body.'), '✓', '✓', '✓'],
            ['js_md5', 'js_md5="82ac3f14327a8b7ba49baa208d4eaa15"', self.tr('Query by JS_md5.'), '✓', '✓', '✓'],
            ['cname', 'cname="ap21.inst.siteforce.com"', self.tr('Query by CName.'), '✓', '✓', '✓'],
            ['cname_domain', 'cname_domain="siteforce.com"', self.tr('Query by main domain resolved from CName.'), '✓', '✓', '✓'],
            ['icon_hash', 'icon_hash="-247388890"', self.tr('Query by hash value of favicon.'), '✓', '✓', '-'],
            ['status_code', 'status_code="402"', self.tr('Filter services with a status code of 402 (website assets)'), '✓', '✓', '-'],
            ['icp', 'icp="京ICP证030173号"', self.tr('Query by ICP number included in HTML body'), '✓', '✓', '✓'],
            ['sdk_hash', 'sdk_hash=="Mkb4Ms4R96glv/T6TRzwPWh3UDatBqeF"', self.tr('Query by hash value calculated from third-party code embedded in the website (Business and above)'), '✓', '✓', '-']
        ]

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels([self.tr('Syntax'), self.tr('Example'), self.tr('Description'), '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table

    def create_location_class_table(self, parent):
        """
        创建地理位置的表格
        """

        # 获取当前语言的表格数据
        current_language = cfg.language.value

        # 如果是 Language.AUTO，根据系统语言来判断
        if current_language == Language.AUTO:
            system_locale = QLocale.system().language()
            if system_locale == QLocale.Language.Chinese:
                # 如果系统语言是中文（简体或繁体），使用简体中文数据
                current_language = Language.CHINESE_SIMPLIFIED
            else:
                # 如果系统语言是英文，使用英文数据
                current_language = Language.ENGLISH

        # 语言对应的数据
        data_dict = {
            Language.CHINESE_SIMPLIFIED: [
                ['country', 'country="CN"', '通过国家的简称代码进行查询', '✓', '✓', '-'],
                ['country', 'country="中国"', '通过国家中文名称进行查询', '✓', '✓', '-'],
                ['region', 'region="Zhejiang"', '通过省份/地区英文名称进行查询', '✓', '✓', '-'],
                ['region', 'region="浙江"', '通过省份/地区中文名称进行查询（仅支持中国地区）', '✓', '✓', '-'],
                ['city', 'city="Hangzhou"', '通过城市英文名称进行查询', '✓', '✓', '-']
            ],
            Language.CHINESE_TRADITIONAL: [
                ['country', 'country="CN"', '透過國家的簡稱代碼進行查詢', '✓', '✓', '-'],
                ['country', 'country="中國"', '透過國家中文名稱進行查詢', '✓', '✓', '-'],
                ['region', 'region="Zhejiang"', '透過省份/地區英文名稱進行查詢', '✓', '✓', '-'],
                ['region', 'region="浙江"', '透過省份/地區中文名稱進行查詢（僅支持中國地區）', '✓', '✓', '-'],
                ['city', 'city="Hangzhou"', '透過城市英文名稱進行查詢', '✓', '✓', '-']
            ],
            Language.ENGLISH: [
                ['country', 'country="US"', 'Query by country code.', '✓', '✓', '-'],
                ['region', 'region="New York"', 'Query by province/region name.', '✓', '✓', '-'],
                ['city', 'city="Hangzhou"', 'Query by city name.', '✓', '✓', '-']
            ]
        }

        # 获取对应语言的数据
        data = data_dict.get(current_language, [])

        # 创建表格
        table = TableWidget(parent)
        table.setBorderVisible(True)
        table.setBorderRadius(8)
        table.setColumnCount(6)

        # 根据当前语言设置表格高度
        if current_language == Language.ENGLISH:
            table.setFixedHeight(153)  # 英文设置为153
        else:
            table.setFixedHeight(235)  # 中文（包括简体和繁体）设置为235

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.setRowCount(len(data))

        # 填充表格数据
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        # 设置表头
        table.setHorizontalHeaderLabels(
            [self.tr('Syntax'), self.tr('Example'), self.tr('Description'), '=', '!=', '*='])

        # 自动调整行高
        table.resizeRowsToContents()

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
            ['cert', 'cert="baidu"', self.tr('Query by certificate.'), '✓', '✓', '✓'],
            ['cert.subject', 'cert.subject="Oracle Corporation"', self.tr('Query by certificate subject.'), '✓', '✓', '✓'],
            ['cert.issuer', 'cert.issuer="DigiCert"', self.tr('Query by certificate issuer.'), '✓', '✓', '✓'],
            ['cert.subject.org', 'cert.subject.org="Oracle Corporation"', self.tr("Query by certificate subject's organization."), '✓', '✓', '✓'],
            ['cert.subject.cn', 'cert.subject.cn="baidu.com"', self.tr("Query by certificate subject's common name."), '✓', '✓', '✓'],
            ['cert.issuer.org', 'cert.issuer.org="cPanel, Inc."', self.tr("Query by certificate issuer's organization."), '✓', '✓', '✓'],
            ['cert.issuer.cn', 'cert.issuer.cn="Synology Inc. CA"', self.tr("Query by certificate issuer's common name."), '✓', '✓', '✓'],
            ['cert.domain', self.tr('cert.domain="amazon.com"'), self.tr("Query by certificate subject's domain."), '✓', '✓', '✓'],
            ['cert.is_equal', 'cert.is_equal=true', self.tr("Filter assets where certificate issuer matches certificate subject. (Personal and above)"), '✓', '-', '-'],
            ['cert.is_equal', 'cert.is_equal=false', self.tr("Filter assets where certificate issuer does not matches certificate subject. (Personal and above)"), '✓', '-', '-'],
            ['cert.is_valid', 'cert.is_valid=true', self.tr("Filter assets that have valid certificates. (Personal and above)"), '✓', '-', '-'],
            ['cert.is_valid', 'cert.is_valid=false', self.tr("Filter assets that have invalid certificates. (Personal and above)"), '✓', '-', '-'],
            ['cert.is_match', 'cert.is_match=true', self.tr("Filter assets where certificate matches the domain. (Personal and above)"), '✓', '-', '-'],
            ['cert.is_match', 'cert.is_match=false', self.tr("Filter assets where certificate does not match the domain. (Personal and above)"), '✓', '-', '-'],
            ['cert.is_expired', 'cert.is_expired=true', self.tr("Filter assets with expired certificates. (Personal and above)"), '✓', '-', '-'],
            ['cert.is_expired', 'cert.is_expired=false', self.tr("Filter assets with non-expired certificates. (Personal and above)"), '✓', '-', '-'],
            ['jarm', 'jarm="2ad2ad0002ad2ad22c2ad2ad2ad2ad2eac92ec34bcc0cf7520e97547f83e81"', self.tr("Query by JARM fingerprint."), '✓', '✓', '✓'],
            ['tls.version', 'tls.version="TLS 1.3"', self.tr("Query by tls protocol version."), '✓', '✓', '-'],
            ['tls.ja3s', 'tls.ja3s="15af977ce25de452b96affa2addb1036"', self.tr("Query by tls ja3s fingerprint."), '✓', '✓', '✓']
        ]

        table.setSpan(8, 0, 2, 1)
        table.setSpan(10, 0, 2, 1)
        table.setSpan(12, 0, 2, 1)
        table.setSpan(14, 0, 2, 1)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels([self.tr('Syntax'), self.tr('Example'), self.tr('Description'), '=', '!=', '*='])
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
            ['after', 'after="2023-01-01"', self.tr('Filter assets that have been updated after a time.'), '✓', '-', '-'],
            ['before', 'before="2023-12-01"', self.tr('Filter assets that have been updated before a time.'), '✓', '-', '-'],
            ['after&before', 'after="2023-01-01" && before="2023-12-01"', self.tr('Filter assets that have been updated within a time interval.'), '✓', '-', '-']
        ]

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels([self.tr('Syntax'), self.tr('Example'), self.tr('Description'), '=', '!=', '*='])
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
            ['port_size', 'port_size="6"', self.tr("Filter Unique IPs with exactly 6 open ports. (Personal and above)"), '✓', '✓', '-'],
            ['port_size_gt', 'port_size_gt="6"', self.tr("Filter Unique IPs with more than 6 open ports. (Personal and above)"), '✓', '-', '-'],
            ['port_size_lt', 'port_size_lt="12"', self.tr("Filter Unique IPs with less than 12 open ports. (Personal and above)"), '✓', '-', '-'],
            ['ip_ports', 'ip_ports="80,161"', self.tr("Filter Unique IPs that have different ports open."), '✓', '-', '-'],
            ['ip_country', 'ip_country="CN"', self.tr("Query Unique IPs by country code."), '✓', '-', '-'],
            ['ip_region', 'ip_region="Zhejiang"', self.tr("Query Unique IPs by province/region name."), '✓', '-', '-'],
            ['ip_city', 'ip_city="Hangzhou"', self.tr("Query Unique IPs by city name."), '✓', '-', '-'],
            ['ip_after', 'ip_after="2021-03-18"', self.tr("Filter Unique IPs that have been updated after a time"), '✓', '-', '-'],
            ['ip_before', 'ip_before="2019-09-09"', self.tr("Filter Unique IPs that have been updated before a time."), '✓', '-', '-']
        ]

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(item))

        table.setHorizontalHeaderLabels([self.tr('Syntax'), self.tr('Example'), self.tr('Description'), '=', '!=', '*='])
        table.resizeRowsToContents()  # 自动调整行高
        return table


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = HelpInterface()
#     window.setWindowTitle("Fofa 搜索语法帮助")
#     window.setFixedSize(900, 600)  # 设置窗口固定大小
#     window.show()
#     sys.exit(app.exec())
