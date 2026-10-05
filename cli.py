"""命令行：python3 cli.py 或 python3 cli.py -f app.log"""
import argparse
import sys

from diagnoser import diagnose, parse_levels, report, SAMPLE_LOG


def main(argv=None):
    p = argparse.ArgumentParser(description="log-diagnoser-lite 日志异常诊断")
    p.add_argument("-f", "--file", help="日志文件")
    p.add_argument("--sample", action="store_true", help="使用内置示例日志")
    args = p.parse_args(argv)

    if args.sample:
        text = SAMPLE_LOG
    elif args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    if not text.strip():
        print("错误：未提供日志", file=sys.stderr)
        return 2
    print(report(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
