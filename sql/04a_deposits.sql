-- DEPOSIT TRANSACTIONS
SET SERVEROUTPUT ON SIZE UNLIMITED
SET ECHO OFF
SET DEFINE OFF

PROMPT === DEPOSIT TRANSACTIONS (DEPOSIT_FUNDS PROCEDURE) ===

PROMPT [TXN-1] Deposit Rs.5,000 into account 100010000001 (Arun Kumar - SAVINGS)
PROMPT SQL> DECLARE v_status VARCHAR2(200); BEGIN deposit_funds(100010000001, 5000, 'Salary Credit'
PROMPT        v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
PROMPT SQL> /
DECLARE v_status VARCHAR2(200); BEGIN deposit_funds(100010000001, 5000, 'Salary Credit', v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
/

PROMPT [TXN-2] Deposit Rs.20,000 into account 100010000003 (Priya Lakshmi - SAVINGS)
PROMPT SQL> DECLARE v_status VARCHAR2(200); BEGIN deposit_funds(100010000003, 20000, 'Cash Deposit'
PROMPT        v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
PROMPT SQL> /
DECLARE v_status VARCHAR2(200); BEGIN deposit_funds(100010000003, 20000, 'Cash Deposit', v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
/

PROMPT [TXN-3] Deposit Rs.12,000 into account 100010000004 (Mohammed Rasheed - FIXED)
PROMPT SQL> DECLARE v_status VARCHAR2(200); BEGIN deposit_funds(100010000004, 12000, 'FD Interest'
PROMPT        v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
PROMPT SQL> /
DECLARE v_status VARCHAR2(200); BEGIN deposit_funds(100010000004, 12000, 'FD Interest', v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
/
