-- =====================================================================
--  BANKING DATABASE - REPORTING QUERIES
-- =====================================================================
SET ECHO OFF
SET DEFINE OFF
SET PAGESIZE 100 LINESIZE 170
SET FEEDBACK ON
COL account_no  FORMAT 999999999999
COL name        FORMAT A22
COL type        FORMAT A8
COL open_bal    FORMAT 99,999,990.00
COL cur_bal     FORMAT 99,999,990.00
COL status      FORMAT A8
COL opened_on   FORMAT A12
COL txn_id      FORMAT 99999
COL txn_date    FORMAT A20
COL ttype       FORMAT A10
COL amount      FORMAT 9,999,990.00
COL bal_after   FORMAT 9,999,990.00
COL remark      FORMAT A18

PROMPT === 3. TRANSACTION HISTORY - Account 100010000001 ===
SELECT txn_id,
       TO_CHAR(txn_date,'DD-MON-YYYY HH24:MI:SS') AS txn_date,
       txn_type AS ttype,
       amount,
       balance_after AS bal_after,
       description AS remark
FROM   transaction
WHERE  account_no = 100010000001
ORDER BY txn_date;

PROMPT === 4. COMPLETE TRANSACTION HISTORY (all accounts) ===
SELECT txn_id,
       account_no,
       TO_CHAR(txn_date,'DD-MON-YYYY HH24:MI') AS txn_date,
       txn_type AS ttype,
       amount,
       balance_after AS bal_after,
       description AS remark
FROM   transaction
ORDER BY txn_date, txn_id;

PROMPT === 5. BANK SUMMARY ===
SELECT 'TOTAL CUSTOMERS'   AS metric, TO_CHAR(COUNT(*), '9999')                 AS value FROM customer
UNION ALL
SELECT 'TOTAL ACCOUNTS'    AS metric, TO_CHAR(COUNT(*), '9999')                 AS value FROM account
UNION ALL
SELECT 'TOTAL DEPOSITS'    AS metric, TO_CHAR(SUM(amount), '9,999,990.00')      AS value FROM transaction WHERE txn_type = 'DEPOSIT'
UNION ALL
SELECT 'TOTAL WITHDRAWALS' AS metric, TO_CHAR(SUM(amount), '9,999,990.00')      AS value FROM transaction WHERE txn_type = 'WITHDRAWAL'
UNION ALL
SELECT 'TOTAL BANK BALANCE' AS metric, TO_CHAR(SUM(current_balance), '9,999,990.00') AS value FROM account;
