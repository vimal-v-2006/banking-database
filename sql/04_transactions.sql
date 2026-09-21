-- =====================================================================
--  BANKING DATABASE - TRANSACTION DEMO (Deposits & Withdrawals)
-- =====================================================================
SET SERVEROUTPUT ON SIZE UNLIMITED
SET ECHO OFF

PROMPT === DEPOSIT TRANSACTIONS ===
PROMPT [TXN-1] Deposit Rs.5,000   into account 100010000001 (Arun Kumar - SAVINGS)
DECLARE
    v_status VARCHAR2(200);
BEGIN
    deposit_funds(100010000001, 5000, 'Salary Credit', v_status);
    DBMS_OUTPUT.PUT_LINE(v_status);
END;
/

PROMPT [TXN-2] Deposit Rs.20,000  into account 100010000003 (Priya Lakshmi - SAVINGS)
DECLARE
    v_status VARCHAR2(200);
BEGIN
    deposit_funds(100010000003, 20000, 'Cash Deposit', v_status);
    DBMS_OUTPUT.PUT_LINE(v_status);
END;
/

PROMPT [TXN-3] Deposit Rs.12,000  into account 100010000004 (Mohammed Rasheed - FIXED)
DECLARE
    v_status VARCHAR2(200);
BEGIN
    deposit_funds(100010000004, 12000, 'FD Interest', v_status);
    DBMS_OUTPUT.PUT_LINE(v_status);
END;
/

PROMPT === WITHDRAWAL TRANSACTIONS ===
PROMPT [TXN-4] Withdraw Rs.2,500  from account 100010000002 (Arun Kumar - CURRENT)
DECLARE
    v_status VARCHAR2(200);
BEGIN
    withdraw_funds(100010000002, 2500, 'ATM Withdrawal', v_status);
    DBMS_OUTPUT.PUT_LINE(v_status);
END;
/

PROMPT [TXN-5] Withdraw Rs.5,000  from account 100010000006 (Suresh Babu - CURRENT)
DECLARE
    v_status VARCHAR2(200);
BEGIN
    withdraw_funds(100010000006, 5000, 'NEFT Transfer', v_status);
    DBMS_OUTPUT.PUT_LINE(v_status);
END;
/

PROMPT [TXN-6] Withdraw Rs.10,000 from account 100010000005 (Kavya S - SAVINGS)
DECLARE
    v_status VARCHAR2(200);
BEGIN
    withdraw_funds(100010000005, 10000, 'ATM Withdrawal', v_status);
    DBMS_OUTPUT.PUT_LINE(v_status);
END;
/

PROMPT [TXN-7] Withdraw Rs.1,000  from account 999999999999 (invalid account)
DECLARE
    v_status VARCHAR2(200);
BEGIN
    withdraw_funds(999999999999, 1000, 'ATM Withdrawal', v_status);
    DBMS_OUTPUT.PUT_LINE(v_status);
END;
/
