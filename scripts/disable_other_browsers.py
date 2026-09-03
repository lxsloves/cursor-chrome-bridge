#!/usr/bin/env python3
"""Disable alternate Cursor browser-control paths; keep chrome-bridge only."""
from __future__ import annotations

import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

DB = Path("/Users/rxyy/Library/Application Support/Cursor/User/globalStorage/state.vscdb")
APP_KEY = "src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl.persistentStorage.applicationUser"
CLOUD_KEY = "agentData.cacheStorage.glass.cloudMcpServers.v1.personal.github%7Cuser_01K67S521KDJTB49JA0S1HH834"

# Playwright + Browserbase Browse plugin IDs (from cloud MCP cache)
REMOVE_PLUGIN_IDS = {"675", "578820"}


def main() -> None:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = DB.with_name(f"state.vscdb.bak-browser-cleanup-{stamp}")
    shutil.copy2(DB, backup)
    print(f"backup: {backup}")

    con = sqlite3.connect(DB)
    cur = con.cursor()

    # 1) Turn Browser Automation Off
    raw = cur.execute("SELECT value FROM ItemTable WHERE key=?", (APP_KEY,)).fetchone()[0]
    data = json.loads(raw)
    data["lastBrowserConnectionMode"] = "none"
    data["browserChipManuallyDisabled"] = True
    data["browserChipManuallyEnabled"] = False
    if isinstance(data.get("composerState"), dict):
        data["composerState"]["playwrightProtection"] = True
    cur.execute("UPDATE ItemTable SET value=? WHERE key=?", (json.dumps(data, ensure_ascii=False), APP_KEY))
    print("set lastBrowserConnectionMode=none, browserChipManuallyDisabled=true, playwrightProtection=true")

    # 2) Uninstall Playwright + Browse plugins from every workspace install list
    rows = cur.execute("SELECT key, value FROM ItemTable WHERE key LIKE 'cursor.plugins.installedIds%'").fetchall()
    for key, val in rows:
        plugins = json.loads(val)
        kept = [p for p in plugins if str(p.get("id")) not in REMOVE_PLUGIN_IDS]
        if len(kept) != len(plugins):
            removed = [p.get("id") for p in plugins if str(p.get("id")) in REMOVE_PLUGIN_IDS]
            cur.execute("UPDATE ItemTable SET value=? WHERE key=?", (json.dumps(kept, ensure_ascii=False), key))
            print(f"plugins {key}: removed {removed}")

    # 3) Mark cloud MCP cache entries disabled (best-effort until next sync)
    row = cur.execute("SELECT value FROM ItemTable WHERE key=?", (CLOUD_KEY,)).fetchone()
    if row:
        blob = row[0]
        prefix = ""
        body = blob
        if body.startswith("v2:"):
            nl = body.find("\n")
            prefix, body = body[: nl + 1], body[nl + 1 :]
        cloud = json.loads(body)
        servers = cloud.get("servers", {}).get("servers", [])
        for s in servers:
            if str(s.get("pluginId")) in REMOVE_PLUGIN_IDS or s.get("name") in {"Playwright", "Browser"}:
                s["enabled"] = False
                print(f"cloud MCP disable: {s.get('name')} pluginId={s.get('pluginId')}")
        cur.execute(
            "UPDATE ItemTable SET value=? WHERE key=?",
            (prefix + json.dumps(cloud, ensure_ascii=False), CLOUD_KEY),
        )

    con.commit()
    con.close()
    print("done")


if __name__ == "__main__":
    main()
