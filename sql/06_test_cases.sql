-- Banking Database : Test Cases (constraint and validation tests)
SET DEFINE OFF
SET ECHO OFF
SET FEEDBACK ON

PROMPT SQL> === TEST 1 : Invalid phone number (CHECK constraint) ===
PROMPT SQL> INSERT INTO customer VALUES (9, 'Test', 'User', 't@x.com', '12345', TO_DATE('01-JAN-1990','DD-MON-YYYY'), 'Test St', 'Kotagiri', SYSDATE);
INSERT INTO customer VALUES (9, 'Test', 'User', 't@x.com', '12345', TO_DATE('01-JAN-1990','DD-MON-YYYY'), 'Test St', 'Kotagiri', SYSDATE);

PROMPT SQL> === TEST 2 : Invalid account type (CHECK constraint) ===
PROMPT SQL> INSERT INTO account VALUES (100010000099, 1, 'LOAN', 1000, 1000, 'ACTIVE', SYSDATE);
INSERT INTO account VALUES (100010000099, 1, 'LOAN', 1000, 1000, 'ACTIVE', SYSDATE);

PROMPT SQL> === TEST 3 : Negative deposit amount (procedure validation) ===
PROMPT SQL> DECLARE v_status VARCHAR2(200); BEGIN deposit_funds(100010000001, -500, 'Bad Deposit', v_status);
PROMPT        DBMS_OUTPUT.PUT_LINE(v_status); END;
PROMPT SQL> /
DECLARE v_status VARCHAR2(200); BEGIN deposit_funds(100010000001, -500, 'Bad Deposit', v_status);
DBMS_OUTPUT.PUT_LINE(v_status); END;
/

PROMPT SQL> === TEST 4 : Duplicate email (UNIQUE constraint) ===
PROMPT SQL> INSERT INTO customer VALUES (10, 'Dup', 'Email', 'arun.kumar@gmail.com', '9876543210', TO_DATE('01-JAN-1990','DD-MON-YYYY'), 'St', 'City', SYSDATE);
INSERT INTO customer VALUES (10, 'Dup', 'Email', 'arun.kumar@gmail.com', '9876543210', TO_DATE('01-JAN-1990','DD-MON-YYYY'), 'St', 'City', SYSDATE);

PROMPT SQL> === TEST 5 : Unknown customer (FOREIGN KEY constraint) ===
PROMPT SQL> INSERT INTO account VALUES (100010000098, 999, 'SAVINGS', 1000, 1000, 'ACTIVE', SYSDATE);
INSERT INTO account VALUES (100010000098, 999, 'SAVINGS', 1000, 1000, 'ACTIVE', SYSDATE);

EXIT
