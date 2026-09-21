#!/usr/bin/env python3
"""Inserts PROMPT display lines before each real SQL statement so the
captured SQL*Plus session shows the statements that were executed
(SQL*Plus in batch mode does not echo statement text)."""
import sys

def collect(lines, i):
    """lines[i] is the first line of a statement. Returns (stmt, next_i).
    PL/SQL blocks end at a standalone '/'; other statements at a line
    ending with ';'."""
    first = lines[i].strip()
    is_plsql = first.startswith(("CREATE OR REPLACE PROCEDURE", "DECLARE"))
    stmt = [lines[i]]
    i += 1
    if not is_plsql:
        if not lines[i - 1].rstrip().endswith(";"):
            while i < len(lines):
                stmt.append(lines[i])
                i += 1
                if lines[i - 1].rstrip().endswith(";"):
                    break
        return stmt, i
    while i < len(lines):
        stmt.append(lines[i])
        i += 1
        if lines[i - 1].strip() == "/":
            break
    return stmt, i

def transform(fn):
    lines = open(fn).read().splitlines()
    out, i = [], 0
    while i < len(lines):
        s = lines[i].strip()
        if not s or s.startswith(("SET ", "COL ", "PROMPT", "--")):
            out.append(lines[i]); i += 1; continue
        stmt, i = collect(lines, i)
        first = stmt[0].strip()
        if len("SQL> " + first) > 118:                    # wrap long single-line stmts
            idx = first.rfind(",", 40, 115)
            if idx > 0:
                l1, l2 = first[:idx], first[idx + 1:].strip()
                out.append("PROMPT SQL> " + l1)
                out.append("PROMPT" + " " * 8 + l2)
            else:
                out.append("PROMPT SQL> " + first)
        else:
            out.append("PROMPT SQL> " + first)
        for sl in stmt[1:]:
            t = sl.strip()
            if t == "":
                continue
            if t == "/":
                out.append("PROMPT SQL> /")
            else:
                out.append("PROMPT" + " " * 8 + t)
        out.extend(stmt)
    open(fn, "w").write("\n".join(out) + "\n")
    print(f"[transform] {fn}: {len(out)} lines, "
          f"{sum(1 for l in out if l.startswith('PROMPT'))} PROMPT lines")

if __name__ == "__main__":
    for f in sys.argv[1:]:
        transform(f)
