# ui/controller/main_controller.py
import time
import cv2
import numpy as np
import pyautogui
import re

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QListWidgetItem, QApplication

from ocr.base import OCRManager
from hw_serial.serial_comm import SerialCommunicator
from utils.logger import Logger
from logic.value_parser import extract_value
from logic.unit_assist import unit_assist_check
from logic.trigger_rule import check_and_trigger
from ui.widgets.region_selector import ScreenRegionSelector


class MainController:
    def __init__(self, view):
        self.view = view

        # ===== 核心模块 =====
        self.ocr = OCRManager(backend="paddle", lang="ch")
        self.serial = SerialCommunicator()

        self.timer = QTimer()
        self.timer.timeout.connect(self.recognize_once)

        # ===== 状态 =====
        self.region = None
        self.ocr_results = []
        self.selected_text_id = -1
        self.hex_send_count = 0

        # ===== 日志 =====
        self.logger = Logger(self.view.log_box)

        self._bind_events()

    # ---------- 事件绑定 ----------
    def _bind_events(self):
        self.view.btn_select_region.clicked.connect(self.select_region)
        self.view.btn_serial.clicked.connect(self.toggle_serial)
        self.view.btn_start.clicked.connect(self.start)
        self.view.btn_stop.clicked.connect(self.stop)
        self.view.btn_clear_hex.clicked.connect(self.clear_hex_count)
        self.view.list_texts.itemClicked.connect(self.on_text_selected)

    # ---------- 日志 ----------
    def log(self, msg):
        self.logger.info(msg)


    # ---------- 串口 ----------
    def toggle_serial(self):
        if self.serial.is_connected:
            self.serial.disconnect()
            self.log("串口已断开")
            return

        ports = self.serial.list_ports()
        if not ports:
            self.log("未找到串口")
            return

        if self.serial.connect(ports[0]):
            self.log(f"串口已连接: {ports[0]}")
        else:
            self.log("串口连接失败")

    # ---------- 区域 ----------
    def select_region(self):
        sel = ScreenRegionSelector()
        start = time.time()

        while sel.isVisible():
            QApplication.processEvents()
            if time.time() - start > 10:
                sel.hide()
                return

        if not sel.start_point or not sel.end_point:
            return

        x1 = min(sel.start_point.x(), sel.end_point.x())
        y1 = min(sel.start_point.y(), sel.end_point.y())
        x2 = max(sel.start_point.x(), sel.end_point.x())
        y2 = max(sel.start_point.y(), sel.end_point.y())

        self.region = (x1, y1, x2 - x1, y2 - y1)
        self.log(f"区域设置: {self.region}")

    # ---------- 启停 ----------
    def start(self):
        if not self.region:
            self.log("请先选择区域")
            return
        self.timer.start(1000)
        self.log("开始识别")

    def stop(self):
        self.timer.stop()
        self.log("停止识别")

    # ---------- OCR 主流程 ----------
    def recognize_once(self):
        if not self.region:
            return

        x, y, w, h = self.region
        img = cv2.cvtColor(
            np.array(pyautogui.screenshot(region=(x, y, w, h))),
            cv2.COLOR_RGB2BGR
        )

        self.ocr_results = self.ocr.recognize(img)
        self._update_text_list()

        if self.selected_text_id < 0:
            return

        if self.selected_text_id >= len(self.ocr_results):
            self.log("文本 ID 失效，请重新选择")
            self.selected_text_id = -1
            return

        text = self.ocr_results[self.selected_text_id]["text"]
        value = extract_value(text)

        if value is None:
            self.log("未检测到数值")
            return

        if self.view.chk_unit_assist.isChecked():
            unit_assist_check(
                self.ocr_results,
                self.selected_text_id,
                self.view.edit_unit.text().strip(),
                self.log
            )

        self.hex_send_count = check_and_trigger(
            value,
            self.view.spin_threshold.value(),
            self.serial,
            self.view.edit_hex.text(),
            self.hex_send_count,
            self.view.spin_hex_limit.value(),
            self.log
        )

    # ---------- OCR 列表 ----------
    def _update_text_list(self):
        self.view.list_texts.clear()

        for idx, d in enumerate(self.ocr_results):
            item = QListWidgetItem(
                f"[{idx}] {d['text']} ({d['confidence']:.2f})"
            )
            item.setData(0x0100, idx)
            self.view.list_texts.addItem(item)

        self._update_highlight()

    def on_text_selected(self, item):
        self.selected_text_id = int(item.data(0x0100))
        self._update_highlight()
        self.log(f"用户选择文本 ID={self.selected_text_id}")

    def _update_highlight(self):
        for i in range(self.view.list_texts.count()):
            self.view.list_texts.item(i).setBackground(QColor("white"))

        if 0 <= self.selected_text_id < self.view.list_texts.count():
            self.view.list_texts.item(self.selected_text_id).setBackground(
                QColor(255, 230, 180)
            )

    # ---------- 计数 ----------
    def clear_hex_count(self):
        self.hex_send_count = 0
        self.log("HEX 发送计数已清空")
