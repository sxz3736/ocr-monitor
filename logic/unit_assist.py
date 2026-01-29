# logic/unit_assist.py
import re


def unit_assist_check(
    ocr_results: list,
    base_idx: int,
    user_unit: str,
    log
):
    """
    单位辅助判断（只提示，不影响流程）

    ocr_results:
        [
            {"text": "...", "confidence": 0.xx, "bbox": {...}},
            ...
        ]
    base_idx:
        当前监测文本索引
    user_unit:
        用户输入的单位，如 "A" / "V"
    log:
        日志回调函数
    """
    if not user_unit:
        return

    if base_idx < 0 or base_idx >= len(ocr_results):
        return

    base_text = ocr_results[base_idx]["text"].replace(" ", "")

    # === 情况 A：当前文本已包含单位 ===
    if user_unit in base_text:
        log(
            f"[INFO] 单位辅助判断：当前文本 ID={base_idx} "
            f"已包含单位 '{user_unit}'，监测数据正确。"
        )
        return

    # === 情况 B：在其它文本中查找 ===
    for idx, d in enumerate(ocr_results):
        if idx == base_idx:
            continue

        txt = d["text"].replace(" ", "")
        if user_unit in txt and re.search(r"\d", txt):
            log(
                f"[WARN] 单位辅助判断：在文本 ID={idx} ('{txt}') 中发现匹配单位，"
                f"当前选中文本 ID={base_idx} 可能不是监测数据，"
                "监测数据可能发生位置变动。"
            )
            return

    # === 情况 C：未找到 ===
    log(
        "[WARN] 单位辅助判断：未在其它文本中发现匹配单位，"
        "监测数据可能丢失或 OCR 识别异常。"
    )
