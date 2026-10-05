"""log-diagnoser-lite — 日志异常诊断。

解析日志中的级别与堆栈/错误模式，规则聚类错误并给出可能原因。
零第三方依赖。内置示例日志可离线演示。
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

LEVELS = ["DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL", "FATAL"]

ERROR_PATTERNS = [
    (r"Connection(?:Refused|Error|Timeout)", "网络/下游服务不可达：检查目标服务存活与网络连通"),
    (r"OutOfMemory|OOM|MemoryError", "内存不足：检查内存泄漏或调大堆内存"),
    (r"Timeout|timed out", "请求超时：下游慢或超时阈值过小"),
    (r"NullPointer|NoneType|KeyError|IndexError", "空值/越界：上游返回异常数据未做判空"),
    (r"401|Unauthorized|403|Forbidden", "鉴权失败：检查 token / 权限配置"),
    (r"404|Not Found", "资源不存在：检查路径或数据是否被删除"),
    (r"5\d\d|Internal Server Error", "服务端内部错误：查看服务堆栈与发布记录"),
    (r"Database|SQL|deadlock|Duplicate entry", "数据库异常：检查 SQL、锁、唯一约束冲突"),
]

SAMPLE_LOG = """2026-01-01 10:00:01 INFO  Server started on :8080
2026-01-01 10:00:05 ERROR ConnectionRefusedError: connect to db:5432 failed
2026-01-01 10:00:06 ERROR ConnectionRefusedError: connect to db:5432 failed
2026-01-01 10:01:00 WARN  Slow query took 3.2s
2026-01-01 10:02:11 ERROR TimeoutError: request to upstream timed out
2026-01-01 10:02:12 ERROR TimeoutError: request to upstream timed out
2026-01-01 10:03:00 ERROR KeyError: 'user_id' at handler.py:42
2026-01-01 10:04:00 CRITICAL OutOfMemoryError: heap space exhausted
"""


def parse_levels(text: str) -> dict:
    """统计各级别出现次数。"""
    counts = Counter()
    for line in text.splitlines():
        for lv in LEVELS:
            if re.search(rf"\b{lv}\b", line):
                counts[lv] += 1
                break
    return dict(counts)


def diagnose(text: str) -> list[dict]:
    """聚类错误行并给出可能原因。"""
    clusters: dict[str, dict] = {}
    for line in text.splitlines():
        if not re.search(r"\b(ERROR|CRITICAL|FATAL)\b", line):
            continue
        matched = None
        for pattern, cause in ERROR_PATTERNS:
            if re.search(pattern, line):
                matched = (pattern, cause)
                break
        key = matched[0] if matched else "OTHER"
        if key not in clusters:
            clusters[key] = {"pattern": key, "count": 0,
                             "cause": matched[1] if matched else "未识别模式，需人工查看堆栈",
                             "examples": []}
        clusters[key]["count"] += 1
        if len(clusters[key]["examples"]) < 2:
            clusters[key]["examples"].append(line.strip())
    return sorted(clusters.values(), key=lambda x: x["count"], reverse=True)


def report(text: str) -> str:
    levels = parse_levels(text)
    diags = diagnose(text)
    lines = ["=== 日志异常诊断报告 ==="]
    lines.append("级别分布：" + "，".join(f"{k}={v}" for k, v in sorted(levels.items())))
    lines.append("")
    if not diags:
        lines.append("未发现 ERROR/CRITICAL 级别日志。")
    for i, d in enumerate(diags, 1):
        lines.append(f"[{i}] 错误模式：{d['pattern']}  出现 {d['count']} 次")
        lines.append(f"    可能原因：{d['cause']}")
        for ex in d["examples"]:
            lines.append(f"    示例：{ex}")
    return "\n".join(lines)
