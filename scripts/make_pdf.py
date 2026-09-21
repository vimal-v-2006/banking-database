#!/usr/bin/env python3
"""Builds the single PDF report for the Banking Database project."""
import os
import re
from fpdf import FPDF

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = f"{ROOT}/report/images"
SQL = f"{ROOT}/sql"
OUT = f"{ROOT}/report/output/Banking_Database_Project_Report.pdf"

GITHUB = "https://github.com/vimal-v-2006/banking-database"

CUSTOMER, REGNO, COLLEGE, COURSE, AY = (
    "Vimal", "2422J1256",
    "Kaypeeyes College of Arts and Science, Kotagiri",
    "III BCA", "2026 - 2027")

NAVY = (18, 42, 84)
LIGHT = (240, 243, 248)
GRAY = (90, 90, 90)


def read_sql(name):
    """Read a SQL script, dropping the PROMPT display-echo lines that exist
    only so sqlplus captures show the executed statements."""
    with open(f"{SQL}/{name}") as f:
        lines = f.read().splitlines()
    clean = []
    for line in lines:
        if line.startswith("PROMPT SQL>"):
            continue
        if re.match(r"^PROMPT {8}\S", line):
            continue
        clean.append(line)
    return "\n".join(clean)


class Report(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.chapter_no = ""
        self.chapter_title = ""
        self.set_auto_page_break(True, margin=16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, "Banking Database  -  Oracle 21c", 0, 0, "L")
        self.cell(0, 5, f"{CUSTOMER}  ({REGNO})", 0, 0, "R")
        self.set_draw_color(*NAVY)
        self.set_line_width(0.3)
        self.line(self.l_margin, 11, self.w - self.r_margin, 11)
        self.ln(4)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", 0, 0, "C")

    # ---------- content helpers ----------
    def chapter(self, no, title):
        self.add_page()
        self.chapter_no = no
        self.chapter_title = title
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(*NAVY)
        self.cell(0, 12, f"{no}.  {title}", 0, 1, "L")
        self.set_draw_color(*NAVY)
        self.set_line_width(0.5)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(6)
        self.start_section(f"{no}. {title}")

    def h2(self, text):
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 12.5)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 6.5, text)
        self.set_x(self.l_margin)
        self.set_text_color(30, 30, 30)

    def body(self, text, size=10):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", size)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.set_x(self.l_margin)
        self.ln(1.5)

    def bullets(self, items, size=10):
        self.set_font("Helvetica", "", size)
        self.set_text_color(30, 30, 30)
        for it in items:
            x = self.get_x()
            self.cell(5, 5, "*")
            self.multi_cell(0, 5, it)
            self.set_x(x)
            self.set_x(self.l_margin)
            self.set_x(x)
        self.ln(1.5)

    def code(self, text, size=7.8):
        self.ln(1)
        self.set_font("Courier", "", size)
        self.set_text_color(25, 25, 25)
        self.set_fill_color(*LIGHT)
        for line in text.rstrip("\n").split("\n"):
            self.set_x(self.l_margin)
            self.multi_cell(0, 3.6, line if line else " ", fill=True)
        self.set_x(self.l_margin)
        self.ln(2.5)
        self.set_text_color(30, 30, 30)

    def figure(self, img, caption, max_w=180, max_h=235):
        from PIL import Image as PImage
        wpx, hpx = PImage.open(img).size
        w = max_w
        h = w * hpx / wpx
        if h > max_h:
            h = max_h
            w = h * wpx / hpx
        if self.get_y() + h + 14 > 281:
            self.add_page()
        x = (self.w - w) / 2
        self.image(img, x, self.get_y(), w, h)
        self.set_y(self.get_y() + h + 2)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 5, caption, 0, "C")
        self.set_x(self.l_margin)
        self.set_text_color(30, 30, 30)
        self.ln(2)

    def data_table(self, headers, rows, widths, align=None):
        from fpdf.enums import Align
        from fpdf.fonts import FontFace
        self.set_x(self.l_margin)
        with self.table(
            col_widths=list(widths),
            text_align=Align.L,
            line_height=5.2,
            headings_style=FontFace(emphasis="BOLD", color=(255, 255, 255),
                                    fill_color=NAVY, size_pt=8.5),
            first_row_as_headings=True,
        ) as t:
            t.row(headers)
            for row in rows:
                t.row(row)
        self.set_x(self.l_margin)
        self.ln(3)


def render_toc(pdf, outline):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 9, "Contents", 0, 1)
    pdf.ln(2)
    for e in outline:
        pdf.set_font("Helvetica", "B" if e.level == 0 else "", 11 if e.level == 0 else 10)
        pdf.set_text_color(30, 30, 30)
        indent = 0 if e.level == 0 else 6
        x0 = pdf.l_margin + indent
        pdf.set_x(x0)
        pdf.cell(0, 7, e.name, 0, 0)
        pdf.set_x(pdf.w - pdf.r_margin)
        pdf.cell(0, 7, str(e.page_number), 0, 1, "R")


def main():
    pdf = Report()
    pdf.alias_nb_pages()
    pdf.set_margins(15, 15, 15)

    # ============ COVER PAGE ============
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 60, "F")
    pdf.set_y(18)
    pdf.set_font("Helvetica", "B", 30)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 14, "BANKING DATABASE", 0, 1, "C")
    pdf.set_font("Helvetica", "", 13)
    pdf.cell(0, 8, "Design and Implementation of a Banking Database System", 0, 1, "C")
    pdf.cell(0, 8, "using Oracle Database 21c Express Edition", 0, 1, "C")

    pdf.set_y(90)
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.4)
    pdf.rect(40, pdf.get_y(), 130, 74)
    pdf.set_fill_color(248, 249, 252)
    pdf.rect(40, pdf.get_y(), 130, 74, "F")
    pdf.set_y(pdf.get_y() + 6)
    pdf.set_text_color(30, 30, 30)
    rows = [
        ("Submitted by :", CUSTOMER),
        ("Registration No :", REGNO),
        ("Course :", "Bachelor of Computer Applications (BCA)"),
        ("Year / Semester :", f"{COURSE}  (5th Semester)"),
        ("Academic Year :", AY),
        ("Institution :", COLLEGE),
    ]
    pdf.set_font("Helvetica", "", 11)
    for k, v in rows:
        pdf.set_x(48)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(40, 9, k)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 9, v, 0, 1)
    pdf.set_y(180)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 8, f"Project Repository :  {GITHUB}", 0, 1, "C")
    pdf.set_y(200)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 7, "A Mini-Project / Hackathon Report", 0, 1, "C")
    pdf.cell(0, 7, "Department of Computer Applications", 0, 1, "C")
    pdf.set_y(265)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 7, "September 2026", 0, 1, "C")

    # ============ DECLARATION ============
    pdf.add_page()
    pdf.start_section("Declaration")
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 12, "Declaration", 0, 1, "C")
    pdf.ln(8)
    pdf.body(
        f"I, {CUSTOMER} (Registration No: {REGNO}), student of {COURSE}, "
        f"{COLLEGE}, hereby declare that the project report entitled "
        f"BANKING DATABASE - Design and Implementation of a Banking "
        f"Database System using Oracle Database 21c - submitted to the "
        f"college, is an authentic record of work carried out by me under proper "
        f"supervision. The work presented in this report is original and has not "
        f"been submitted earlier for the award of any other degree or diploma. "
        f"All the data used in the implementation was generated on a live Oracle "
        f"Database 21c instance and the screenshots in this report are genuine "
        f"captures of that execution.")
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 7, f"Place : Kotagiri", 0, 1)
    pdf.cell(0, 7, f"Date  : 21 September 2026", 0, 1)
    pdf.ln(18)
    pdf.cell(0, 7, f"                                   {CUSTOMER}", 0, 1)
    pdf.cell(0, 7, f"                                   {REGNO}", 0, 1)

    # ============ TOC ============
    pdf.add_page()
    pdf.insert_toc_placeholder(render_toc, pages=1)

    # ============ CH 1 : INTRODUCTION ============
    pdf.chapter(1, "Introduction")
    pdf.h2("1.1  Problem Statement")
    pdf.body(
        "A bank handles three fundamental kinds of data: its customers, the "
        "accounts they hold, and the transactions performed on those accounts. "
        "When such data is kept in registers or flat files, errors such as "
        "duplicate records, missing account references and inconsistent "
        "balances are inevitable. This project designs and implements a "
        "relational banking database on Oracle Database 21c Express Edition in "
        "which every business rule - from a valid 10-digit phone number to an "
        "insufficient-balance check on withdrawal - is enforced inside the "
        "database itself, so that the data stays correct no matter which "
        "application uses it.")
    pdf.h2("1.2  Objectives")
    pdf.bullets([
        "Model the banking domain using the Entity-Relationship approach with "
        "CUSTOMER, ACCOUNT and TRANSACTION entities.",
        "Support multiple account types per customer - Savings, Current and "
        "Fixed deposit accounts.",
        "Enforce data integrity using primary keys, foreign keys, unique keys, "
        "check constraints and regular-expression validation.",
        "Automate deposits and withdrawals with PL/SQL stored procedures that "
        "validate input, update balances atomically and log every transaction "
        "with its running balance.",
        "Provide standard reporting queries: customer details, account summary, "
        "complete transaction history and a bank-level summary.",
        "Demonstrate the complete system on a live Oracle 21c instance with "
        "realistic sample data and document every step with screenshots.",
    ])
    pdf.h2("1.3  Scope")
    pdf.body(
        "The system covers the core back-office data layer of a small branch "
        "bank: customer onboarding data, account opening, money movement "
        "(deposit and withdrawal), and transaction auditing. It is a single-"
        "instance relational database; multi-branch replication, online "
        "transfer settlement and a customer-facing front end are outside the "
        "scope of this project.")
    pdf.h2("1.4  Advantages of the Database Approach")
    pdf.bullets([
        "Data integrity is guaranteed by the DBMS constraints rather than by "
        "application code.",
        "Every rupee movement leaves an audit trail with the resulting "
        "balance, which supports dispute resolution and reconciliation.",
        "Stored procedures make business rules reusable and consistent across "
        "all users of the database.",
        "Standard SQL queries allow instant reporting without additional "
        "tooling.",
    ])

    # ============ CH 2 : SYSTEM DESIGN ============
    pdf.chapter(2, "System Design")
    pdf.h2("2.1  Requirements")
    pdf.body("Software requirements:", 10.5)
    pdf.data_table(
        ["Item", "Version / Detail"],
        [["DBMS", "Oracle Database 21c Express Edition (21.3.0.0.0)"],
         ["Database instance", "Oracle XE - PDB: XEPDB1"],
         ["Development tool", "SQL*Plus (sqlplus)"],
         ["PL/SQL", "Oracle PL/SQL engine (built-in)"],
         ["Operating system", "Oracle Linux (Docker container)"]],
        [55, 125])
    pdf.ln(2)
    pdf.body("Hardware / execution environment:", 10.5)
    pdf.body(
        "The database runs as an Oracle XE 21c container (image "
        "gvenzl/oracle-xe:21.3.0-slim) on a standard Linux host with 4 GB RAM. "
        "The minimum requirement of Oracle XE 21c is a 64-bit OS, 1 GB of "
        "RAM and 2 GB of disk space, all of which are comfortably met.")

    pdf.h2("2.2  Entity-Relationship Diagram")
    pdf.body(
        "The conceptual model contains three entities. A customer OPENS one "
        "or more accounts (1:M) and each account RECORDS_IN one or more "
        "transactions (1:M). The relationship diagram is shown in Figure 2.1.")
    pdf.figure(f"{IMG}/er_diagram.png",
               "Figure 2.1  -  ER Diagram of the Banking Database")
    pdf.body(
        "Primary keys are underlined conceptsually and marked (PK); foreign "
        "keys (FK) enforce the two one-to-many relationships. The account_no "
        "column uses a 12-digit numeric format so that an account number can "
        "carry branch and sequence information; in this project the accounts "
        "numbered 100010000001 to 100010000007 are used.")

    pdf.h2("2.3  Table Structures")
    pdf.body("Table 2.1 - CUSTOMER (customer master data)", 10.5)
    pdf.data_table(
        ["Attribute", "Data Type", "Constraint / Remark"],
        [["customer_id", "NUMBER(2)", "Primary key"],
         ["first_name", "VARCHAR2(30)", "NOT NULL"],
         ["last_name", "VARCHAR2(30)", "NOT NULL"],
         ["email", "VARCHAR2(60)", "NOT NULL, UNIQUE"],
         ["phone", "VARCHAR2(10)", "CHECK: starts with 9, exactly 10 digits"],
         ["date_of_birth", "DATE", ""],
         ["address", "VARCHAR2(100)", ""],
         ["city", "VARCHAR2(50)", ""],
         ["created_on", "DATE", "Default SYSDATE"]],
        [42, 42, 96])
    pdf.ln(1)
    pdf.body("Table 2.2 - ACCOUNT (bank accounts)", 10.5)
    pdf.data_table(
        ["Attribute", "Data Type", "Constraint / Remark"],
        [["account_no", "NUMBER(12)", "Primary key"],
         ["customer_id", "NUMBER(2)", "Foreign key -> CUSTOMER"],
         ["account_type", "VARCHAR2(10)", "CHECK in (SAVINGS, CURRENT, FIXED)"],
         ["opening_balance", "NUMBER(12,2)", "DEFAULT 0"],
         ["current_balance", "NUMBER(12,2)", "DEFAULT 0, CHECK >= 0"],
         ["status", "VARCHAR2(10)", "CHECK in (ACTIVE, CLOSED), DEFAULT ACTIVE"],
         ["opened_on", "DATE", "DEFAULT SYSDATE"]],
        [42, 42, 96])
    pdf.ln(1)
    pdf.body("Table 2.3 - TRANSACTION (transaction history / audit trail)", 10.5)
    pdf.data_table(
        ["Attribute", "Data Type", "Constraint / Remark"],
        [["txn_id", "NUMBER(5)", "Primary key (sequence-generated)"],
         ["account_no", "NUMBER(12)", "Foreign key -> ACCOUNT"],
         ["txn_date", "DATE", "DEFAULT SYSDATE"],
         ["txn_type", "VARCHAR2(10)", "CHECK in (DEPOSIT, WITHDRAWAL)"],
         ["amount", "NUMBER(12,2)", "CHECK > 0"],
         ["balance_after", "NUMBER(12,2)", "Running balance after this txn"],
         ["description", "VARCHAR2(100)", "Free-text remarks"]],
        [42, 42, 96])

    pdf.h2("2.4  Integrity Constraints and Business Rules")
    pdf.bullets([
        "CK_CUSTOMER_PHONE - phone must match the pattern ^9[0-9]{9}$ "
        "(Indian mobile number).",
        "UK_CUSTOMER_EMAIL - one customer per email address.",
        "FK_ACCOUNT_CUSTOMER - an account must belong to an existing "
        "customer.",
        "CK_ACCOUNT_TYPE - only SAVINGS, CURRENT and FIXED accounts.",
        "CK_ACCT_BALANCE / CK_ACCT_STATUS - balance can never go negative and "
        "status is limited to ACTIVE / CLOSED.",
        "FK_TXN_ACCOUNT - a transaction must reference an existing account.",
        "Business rules (PL/SQL): deposits must be positive; withdrawals are "
        "rejected when the balance is insufficient or the account is missing / "
        "not active; every successful movement writes a TRANSACTION row and "
        "updates current_balance in the same transaction.",
    ])

    # ============ CH 3 : IMPLEMENTATION ============
    pdf.chapter(3, "Database Implementation")
    pdf.h2("3.1  Environment")
    pdf.body(
        "The database is an Oracle XE 21.3.0.0.0 instance running in a Docker "
        "container. Sessions connect through SQL*Plus to the pluggable "
        "database XEPDB1 with the SYSTEM account. All objects were created in "
        "the SYSTEM schema. The scripts in the sql/ directory of the project "
        "repository are executed in the order 00 -> 06; the complete listing "
        "of each script is given below.")
    pdf.h2("3.2  Schema Creation (DDL)")
    pdf.body("Script: sql/01_create_schema.sql - sequences and the three tables with all constraints:")
    pdf.code(read_sql("01_create_schema.sql"))
    pdf.h2("3.3  PL/SQL Stored Procedures")
    pdf.body(
        "Three procedures implement the business rules. deposit_funds and "
        "withdraw_funds validate the input, lock the account row (FOR UPDATE), "
        "update the balance and insert the audit row atomically; open_account "
        "creates a new account for an existing customer.")
    pdf.code(read_sql("03_procedures.sql"))
    pdf.h2("3.4  Customer Master Data")
    pdf.body("Script: sql/02a_customers.sql - six customers covering Kotagiri, Coimbatore, Ooty and Pollachi:")
    pdf.code(read_sql("02a_customers.sql"))
    pdf.h2("3.5  Account Opening")
    pdf.body("Script: sql/02b_accounts.sql - seven accounts across the three account types:")
    pdf.code(read_sql("02b_accounts.sql"))
    pdf.h2("3.6  Deposit and Withdrawal Transactions")
    pdf.body("Script: sql/04a_deposits.sql - three successful deposits (salary credit, cash deposit, FD interest):")
    pdf.code(read_sql("04a_deposits.sql"))
    pdf.ln(0)
    pdf.body("Script: sql/04b_withdrawals.sql - two successful withdrawals plus two deliberate error cases (insufficient balance, invalid account number):")
    pdf.code(read_sql("04b_withdrawals.sql"))
    pdf.h2("3.7  Reporting Queries and View")
    pdf.body("Script: sql/05_demo_queries.sql - customer details, account summary with holder names, full transaction history, and the bank_summary view:")
    pdf.code(read_sql("05_demo_queries.sql"))
    pdf.h2("3.8  Constraint and Validation Tests")
    pdf.body("Script: sql/06_test_cases.sql - exercises every constraint and the procedure-level validations (see Chapter 6):")
    pdf.code(read_sql("06_test_cases.sql"))

    # ============ CH 4 : SCREENSHOTS ============
    pdf.chapter(4, "Implementation Screenshots")
    pdf.body(
        "This chapter contains genuine SQL*Plus captures taken from the live "
        "Oracle XE 21c instance while executing the scripts of Chapter 3. The "
        "session banner confirms the database version: Oracle Database 21c "
        "Express Edition Release 21.0.0.0.0, SQL*Plus Release 21.0.0.0.0.")
    pdf.figure(f"{IMG}/er_connect.png", "Figure 4.1  -  SQL*Plus connection to Oracle 21c and version check")
    pdf.figure(f"{IMG}/er_schema1.png", "Figure 4.2  -  Schema creation (part 1): sequence and CUSTOMER table")
    pdf.figure(f"{IMG}/er_schema2.png", "Figure 4.3  -  Schema creation (part 2): ACCOUNT and TRANSACTION tables")
    pdf.figure(f"{IMG}/er_customers.png", "Figure 4.4  -  Inserting customer master data and displaying customer information")
    pdf.figure(f"{IMG}/er_accounts.png", "Figure 4.5  -  Creating the seven bank accounts and displaying the account list")
    pdf.figure(f"{IMG}/er_proc1.png", "Figure 4.6  -  DEPOSIT_FUNDS stored procedure")
    pdf.figure(f"{IMG}/er_proc2.png", "Figure 4.7  -  WITHDRAW_FUNDS stored procedure")
    pdf.figure(f"{IMG}/er_proc3.png", "Figure 4.8  -  OPEN_ACCOUNT stored procedure")
    pdf.figure(f"{IMG}/er_deposits.png", "Figure 4.9  -  Executing three deposits through DEPOSIT_FUNDS")
    pdf.figure(f"{IMG}/er_withdrawals.png", "Figure 4.10  -  Withdrawals: two successes and two controlled error cases")
    pdf.figure(f"{IMG}/er_history.png", "Figure 4.11  -  Transaction history and per-account summary")
    pdf.figure(f"{IMG}/er_summary.png", "Figure 4.12  -  bank_summary view: customer, holder and account-wise balances")
    pdf.figure(f"{IMG}/er_tests.png", "Figure 4.13  -  Constraint violation and validation tests (ORA errors)")

    # ============ CH 5 : DATA AND RESULTS ============
    pdf.chapter(5, "Sample Data and Results")
    pdf.h2("5.1  Customer Master Data")
    pdf.data_table(
        ["ID", "Name", "Email", "Phone", "DOB", "City"],
        [["1", "Arun Kumar", "arun.kumar@gmail.com", "9843012345", "12-APR-1988", "Kotagiri"],
         ["2", "Priya Lakshmi", "priya.l@gmail.com", "9791122334", "25-AUG-1992", "Coimbatore"],
         ["3", "Mohammed Rasheed", "rasheed.m@yahoo.com", "9442233445", "30-JAN-1990", "Kotagiri"],
         ["4", "Kavya S", "kavya.s@outlook.com", "9003344556", "02-NOV-1995", "Ooty"],
         ["5", "Suresh Babu", "suresh.b@gmail.com", "9864455667", "18-JUN-1985", "Pollachi"],
         ["6", "Divya R", "divya.r@gmail.com", "9952266778", "09-MAR-1998", "Kotagiri"]],
        [10, 38, 42, 22, 22, 26])
    pdf.h2("5.2  Accounts and Final Balances")
    pdf.body(
        "The current_balance column reflects the five successful transactions "
        "of Section 5.3 (the two failed withdrawals left the balances "
        "unchanged).")
    pdf.data_table(
        ["Account No", "Holder", "Type", "Opening", "Final Balance", "Status"],
        [["100010000001", "Arun Kumar", "SAVINGS", "10,000.00", "15,000.00", "ACTIVE"],
         ["100010000002", "Arun Kumar", "CURRENT", "25,000.00", "22,500.00", "ACTIVE"],
         ["100010000003", "Priya Lakshmi", "SAVINGS", "15,000.00", "35,000.00", "ACTIVE"],
         ["100010000004", "Mohammed Rasheed", "FIXED", "100,000.00", "112,000.00", "ACTIVE"],
         ["100010000005", "Kavya S", "SAVINGS", "8,000.00", "8,000.00", "ACTIVE"],
         ["100010000006", "Suresh Babu", "CURRENT", "50,000.00", "45,000.00", "ACTIVE"],
         ["100010000007", "Divya R", "SAVINGS", "5,000.00", "5,000.00", "ACTIVE"]],
        [30, 34, 20, 22, 30, 18])
    pdf.h2("5.3  Transaction History (Audit Trail)")
    pdf.data_table(
        ["Txn", "Account No", "Date", "Type", "Amount (Rs.)", "Balance After (Rs.)", "Description"],
        [["1001", "100010000001", "21-SEP-2026", "DEPOSIT", "5,000.00", "15,000.00", "Salary Credit"],
         ["1002", "100010000003", "21-SEP-2026", "DEPOSIT", "20,000.00", "35,000.00", "Cash Deposit"],
         ["1003", "100010000004", "21-SEP-2026", "DEPOSIT", "12,000.00", "112,000.00", "FD Interest"],
         ["1004", "100010000002", "21-SEP-2026", "WITHDRAWAL", "2,500.00", "22,500.00", "ATM Withdrawal"],
         ["1005", "100010000006", "21-SEP-2026", "WITHDRAWAL", "5,000.00", "45,000.00", "NEFT Transfer"]],
        [12, 28, 22, 20, 20, 26, 28])
    pdf.body(
        "Note: the attempted withdrawal of Rs.10,000 from account "
        "100010000005 (balance Rs.8,000) and the withdrawal from the "
        "non-existent account 999999999999 were rejected by WITHDRAW_FUNDS and "
        "deliberately leave no row in the TRANSACTION table - the audit trail "
        "contains only money that actually moved.")

    # ============ CH 6 : TESTING ============
    pdf.chapter(6, "Testing and Verification")
    pdf.body(
        "The system was tested on the live database after loading the sample "
        "data. TC-01 to TC-12 below cover the stored procedures, the "
        "constraint layer and the reporting queries; the corresponding "
        "screenshots appear in Chapter 4 (Figures 4.9-4.13).")
    pdf.data_table(
        ["Test", "Case", "Expected Result", "Observed Result", "Status"],
        [["TC-01", "Deposit Rs.5,000 into 100010000001", "SUCCESS; balance 10,000 -> 15,000; txn 1001", "As expected", "PASS"],
         ["TC-02", "Deposit Rs.20,000 into 100010000003", "SUCCESS; balance 15,000 -> 35,000; txn 1002", "As expected", "PASS"],
         ["TC-03", "Deposit Rs.12,000 into FIXED 100010000004", "SUCCESS; balance 100,000 -> 112,000; txn 1003", "As expected", "PASS"],
         ["TC-04", "Withdraw Rs.2,500 from 100010000002", "SUCCESS; balance 25,000 -> 22,500; txn 1004", "As expected", "PASS"],
         ["TC-05", "Withdraw Rs.5,000 from 100010000006", "SUCCESS; balance 50,000 -> 45,000; txn 1005", "As expected", "PASS"],
         ["TC-06", "Withdraw Rs.10,000 from 100010000005 (bal. Rs.8,000)", "ERROR: insufficient balance; balance unchanged; no txn row", "ERROR : Insufficient balance. Available Rs. 8,000.00, requested Rs. 10,000.00", "PASS"],
         ["TC-07", "Withdraw Rs.1,000 from 999999999999", "ERROR: account not found or not active", "ERROR : Account 999999999999 not found or not active.", "PASS"],
         ["TC-08", "INSERT customer with phone '12345'", "ORA-02290 (CK_CUSTOMER_PHONE)", "ORA-02290: check constraint violated", "PASS"],
         ["TC-09", "INSERT account of type 'LOAN'", "ORA-02290 (CK_ACCOUNT_TYPE)", "ORA-02290: check constraint violated", "PASS"],
         ["TC-10", "INSERT customer with duplicate email", "ORA-00001 (UK_CUSTOMER_EMAIL)", "ORA-00001: unique constraint violated", "PASS"],
         ["TC-11", "INSERT account for customer 999", "ORA-02291 (FK_ACCOUNT_CUSTOMER)", "ORA-02291: parent key not found", "PASS"],
         ["TC-12", "Deposit of Rs.-500 (negative amount)", "Procedure validation error; no row written", "ERROR : Deposit amount must be greater than zero.", "PASS"]],
        [14, 44, 40, 56, 16])
    pdf.body(
        "All 12 test cases passed. Every rejected operation was confirmed to "
        "have left the account balances and the transaction history unchanged.")

    # ============ CH 7 : CONCLUSION ============
    pdf.chapter(7, "Conclusion and Future Scope")
    pdf.h2("7.1  Conclusion")
    pdf.body(
        "A complete relational banking database was designed and implemented "
        "on Oracle Database 21c Express Edition. The three-table model with "
        "primary/foreign keys, check constraints and regular-expression "
        "validation keeps the customer, account and transaction data "
        "consistent, while the PL/SQL procedures deposit_funds, "
        "withdraw_funds and open_account automate the "
        "money movement with full error handling and an audit trail that "
        "records the running balance after every transaction. The controlled "
        "error tests (insufficient balance, unknown account, invalid phone, "
        "invalid account type, duplicate email, unknown customer) demonstrate "
        "that the database rejects every form of bad data, and the reporting "
        "queries and bank_summary view confirm that the data is immediately "
        "usable for day-to-day banking operations.")
    pdf.h2("7.2  Future Scope")
    pdf.bullets([
        "Interest computation for savings and fixed accounts using triggers or "
        "scheduled PL/SQL jobs.",
        "Inter-account fund transfer procedure with two-phase balance updates.",
        "Web or desktop front end (e.g. Flask / Java) over the same schema.",
        "Role-based users (teller, clerk, manager) with fine-grained grants.",
        "Partitioning of the TRANSACTION table for high-volume branches.",
    ])

    # ============ REFERENCES ============
    pdf.add_page()
    pdf.start_section("References")
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 10, "References", 0, 1)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    refs = [
        "Oracle Database SQL Language Reference Guide, 21c Release 1 (21.3) - Oracle Corporation.",
        "Oracle Database PL/SQL Language User's Guide and Reference, 21c Release 1 (21.3) - Oracle Corporation.",
        "Oracle Database Express Edition 21c Documentation - Oracle Corporation, https://www.oracle.com/database/technologies/express-edition-downloads.html",
        f"Project source code, screenshots and this report - {GITHUB}",
    ]
    for i, r in enumerate(refs, 1):
        pdf.cell(8, 6, f"[{i}]")
        pdf.multi_cell(0, 6, r)
        pdf.set_x(pdf.l_margin)
        pdf.ln(2)

    pdf.output(OUT)
    print("PDF written:", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
