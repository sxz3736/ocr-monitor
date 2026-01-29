# logic/value_parser.py
import re
from typing import Optional


def extract_value(text: str) -> Optional[float]:
    """
    从 OCR 文本中提取第一个数值

    示例:
        "12.34A"  -> 12.34
        "I = -5"  -> -5.0
        "ABC"     -> None
    """
    if not text:
        return None

    clean = text.replace(" ", "")
    match = re.search(r'([-+]?\d*\.?\d+)', clean)
    if not match:
        return None

    try:
        return float(match.group(1))
    except ValueError:
        return None
