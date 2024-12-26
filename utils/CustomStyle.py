# 通用按钮样式
BUTTON_STYLE = """
QPushButton {
    border: none;
    padding: 5px 10px;
    font-family: 'Segoe UI', 'Microsoft YaHei';
    font-size: 14px;
    color: white;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
}
QPushButton:pressed {
    background-color: rgba(255, 255, 255, 0.2);
}
"""

ADD_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #0d6efd;
}
QPushButton:hover {
    background-color: #0b5ed7;
}
QPushButton:pressed {
    background-color: #0a58ca;
}
"""

DELETE_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #dc3545;
}
QPushButton:hover {
    background-color: #bb2d3b;
}
QPushButton:pressed {
    background-color: #b02a37;
}
"""

BATCH_DELETE_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #fd7e14;
}
QPushButton:hover {
    background-color: #e96b10;
}
QPushButton:pressed {
    background-color: #dc680f;
}
"""

UPDATE_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #198754;
}
QPushButton:hover {
    background-color: #157347;
}
QPushButton:pressed {
    background-color: #146c43;
}
"""

IMPORT_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #6f42c1;
}
QPushButton:hover {
    background-color: #5936a2;
}
QPushButton:pressed {
    background-color: #4a2d8e;
}
"""

EXPORT_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #20c997;
}
QPushButton:hover {
    background-color: #1aa179;
}
QPushButton:pressed {
    background-color: #198b6d;
}
"""

IMPORT_BUTTON_STYLE = BUTTON_STYLE + """
QPushButton {
    background-color: #6f42c1;
}
QPushButton:hover {
    background-color: #5936a2;
}
QPushButton:pressed {
    background-color: #4a2d8e;
}
"""

