#!/usr/bin/env python3
"""
Jarvis command-center collector (runs ON YOUR MAC).

Reads Cowork session metadata + (best-effort) Claude Code transcripts, maps each
session to a project, and writes docs/data.json for the GitHub Pages dashboard.

What it captures reliably:
  - per session: title, selected model, created/last-activity, project, # enabled MCPs
  - per project: session count, model mix, last activity
  - overall: model mix, activity over time
  - tokens: ONLY if a matching Claude Code JSONL transcript with usage data is found
            (otherwise tokens are reported null and the dashboard says "model-mix proxy").

Usage:
    python3 collect.py                # writes docs/data.json next to this repo
    python3 collect.py --push         # also git add/commit/push (run from repo)
    python3 collect.py --base PATH    # override session base dir
"""
import json, os, sys, glob, time, argparse, subprocess, re
from pathlib import Path
from collections import defaultdict

HOME = Path.home()
DEFAULT_BASE = HOME / "Library/Application Support/Claude/local-agent-mode-sessions"
CLAUDE_DIR = HOME / ".claude"
REPO = Path(__file__).resolve().parent.parent          # command-center/
OUT  = REPO / "docs" / "data.json"

# ---- project mapping (keep in sync with registry.json) ----
RULES = [
    ("tino-go",   "Tino Go",               "Teso / SkyWhale",     r"tino\s*go|driver recruit"),
    ("tino",      "Tino Superapp",          "Teso / SkyWhale",     r"tino"),
    ("mmf",       "Money Market Fund",      "Мони Маркет Фанд",    r"money market|mmf"),
    ("midas",     "Midas Finance",          "Midas Finance",       r"midas"),
    ("carmax",    "CarMax",                 "CarMax",              r"carmax"),
    ("marketing", "Marketing / Posters",    "cross-project",       r"poster|media kit"),
    ("skills",    "Skill / Pipeline dev",   "internal",            r"skill|figma mcp|pipeline|design[-\s]?to[-\s]?figma|claude design|bundle|exports"),
    ("personal",  "Personal / Other",       "—",                   r"medication|financial|link preview|plan initiation|summarize my ideas"),
]
RULES = [(i, n, c, re.compile(p, re.I)) for (i, n, c, p) in RULES]

def classify(text):
    for i, n, c, rx in RULES:
        if rx.search(text or ""):
            return i, n, c
    return "other", "Unsorted", "—"

def epoch_ms(v):
    try:
        v = int(v)
        return v if v > 1_000_000_000_000 else v * 1000
    except Exception:
        return None

def build_token_index():
    """Best-effort: scan Claude Code JSONL transcripts, sum usage tokens per session id."""
    idx = defaultdict(lambda: {"input": 0, "output": 0, "cache": 0, "msgs": 0, "models": set()})
    roots = [CLAUDE_DIR / "projects", CLAUDE_DIR]
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        for f in root.rglob("*.jsonl"):
            if f in seen:
                continue
            seen.add(f)
            # session id is usually the filename stem
            stem = f.stem
            try:
                with open(f, "r", errors="ignore") as fh:
                    for line in fh:
                        if '"usage"' not in line:
                            continue
                        try:
                            obj = json.loads(line)
                        except Exception:
                            continue
                        msg = obj.get("message", obj)
                        usage = (msg or {}).get("usage") if isinstance(msg, dict) else None
                        if not isinstance(usage, dict):
                            continue
                        rec = idx[stem]
                        rec["input"]  += usage.get("input_tokens", 0) or 0
                        rec["output"] += usage.get("output_tokens", 0) or 0
                        rec["cache"]  += (usage.get("cache_read_input_tokens", 0) or 0) + (usage.get("cache_creation_input_tokens", 0) or 0)
                        rec["msgs"]   += 1
                        m = msg.get("model") if isinstance(msg, dict) else None
                        if m:
                            rec["models"].add(m)
            except Exception:
                continue
    return idx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(DEFAULT_BASE))
    ap.add_argument("--push", action="store_true")
    args = ap.parse_args()

    base = Path(args.base)
    files = [p for p in base.rglob("local_*.json")
             if "/.claude/" not in str(p) and "skills-plugin" not in str(p)]

    tokidx = build_token_index()
    tokens_found = any(v["input"] or v["output"] for v in tokidx.values())

    sessions = []
    for p in files:
        try:
            d = json.loads(p.read_text(errors="ignore"))
        except Exception:
            continue
        if not isinstance(d, dict) or "sessionId" not in d:
            continue
        title = d.get("title") or d.get("initialMessage", "")[:60] or p.stem
        pid, pname, pco = classify(f"{title} {d.get('cwd','')}")
        sid = d.get("sessionId", p.stem)
        cli = d.get("cliSessionId", "")
        tok = None
        for key in (sid, cli, p.stem):
            if key in tokidx and (tokidx[key]["input"] or tokidx[key]["output"]):
                t = tokidx[key]
                tok = {"input": t["input"], "output": t["output"], "cache": t["cache"], "msgs": t["msgs"]}
                break
        sessions.append({
            "id": sid,
            "title": title,
            "project": pid, "projectName": pname, "company": pco,
            "model": d.get("model", "unknown"),
            "archived": bool(d.get("isArchived")),
            "createdAt": epoch_ms(d.get("createdAt")),
            "lastActivityAt": epoch_ms(d.get("lastActivityAt")),
            "enabledMcps": len(d.get("enabledMcpTools", {}) or {}),
            "tokens": tok,
        })

    # aggregates
    by_project = defaultdict(lambda: {"sessions": 0, "models": defaultdict(int), "lastActivity": 0,
                                      "name": "", "company": "", "tokIn": 0, "tokOut": 0})
    by_model = defaultdict(int)
    for s in sessions:
        g = by_project[s["project"]]
        g["sessions"] += 1
        g["models"][s["model"]] += 1
        g["name"] = s["projectName"]; g["company"] = s["company"]
        if s["lastActivityAt"]:
            g["lastActivity"] = max(g["lastActivity"], s["lastActivityAt"])
        by_model[s["model"]] += 1
        if s["tokens"]:
            g["tokIn"] += s["tokens"]["input"]; g["tokOut"] += s["tokens"]["output"]

    projects = [{
        "id": pid, "name": g["name"], "company": g["company"],
        "sessions": g["sessions"], "models": dict(g["models"]),
        "lastActivity": g["lastActivity"],
        "tokens": ({"input": g["tokIn"], "output": g["tokOut"]} if tokens_found else None),
    } for pid, g in by_project.items()]
    projects.sort(key=lambda x: -x["sessions"])

    data = {
        "generatedAt": int(time.time() * 1000),
        "sessionCount": len(sessions),
        "tokensAvailable": tokens_found,
        "tokensNote": ("Real token counts recovered from Claude Code transcripts."
                       if tokens_found else
                       "No transcript token data found — showing model-mix as the cost proxy."),
        "byModel": dict(by_model),
        "projects": projects,
        "sessions": sorted(sessions, key=lambda s: -(s["lastActivityAt"] or 0))[:50],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Wrote {OUT}")
    print(f"  sessions={len(sessions)}  models={dict(by_model)}  tokens_found={tokens_found}")

    if args.push:
        try:
            subprocess.run(["git", "-C", str(REPO), "add", "docs/data.json"], check=True)
            subprocess.run(["git", "-C", str(REPO), "commit", "-m",
                            f"data: refresh {time.strftime('%Y-%m-%d %H:%M')}"], check=True)
            subprocess.run(["git", "-C", str(REPO), "push"], check=True)
            print("  pushed to GitHub.")
        except subprocess.CalledProcessError as e:
            print(f"  push skipped/failed: {e}")

if __name__ == "__main__":
    main()
