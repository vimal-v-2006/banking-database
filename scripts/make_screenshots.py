#!/usr/bin/env python3
"""Renders real SQL*Plus captured output as terminal-style screenshot PNGs."""
import re, os
from PIL import Image, ImageDraw, ImageFont

OUT = "report/output"
IMGS = "report/images"

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
TFONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)

PAD, LH, BART = 22, 19, 36

C_BG, C_BAR, C_BARTXT = (16, 20, 24), (232, 232, 232), (60, 60, 60)
C_TEXT, C_GREEN = (212, 212, 212), (106, 153, 85)
C_TEAL, C_BLUE, C_YELLOW = (78, 201, 176), (86, 156, 214), (220, 220, 170)
C_ORANGE, C_RED, C_GRAY, C_DIM = (206, 145, 120), (244, 71, 71), (157, 165, 180), (90, 96, 110)

FEEDBACK_RE = re.compile(
    r"^(\d+ rows? (selected|created)\.|(Table|Index|View|Sequence|Procedure) created\.|Commit complete\.|PL/SQL procedure successfully completed\.)$")
SQL_KW_RE = re.compile(r"^(INSERT|SELECT|CREATE|DROP|SET|COMMIT|DECLARE|BEGIN|END|GRANT|EXEC)\b")

CONT_START = ("TO_CHAR", "FROM ", "ORDER BY", "WHERE ", "UNION", "SELECT ", "GROUP BY", "HAVING",
              "AND ", "OR ", "BEGIN", "END ", "IF ", "THEN", "ELSE", "END IF", "FOR ", "INTO ",
              "WHEN ", "EXCEPTION", "ROLLBACK", "COMMIT", "RETURN", "UPDATE", "INSERT", "VALUES",
              "DECLARE", "SET ", "NO_DATA_FOUND")

def _is_continuation(text):
    """True if this line is a wrapped continuation of the previous statement."""
    c = text[:1]
    if c.islower() or c in "'\"(),-/:" or c.isdigit():
        return True
    return text.upper().startswith(CONT_START)


def expand_tabs(s):
    out, col = [], 0
    for ch in s:
        if ch == "\t":
            n = 8 - col % 8
            out.append(" " * n); col += n
        else:
            out.append(ch); col += 1
    return "".join(out)


def parse_session(path, keep_sections=None):
    """Return list of (kind, text); kind in banner|prompt|label|msg|feedback|sep|data|plain|blank"""
    lines = open(path).read().splitlines()
    logical, in_table, prev_kind = [], False, None

    def push(kind, text):
        nonlocal prev_kind
        if kind == "blank":
            if prev_kind not in (None, "blank"):
                logical.append((kind, text))
            return
        logical.append((kind, text))
        prev_kind = kind

    for raw in lines:
        line = expand_tabs(raw.rstrip())
        stripped = line.strip()
        if not stripped:
            in_table = False
            push("blank", "")
            continue

        text, is_prompt = stripped, False
        m = re.match(r"^(?:SQL>\s*)+(.*)$", line)
        if m:
            rest = m.group(1).strip()
            n_prompt = line.count("SQL>")
            if not rest:
                in_table = False
                push("blank", "")
                continue
            if re.fullmatch(r"[\d\s]+", rest):            # line-number artifact
                push("blank", "")
                continue
            nm = re.match(r"^\d+(?:\s+\d+)*\s+(\S.*)$", rest)  # artifact prefix on message
            if nm:
                rest = nm.group(1)
            if n_prompt >= 2:                              # echoed statement / label
                in_table = False
                if rest.startswith("===") or rest.startswith("[TXN"):
                    push("label", rest)
                else:
                    push("prompt", rest)
                continue
            # single SQL> prefix: wrapped continuation of the previous statement
            bannerish = rest.startswith(("Disconnected", "SQL*Plus:", "Version ", "Connected",
                                         "Copyright", "Last Successful", "Oracle Database"))
            if logical and logical[-1][0] == "prompt" and not bannerish and _is_continuation(rest):
                logical[-1] = ("prompt", logical[-1][1] + " " + rest)
                continue
            text, is_prompt = rest, True

        if re.fullmatch(r"(-{3,}\s*)+", text):            # column separator row
            in_table = True
            push("sep", text)
            continue
        if in_table:                                      # keep result rows verbatim
            push("data", text)
            continue
        if FEEDBACK_RE.match(text):
            push("feedback", text)
            continue
        if text.startswith("===") or text.startswith("[TXN"):
            push("label", text)
            continue
        if is_prompt:
            push("prompt", text)
            continue
        if text.startswith(("SUCCESS", "ERROR", "ORA-")):
            push("msg", text)
            continue
        if text.startswith(("SQL*Plus:", "Version ", "Copyright", "Last Successful",
                            "Connected to:", "Oracle Database", "Disconnected from")):
            push("banner", text)
            continue
        if SQL_KW_RE.match(text):
            push("prompt", text)                          # un-prefixed SQL statements
            continue
        if re.fullmatch(r"\d{1,3}(\s+\d{1,3})+", text):   # bare line-number artifact
            push("blank", "")
            continue
        # wrap-around continuation (DBMS_OUTPUT split by LINESIZE)
        if logical and logical[-1][0] == "msg":
            logical[-1] = ("msg", logical[-1][1] + " " + text)
        elif logical and logical[-1][0] == "prompt" and text[:1].islower():
            logical[-1] = ("prompt", logical[-1][1] + " " + text)
        else:
            push("plain", text)

    if keep_sections:
        start, end = keep_sections
        first_label_idx = next((i for i, (k, _) in enumerate(logical) if k == "label"), None)
        kept, active = [], False
        for idx, (kind, t) in enumerate(logical):
            header = kind == "banner" and first_label_idx is not None and idx < first_label_idx
            if kind == "label" and t.startswith(start):
                active = True
            if active and end and kind == "label" and t.startswith(end):
                active = False
            if header or active:
                kept.append((kind, t))
        logical = kept
    while logical and logical[0][0] == "blank":
        logical.pop(0)
    while logical and logical[-1][0] == "blank":
        logical.pop()
    return logical


def render(logical, title, out_path):
    maxw = 118

    def wrap(t, w):
        if len(t) <= w:
            return [t]
        out, cur = [], ""
        for word in t.split(" "):
            if len(cur) + 1 + len(word) > w and cur:
                out.append(cur); cur = word
            else:
                cur = cur + " " + word if cur else word
        if cur:
            out.append(cur)
        return out

    rows = []
    for kind, t in logical:
        if kind == "blank" or kind in ("data", "sep"):
            rows.append((kind, t)); continue
        rows.extend((kind, p) for p in wrap(t, maxw))

    w = int(max(max(len(t) for _, t in rows) * 8.42 + PAD * 2, 560))
    h = int(BART + PAD + len(rows) * LH)
    img = Image.new("RGB", (w, h), C_BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, BART], fill=C_BAR)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse([10 + i * 20, BART // 2 - 6, 22 + i * 20, BART // 2 + 6], fill=c)
    d.text((w / 2, BART / 2 - 8), title, font=TFONT, fill=C_BARTXT, anchor="mm")

    y = BART + 8
    for kind, t in rows:
        if kind == "blank":
            y += LH; continue
        if kind == "prompt":
            d.text((PAD, y), "SQL> ", font=FONT, fill=C_BLUE)
            d.text((PAD + 5 * 8.42, y), t, font=FONT, fill=C_TEXT)
        elif kind == "msg":
            d.text((PAD, y), t, font=FONT, fill=C_RED if t.startswith(("ERROR", "ORA-")) else C_GREEN)
        elif kind == "label":
            d.text((PAD, y), t, font=FONT, fill=C_YELLOW)
        elif kind == "banner":
            d.text((PAD, y), t, font=FONT, fill=C_TEAL if "SQL*Plus:" in t else C_GRAY)
        elif kind == "feedback":
            d.text((PAD, y), t, font=FONT, fill=C_GREEN)
        elif kind == "sep":
            d.text((PAD, y), t, font=FONT, fill=C_DIM)
        else:
            d.text((PAD, y), t, font=FONT, fill=C_GRAY if kind == "plain" else C_TEXT)
        y += LH
    img.save(out_path)
    print(f"[screenshot] {out_path}  ({w}x{h}, {len(rows)} lines)")


SHOTS = [
    ("ss1_version.txt",      "er_connect.png",   "SQL*Plus  -  Oracle Database 21c Express Edition", None),
    ("ss2_schema.txt",       "er_schema1.png",   "SQL*Plus  -  Oracle Database 21c Express Edition", ("=== STEP 1", "=== STEP 3")),
    ("ss2_schema.txt",       "er_schema2.png",   "SQL*Plus  -  Oracle Database 21c Express Edition", ("=== STEP 3", None)),
    ("ss3_customers.txt",    "er_customers.png", "SQL*Plus  -  Oracle Database 21c Express Edition", None),
    ("ss4_accounts.txt",     "er_accounts.png",  "SQL*Plus  -  Oracle Database 21c Express Edition", None),
    ("ss5_procedures.txt",   "er_proc1.png",  "SQL*Plus  -  Oracle Database 21c Express Edition",
     ("=== CREATE PROCEDURE DEPOSIT_FUNDS", "=== CREATE PROCEDURE WITHDRAW_FUNDS")),
    ("ss5_procedures.txt",   "er_proc2.png",  "SQL*Plus  -  Oracle Database 21c Express Edition",
     ("=== CREATE PROCEDURE WITHDRAW_FUNDS", "=== CREATE PROCEDURE OPEN_ACCOUNT")),
    ("ss5_procedures.txt",   "er_proc3.png",  "SQL*Plus  -  Oracle Database 21c Express Edition",
     ("=== CREATE PROCEDURE OPEN_ACCOUNT", None)),
    ("ss6_deposits.txt",     "er_deposits.png",  "SQL*Plus  -  Oracle Database 21c Express Edition", None),
    ("ss7_withdrawals.txt",  "er_withdrawals.png", "SQL*Plus  -  Oracle Database 21c Express Edition", None),
    ("ss8_report.txt",       "er_history.png",   "SQL*Plus  -  Oracle Database 21c Express Edition", ("=== 3.", "=== 5.")),
    ("ss8_report.txt",       "er_summary.png",   "SQL*Plus  -  Oracle Database 21c Express Edition", ("=== 5.", None)),

]


def main():
    os.makedirs(IMGS, exist_ok=True)
    for src, name, title, sec in SHOTS:
        render(parse_session(f"{OUT}/{src}", sec), title, f"{IMGS}/{name}")


if __name__ == "__main__":
    main()
