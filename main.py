# Copyright (c) 2026.1 sxz3736
# Licensed under the MIT License

import sys
from PyQt5.QtWidgets import QApplication

from ui import MainView, MainController


def main():
    app = QApplication(sys.argv)

    # 创建 UI（只负责控件）
    view = MainView()

    # 创建 Controller（绑定事件 + 业务调度）
    controller = MainController(view)

    # 显示主窗口
    view.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
