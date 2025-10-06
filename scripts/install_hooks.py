#!/usr/bin/env python3
from __future__ import annotations

import os
import stat

HOOK_PATH = os.path.join(".git", "hooks", "post-commit")
MARK = "# simutrador-gh-progress"

SCRIPT = """#!/bin/sh
# {mark}
# Auto-post commit progress to GitHub Issue
if command -v python3 >/dev/null 2>&1; then
  python3 scripts/gh_progress_post_commit.py || true
else
  python scripts/gh_progress_post_commit.py || true
fi
""".strip()


def main() -> int:
    os.makedirs(os.path.dirname(HOOK_PATH), exist_ok=True)

    if os.path.exists(HOOK_PATH):
        with open(HOOK_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        if MARK in content:
            # Already installed
            return 0
        # Append our block safely
        new_content = content.rstrip() + "\n\n" + SCRIPT.format(mark=MARK) + "\n"
    else:
        new_content = SCRIPT.format(mark=MARK) + "\n"

    with open(HOOK_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    st = os.stat(HOOK_PATH)
    os.chmod(HOOK_PATH, st.st_mode | stat.S_IEXEC)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

