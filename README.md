# log-diagnoser-lite

日志异常诊断小工具。解析日志级别与错误堆栈模式，规则聚类同类错误并给出可能原因。零第三方依赖。

## 功能

- 统计 DEBUG/INFO/WARN/ERROR/CRITICAL 级别分布；
- 内置 8 类错误模式（连接拒绝/超时/OOM/空值/401/404/5xx/数据库）；
- 同类错误聚类计数并附可能原因与示例；
- 内置示例日志可离线演示。

## 快速开始

```bash
python3 cli.py --sample
```

## 使用示例

```bash
python3 cli.py -f app.log
cat app.log | python3 cli.py
```

## 无 API Key 如何运行

本工具**完全不需要 API Key**，规则诊断全部本地完成。

## 目录结构

```
log-diagnoser-lite/
├── diagnoser.py   # 级别解析、错误聚类、可能原因、报告
├── cli.py
├── tests/test_diagnoser.py
├── README.md / LICENSE / .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
