fetch("http://127.0.0.1:17321/health")
  .then((r) => r.json())
  .then((h) => {
    const el = document.getElementById("st");
    if (!h.ok) throw new Error("daemon down");
    el.className = h.extension ? "ok" : "bad";
    el.textContent = h.extension
      ? "已连接，可以让 Cursor 操作这个 Chrome"
      : "守护进程在，但扩展还没拉到指令（等 1 秒或切一下标签）";
  })
  .catch(() => {
    const el = document.getElementById("st");
    el.className = "bad";
    el.textContent = "连不上 127.0.0.1:17321，先启动 daemon.py";
  });
