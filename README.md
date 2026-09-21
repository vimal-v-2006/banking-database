# Banking Database

A **Banking Database** project designed and implemented on **Oracle Database 21c Express Edition**.
The project models a small bank with customers, bank accounts (Savings / Current / Fixed) and
transactions, enforced with integrity constraints and business rules implemented in **PL/SQL**.

## Student Details

| Field        | Value                                              |
|--------------|----------------------------------------------------|
| Name         | Vimal                                              |
| Registration | 2422J1256                                          |
| College      | Kaypeeyes College of Arts and Science, Kotagiri    |
| Course       | III BCA                                            |
| Academic Yr  | 2026 - 2027                                        |

## Features

- Customer master data with phone / email integrity constraints
- Multiple account types per customer: **SAVINGS, CURRENT, FIXED**
- Deposits and withdrawals through **PL/SQL stored procedures**
  (`deposit_funds`, `withdraw_funds`, `open_account`)
- Automatic **transaction history** with running balance
- Error handling: insufficient balance, invalid / inactive account, invalid input
- Sample seed data and demo queries with complete screenshots
- Full project report (PDF) with ER diagram, DDL, PL/SQL code and test results

## Schema Overview

```
CUSTOMER (customer_id PK, first_name, last_name, email UK, phone, date_of_birth,
          address, city, created_on)
    |  1 ---< OPENS >--- M
    v
ACCOUNT (account_no PK, customer_id FK, account_type CK, opening_balance,
         current_balance, status CK, opened_on)
    |  1 ---< RECORDS_IN >--- M
    v
TRANSACTION (txn_id PK, account_no FK, txn_date, txn_type CK, amount,
             balance_after, description)
```

## Directory Layout

```
sql/          Oracle SQL scripts (run in order 00 -> 05)
scripts/      Helper scripts (screenshot renderer, capture runner, ER diagram, PDF builder)
report/       Final PDF report
  images/     Screenshots and ER diagram
  output/     Raw sqlplus captures
```

## How to Run

Requires an Oracle Database 21c instance (Oracle XE recommended, PDB `XEPDB1`).

```bash
sqlplus system/<password>@localhost/XEPDB1
SQL> @sql/00_cleanup.sql
SQL> @sql/01_create_schema.sql
SQL> @sql/02a_customers.sql
SQL> @sql/02b_accounts.sql
SQL> @sql/03_procedures.sql
SQL> @sql/04a_deposits.sql
SQL> @sql/04b_withdrawals.sql
SQL> @sql/05_demo_queries.sql
```

## Sample Output

```
SQL> EXEC ... withdraw_funds(100010000005, 10000, 'ATM Withdrawal', v_status); ...
ERROR : Insufficient balance. Available Rs.      8,000.00, requested Rs. 10,000.00
```
