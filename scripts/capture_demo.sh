#!/bin/bash
# =====================================================================
#  Runs the full Banking Database demo on Oracle XE 21c and captures
#  real SQL*Plus session output for the report screenshots.
#  Usage: ./capture_demo.sh  (project root)
# =====================================================================
set -e
cd "$(dirname "$0")/.."
SQLDIR=sql
OUT=report/output
DB="system/Oracle_123@localhost/XEPDB1"
mkdir -p "$OUT"

run_sql() {
    local name="$1"; local file="$2"
    echo "[capture] $name <- $file"
    docker exec -i oraclexe bash -lc "sqlplus -L $DB" < "$SQLDIR/$file" > "$OUT/$name.txt" 2>&1
}

# 0. cleanup (output not captured)
docker exec -i oraclexe bash -lc "sqlplus -L $DB" < "$SQLDIR/00_cleanup.sql" > /dev/null 2>&1

# 1. connection + version banner
printf 'SET PAGESIZE 50 LINESIZE 170\nSET ECHO OFF\nPROMPT SQL> SELECT banner FROM v$version;\nSELECT banner FROM v$version;\n' \
  | docker exec -i oraclexe bash -lc "sqlplus -L $DB" > "$OUT/ss1_version.txt" 2>&1

run_sql ss2_schema      01_create_schema.sql
run_sql ss3_customers   02a_customers.sql
run_sql ss4_accounts    02b_accounts.sql
run_sql ss5_procedures  03_procedures.sql
run_sql ss6_deposits    04a_deposits.sql
run_sql ss7_withdrawals 04b_withdrawals.sql
run_sql ss8_report      05_demo_queries.sql

echo "DONE"
ls -la "$OUT"
