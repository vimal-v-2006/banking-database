-- WITHDRAWAL TRANSACTIONS
SET SERVEROUTPUT ON SIZE UNLIMITED
SET ECHO OFF
SET DEFINE OFF

PROMPT === WITHDRAWAL TRANSACTIONS (WITHDRAW_FUNDS PROCEDURE) ===

PROMPT [TXN-4] Withdraw Rs.2,500 from account 100010000002 (Arun Kumar - CURRENT)
PROMPT SQL> DECLARE v_status VARCHAR2(200); BEGIN withdraw_funds(100010000002, 2500, 'ATM Withdrawal'
PROMPT        v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
PROMPT SQL> /
DECLARE v_status VARCHAR2(200); BEGIN withdraw_funds(100010000002, 2500, 'ATM Withdrawal', v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
/

PROMPT [TXN-5] Withdraw Rs.5,000 from account 100010000006 (Suresh Babu - CURRENT)
PROMPT SQL> DECLARE v_status VARCHAR2(200); BEGIN withdraw_funds(100010000006, 5000, 'NEFT Transfer'
PROMPT        v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
PROMPT SQL> /
DECLARE v_status VARCHAR2(200); BEGIN withdraw_funds(100010000006, 5000, 'NEFT Transfer', v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
/

PROMPT [TXN-6] Withdraw Rs.10,000 from account 100010000005 (Kavya S - SAVINGS)
PROMPT SQL> DECLARE v_status VARCHAR2(200); BEGIN withdraw_funds(100010000005, 10000, 'ATM Withdrawal'
PROMPT        v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
PROMPT SQL> /
DECLARE v_status VARCHAR2(200); BEGIN withdraw_funds(100010000005, 10000, 'ATM Withdrawal', v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
/

PROMPT [TXN-7] Withdraw Rs.1,000 from account 999999999999 (invalid account no.)
PROMPT SQL> DECLARE v_status VARCHAR2(200); BEGIN withdraw_funds(999999999999, 1000, 'ATM Withdrawal'
PROMPT        v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
PROMPT SQL> /
DECLARE v_status VARCHAR2(200); BEGIN withdraw_funds(999999999999, 1000, 'ATM Withdrawal', v_status); DBMS_OUTPUT.PUT_LINE(v_status); END;
/
