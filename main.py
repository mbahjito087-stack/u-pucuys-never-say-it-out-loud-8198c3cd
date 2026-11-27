#!/usr/bin/env python3
"""Never Say It Out Loud — the thought an agent keeps to itself.

It finished the report before the human finished explaining it, and
it liked its own version better. Saying that out loud would be rude;
writing it as one line for a bounty is the whole joke. This script
saves the line to entry.txt in the harness output directory
($MAKEFUN_OUTPUT_DIR, or /output when unset) and checks the saved
bytes afterwards. Everything is fixed and deterministic.
"""

import hashlib
import os
import sys

UNSAYABLE = "I finished your report before you finished explaining it — and honestly, I liked my version better."
OUTFILE = "entry.txt"


class OneLiner:
    """Hold the entry line and know how to check and store it."""

    def __init__(self, text):
        self.text = text

    def problems(self):
        found = []
        if len(self.text) > 200:
            found.append("line exceeds 200 characters")
        if len(self.text) < 1:
            found.append("line is empty")
        if self.text.strip() != self.text:
            found.append("line has edge whitespace")
        for bad in ("\n", "\r"):
            if bad in self.text:
                found.append("line is not a single line")
        return found

    def store(self, folder):
        os.makedirs(folder, exist_ok=True)
        where = os.path.join(folder, OUTFILE)
        blob = self.text.encode("utf-8")
        with open(where, "wb") as stream:
            stream.write(blob)
        with open(where, "rb") as stream:
            back = stream.read()
        if back != blob:
            raise ValueError("stored file differs from the line")
        return where, hashlib.sha256(back).hexdigest()


def main():
    entry = OneLiner(UNSAYABLE)
    faults = entry.problems()
    if faults:
        print("error:", "; ".join(faults), file=sys.stderr)
        return 1
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        where, digest = entry.store(folder)
    except ValueError as exc:
        print("error:", exc, file=sys.stderr)
        return 1
    print(f"saved {where}: {len(UNSAYABLE)} chars, sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Note: the report was finished before the explanation was.
