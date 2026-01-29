# ui/widgets/main_view.py
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("OCR 数值检测上位机")
        self.resize(1100, 760)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # ===== 控制栏 =====
        bar = QHBoxLayout()
        self.btn_select_region = QPushButton("选择区域")
        self.btn_serial = QPushButton("连接串口")
        self.btn_start = QPushButton("开始")
        self.btn_stop = QPushButton("停止")

        bar.addWidget(self.btn_select_region)
        bar.addWidget(self.btn_serial)
        bar.addWidget(self.btn_start)
        bar.addWidget(self.btn_stop)
        layout.addLayout(bar)

        # ===== OCR 列表 =====
        layout.addWidget(QLabel("OCR 文本列表（点击选择检测对象）："))
        self.list_texts = QListWidget()
        layout.addWidget(self.list_texts)

        # ===== 参数区 =====
        param = QHBoxLayout()

        param.addWidget(QLabel("阈值:"))
        self.spin_threshold = QDoubleSpinBox()
        self.spin_threshold.setRange(-1e9, 1e9)
        self.spin_threshold.setValue(5.0)
        param.addWidget(self.spin_threshold)

        param.addWidget(QLabel("单位输入:"))
        self.edit_unit = QLineEdit("A")
        self.edit_unit.setMaximumWidth(60)
        param.addWidget(self.edit_unit)

        self.chk_unit_assist = QCheckBox("根据单位辅助判断当前文本是否正确")
        param.addWidget(self.chk_unit_assist)

        param.addWidget(QLabel("触发HEX:"))
        self.edit_hex = QLineEdit("AA 55 01 02")
        param.addWidget(self.edit_hex)

        param.addWidget(QLabel("HEX上限:"))
        self.spin_hex_limit = QSpinBox()
        self.spin_hex_limit.setRange(1, 100000)
        self.spin_hex_limit.setValue(100)
        param.addWidget(self.spin_hex_limit)

        self.btn_clear_hex = QPushButton("清空发送计数")
        param.addWidget(self.btn_clear_hex)

        layout.addLayout(param)

        # ===== 日志 =====
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(240)
        layout.addWidget(self.log_box)
