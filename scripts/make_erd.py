#!/usr/bin/env python3
"""Draws the Chen-style ER diagram for the Banking Database."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1900, 1000
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

F   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_attr  = ImageFont.truetype(F, 15)
f_attrb = ImageFont.truetype(FB, 15)
f_ent   = ImageFont.truetype(FB, 17)
f_rel   = ImageFont.truetype(FB, 15)
f_card  = ImageFont.truetype(FB, 16)
f_note  = ImageFont.truetype(F, 13)
f_title = ImageFont.truetype(FB, 24)

# ---- geometry ----
CUST, ACCT, TRAN = (300, 500), (950, 500), (1610, 500)
OPENS, REC = (640, 500), (1300, 500)

cust_attrs = [
    ((120, 300), "customer_id (PK)", True), ((280, 255), "first_name", False),
    ((440, 300), "last_name", False),       ((85, 405), "email (UK)", True),
    ((500, 395), "phone", False),           ((120, 700), "date_of_birth", False),
    ((280, 750), "address", False),         ((440, 700), "city", False),
    ((520, 610), "created_on", False),
]
acct_attrs = [
    ((790, 300), "account_no (PK)", True),  ((950, 255), "customer_id (FK)", True),
    ((1110, 300), "account_type (CK)", True),
    ((790, 700), "opening_balance", False), ((950, 750), "current_balance", False),
    ((1110, 700), "status (CK)", True),     ((1230, 610), "opened_on", False),
]
tran_attrs = [
    ((1450, 300), "txn_id (PK)", True),     ((1610, 255), "account_no (FK)", True),
    ((1770, 300), "txn_date", False),
    ((1450, 700), "txn_type (CK)", True),   ((1610, 750), "amount", False),
    ((1770, 700), "balance_after", False),  ((1850, 610), "description", False),
]

# ---- pass 1: connector lines (drawn first, shapes cover their ends) ----
for attrs, ent in ((cust_attrs, CUST), (acct_attrs, ACCT), (tran_attrs, TRAN)):
    for cpos, _, _ in attrs:
        d.line([cpos, ent], fill="black", width=2)
d.line([CUST, OPENS], fill="black", width=2)
d.line([OPENS, ACCT], fill="black", width=2)
d.line([ACCT, REC], fill="black", width=2)
d.line([REC, TRAN], fill="black", width=2)

# ---- pass 2: attribute ellipses ----
for attrs in (cust_attrs, acct_attrs, tran_attrs):
    for cpos, t, b in attrs:
        x, y = cpos
        d.ellipse([x - 80, y - 19, x + 80, y + 19], fill="#FFF8E1", outline="black", width=2)
        d.text((x, y), t, font=f_attrb if b else f_attr, fill="black", anchor="mm")

# ---- pass 3: relationship diamonds ----
for cpos, t in ((OPENS, "OPENS"), (REC, "RECORDS_IN")):
    x, y = cpos
    d.polygon([(x - 95, y), (x, y - 48), (x + 95, y), (x, y + 48)],
              fill="#E8F5E9", outline="black", width=2)
    d.text((x, y), t, font=f_rel, fill="black", anchor="mm")

# ---- pass 4: entity rectangles ----
for cpos, t, rw in ((CUST, "CUSTOMER", 75), (ACCT, "ACCOUNT", 75), (TRAN, "TRANSACTION", 95)):
    x, y = cpos
    d.rectangle([x - rw, y - 32, x + rw, y + 32], fill="#DCE9F7", outline="black", width=3)
    d.text((x, y), t, font=f_ent, fill="black", anchor="mm")

# ---- cardinality labels ----
for p, t in (((500, 476), "1"), ((598, 476), "M"),
             ((818, 476), "1"), ((866, 476), "M"),
             ((1108, 476), "1"), ((1198, 476), "M")):
    d.ellipse([p[0] - 12, p[1] - 12, p[0] + 12, p[1] + 12], fill="white", outline="#B71C1C", width=2)
    d.text(p, t, font=f_card, fill="#B71C1C", anchor="mm")

# ---- title & notes ----
d.text((W / 2, 40), "Entity - Relationship (ER) Diagram  -  Banking Database",
       font=f_title, fill="black", anchor="mm")
d.text((W / 2, H - 42), "CUSTOMER (1) ---< OPENS >--- (M) ACCOUNT (1) ---< RECORDS_IN >--- (M) TRANSACTION",
       font=ImageFont.truetype(FB, 16), fill="#333333", anchor="mm")
d.text((W / 2, H - 18), "PK : Primary Key      FK : Foreign Key      CK : Check Constraint      UK : Unique Key",
       font=f_note, fill="#555555", anchor="mm")

img.save("report/images/er_diagram.png")
print("saved report/images/er_diagram.png", img.size)
