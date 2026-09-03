# Cursor Chrome Bridge

让 Cursor 按 Codex 的方式操作本机已经打开的 Chrome 标签（只连 `127.0.0.1`）。

## 启动

```bash
python3 daemon.py
```

Chrome 打开 `chrome://extensions/` → 开发者模式 → 加载已解压的扩展程序 → 选 `extension/`。工具栏图标应显示 `ON`。

## 指令

```bash
# 编号截图 + 元素列表（默认）
curl -sS -X POST http://127.0.0.1:17321/cmd \
  -H 'Content-Type: application/json' \
  -d '{"action":"capture","urlContains":"lanhuapp.com"}'

# 按编号点
curl -sS -X POST http://127.0.0.1:17321/cmd \
  -H 'Content-Type: application/json' \
  -d '{"action":"click","element":7,"urlContains":"lanhuapp.com","capture_after":true}'
```

截图写到 `last.jpg`，元素列表写到 `last.txt`。动作面：`capture` / `click` / `type` / `key` / `scroll` / `drag` / `wait` / `tabs` / `navigate`。

扩展使用 `debugger` 权限，页面顶上会有调试提示条（和 ChatGPT 官方插件一样）。
