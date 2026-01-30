# OCR 数值检测上位机（Qt + PaddleOCR）

本项目是一个基于 **PyQt5 + PaddleOCR** 的桌面上位机工具，用于：

- 在屏幕指定区域进行 **OCR 文本识别**
- 从 OCR 结果中 **提取数值**
- 根据 **阈值规则** 触发 **串口 HEX 指令**
- 支持 **单位辅助判断**，提高监测对象稳定性
- 适用于电源、电流、电压、仪表等自动化测试场景

---

## ✨ 功能特性

- 🖥 **可视化 GUI（PyQt5）**
- 🖱 **鼠标拖拽选择监测区域**
- 🔍 **基于 PaddleOCR 的中文/英文 OCR**
- 🔢 **自动提取文本中的数值**
- 📏 **阈值触发规则（>= 阈值）**
- 🔌 **串口通信（HEX 指令发送）**
- 🧠 **单位辅助判断（防止监测文本漂移）**
- 🧩 **模块化工程结构，易扩展**

---

## 📁 项目结构

```text
ocr-monitor/
├── main.py                     # 程序入口
├── ui/                         # UI 层
│   ├── widgets/                # 纯控件定义
│   │   ├── main_view.py
│   │   └── region_selector.py
│   ├── controller/             # UI 事件 & 调度
│   │   └── main_controller.py
│   └── __init__.py
│
├── logic/                      # 业务逻辑（无 UI）
│   ├── value_parser.py         # 数值提取
│   ├── unit_assist.py          # 单位辅助判断
│   ├── trigger_rule.py         # 阈值触发规则
│   └── __init__.py
│
├── ocr/                        # OCR 子系统
│   ├── base.py                 # OCR 管理器
│   ├── backend.py              # OCR 接口定义
│   └── paddle_ocr.py           # PaddleOCR 实现
│
├── hw_serial/                  # 串口通信
│   └── serial_comm.py
│
├── utils/                      # 工具模块
│   ├── logger.py               # 日志系统
│   └── __init__.py
│
├── requirements.txt            # 依赖清单
└── README.md
````

---

## 🧰 运行环境

* **Python**: 3.10
* **操作系统**: Windows 11
* **显示环境**: 需要桌面（非纯命令行）

---

## 📦 安装依赖

### 1️⃣ 创建虚拟环境（推荐）

```bash
conda create -n ocr-monitor python=3.10
conda activate ocr-monitor
```

### 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

> ⚠️ **关于 PaddleOCR**
>
> * `paddlepaddle` CPU / GPU 版本不同
> * GPU 用户请根据 CUDA 版本参考官方文档安装
> * 默认 requirements 中为 **CPU 版本**

---

## ▶️ 启动程序

### 推荐启动方式（包模式）

```bash
cd ocr-monitor
python  main.py
```

> 所有模块应从 `main.py` 作为入口启动

---

## 🧭 使用说明

1. 启动程序
2. 点击 **“选择区域”**，用鼠标框选需要监测的屏幕区域
3. 点击 **“开始”**，程序会周期性进行 OCR
4. 在 OCR 文本列表中：

   * 点击选择要监测的文本
5. 设置：

   * 阈值
   * 单位（如 `A` / `V`）
   * HEX 指令
   * 发送次数上限
6. 当检测到数值 **≥ 阈值**：

   * 自动通过串口发送 HEX 指令

---

## 🧠 单位辅助判断说明

当开启 **单位辅助判断** 时：

* 如果当前选中文本中包含单位 → 认为监测正确
* 如果在其他 OCR 文本中发现单位 → 提示监测对象可能发生偏移
* 如果未发现单位 → 提示 OCR 识别异常或数据丢失

⚠️ 单位辅助 **不会影响触发逻辑，仅作为提示**

---

## 🧩 设计说明

* **UI 与业务逻辑完全解耦**
* **OCR / 串口 / 规则模块独立**
* `QApplication.processEvents()` 已被避免
  → 使用 Qt 信号机制保证 UI 稳定性
* Logger 使用 class 封装，便于后续扩展文件日志

---

## 🔮 后续可扩展方向

* OCR 结果稳定性评分 & 自动锁定监测文本
* 多区域 / 多监测点支持
* 规则链（区间、上下限、组合条件）
* 日志导出 CSV / TXT
* 串口 ACK / 超时 / 队列机制
* OCR 后端切换（EasyOCR / Tesseract）

---

## 📄 License

本项目为内部工具 / 学习工程示例。
如需开源或商业使用，请自行补充 License。

---

## 致谢

* [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
* PyQt5
* pyserial
