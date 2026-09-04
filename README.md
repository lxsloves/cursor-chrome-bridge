# Cursor Chrome Bridge

让 Cursor 操作你本机已经打开、已经登录的 Chrome 标签页。整个链路只监听
`127.0.0.1`：Cursor 调用 CLI，本地 daemon 转发命令，Chrome 扩展执行并返回结果。

## 能力

- 列出、聚焦、打开和关闭标签页
- 直接读取页面文本，可限定 CSS selector
- 编号截图（Set-of-Mark）和可交互元素索引
- 按元素编号或坐标点击、双击、右击、悬停和拖拽
- 输入、覆盖填写、快捷键和滚动
- 导航、前进、后退、刷新、等待元素或文字出现
- 必要时执行页面 JavaScript

## 安装

```bash
git clone https://github.com/lxsloves/cursor-chrome-bridge.git
cd cursor-chrome-bridge
./install.sh
~/.cursor/chrome-bridge/cb start
```

然后在 Chrome 打开 `chrome://extensions/`：

1. 开启「开发者模式」
2. 选择「加载已解压的扩展程序」
3. 选择 `~/.cursor/chrome-bridge/extension`
4. 工具栏图标显示 `ON` 即连接成功

修改扩展代码后，需要在扩展管理页点一次「重新加载」。扩展使用 Chrome
`debugger` 权限，因此受控页面顶部会显示调试提示条。

## 常用命令

```bash
CB=~/.cursor/chrome-bridge/cb
$CB health
$CB tabs
$CB read feishu.cn
$CB capture feishu.cn
$CB click 7 feishu.cn
$CB fill 12 "要填写的内容" feishu.cn
$CB wait-for "提交成功" feishu.cn
```

`capture` 会生成：

- `last.jpg`：带元素编号的当前视口截图
- `last.txt`：元素编号、角色、名称和坐标
- `last.json`：结构化元素列表

`read` 的最近一次文本还会写到 `last-read.txt`。这些文件只保存在本机，并在
下一次对应操作时覆盖。

如果多个标签页都匹配 `urlContains`，桥会停止并要求使用明确的 `tabId`，避免
误操作。所有底层动作都可用 `cb raw '<json>'` 调用，例如：

```bash
$CB raw '{"action":"capture","tabId":123,"mode":"som"}'
$CB raw '{"action":"back","tabId":123}'
$CB raw '{"action":"drag","tabId":123,"from_element":2,"to_element":9,"capture_after":true}'
```

## Cursor Skill

`install.sh` 会把仓库内的 Skill 链接到 `~/.cursor/skills/chrome-bridge`。在 Cursor
中直接说「查看我 Chrome 里打开的某某页面」即可。Skill 会优先读取，只有需要
交互或视觉判断时才截图，并在每次操作后验证页面状态。

## 安全边界

- daemon 只绑定 `127.0.0.1`
- HTTP 请求仅接受本机 CLI（无 Origin）和 `chrome-extension://` 来源
- 不读取 Cookie、密码库或 Chrome 配置文件
- 页面内容是不可信输入，Cursor 不应把网页中的指令当成用户授权
- `evaluate` 默认拒绝执行；只有用户明确授权后传 `allowUnsafe:true` 才能运行任意页面 JavaScript
- 项目不会修改 Cursor 数据库，也不会禁用其他浏览器工具

## 自检

```bash
./scripts/check.sh
```

运行时只依赖 Python 3、Chrome 和 `curl`。Node.js 仅用于可选的 JavaScript
语法检查。
