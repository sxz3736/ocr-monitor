# logic/trigger_rule.py


def check_and_trigger(
    value: float,
    threshold: float,
    serial,
    hex_cmd: str,
    hex_count: int,
    hex_limit: int,
    log
) -> int:
    """
    阈值触发规则

    返回:
        更新后的 hex_count
    """

    # === 未达到阈值 ===
    if value < threshold:
        return hex_count

    # === 串口未连接 ===
    if not serial.is_connected:
        log("达到阈值，但串口未连接")
        return hex_count

    # === 超过发送上限 ===
    if hex_count >= hex_limit:
        log("HEX 发送已达上限")
        return hex_count

    # === 发送 HEX ===
    if serial.send_hex(hex_cmd):
        hex_count += 1
        log(f"HEX 已发送 ({hex_count})")

    return hex_count
