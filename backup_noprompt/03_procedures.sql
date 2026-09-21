-- PL/SQL PROCEDURES
SET ECHO OFF
SET FEEDBACK ON
SET DEFINE OFF
SET SERVEROUTPUT ON SIZE UNLIMITED

PROMPT === CREATE PROCEDURE DEPOSIT_FUNDS ===
CREATE OR REPLACE PROCEDURE deposit_funds (
    p_account_no   IN  NUMBER,
    p_amount       IN  NUMBER,
    p_description  IN  VARCHAR2  DEFAULT 'Cash Deposit',
    p_status       OUT VARCHAR2
) IS
    v_balance NUMBER(12,2);
BEGIN
    SELECT current_balance INTO v_balance
    FROM   account
    WHERE  account_no = p_account_no AND status = 'ACTIVE'
    FOR UPDATE;

    IF p_amount <= 0 THEN
        p_status := 'ERROR : Deposit amount must be greater than zero.';
        ROLLBACK;
        RETURN;
    END IF;

    UPDATE account
    SET    current_balance = current_balance + p_amount
    WHERE  account_no = p_account_no;

    INSERT INTO transaction (txn_id, account_no, txn_type, amount, balance_after, description)
    VALUES (seq_txn.NEXTVAL, p_account_no, 'DEPOSIT', p_amount, v_balance + p_amount, p_description);

    COMMIT;
    p_status := 'SUCCESS : Rs.' || TO_CHAR(p_amount, '999,999,990.00') || ' deposited to account ' || p_account_no ||
               '. New balance Rs.' || TO_CHAR(v_balance + p_amount, '999,999,990.00');
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR : Account ' || p_account_no || ' not found or not active.';
END deposit_funds;
/

PROMPT === CREATE PROCEDURE WITHDRAW_FUNDS ===
CREATE OR REPLACE PROCEDURE withdraw_funds (
    p_account_no   IN  NUMBER,
    p_amount       IN  NUMBER,
    p_description  IN  VARCHAR2  DEFAULT 'ATM Withdrawal',
    p_status       OUT VARCHAR2
) IS
    v_balance NUMBER(12,2);
BEGIN
    SELECT current_balance INTO v_balance
    FROM   account
    WHERE  account_no = p_account_no AND status = 'ACTIVE'
    FOR UPDATE;

    IF p_amount <= 0 THEN
        p_status := 'ERROR : Withdrawal amount must be greater than zero.';
        ROLLBACK;
        RETURN;
    END IF;

    IF p_amount > v_balance THEN
        p_status := 'ERROR : Insufficient balance. Available Rs.' || TO_CHAR(v_balance, '999,999,990.00') ||
                    ', requested Rs.' || TO_CHAR(p_amount, '999,999,990.00');
        ROLLBACK;
        RETURN;
    END IF;

    UPDATE account
    SET    current_balance = current_balance - p_amount
    WHERE  account_no = p_account_no;

    INSERT INTO transaction (txn_id, account_no, txn_type, amount, balance_after, description)
    VALUES (seq_txn.NEXTVAL, p_account_no, 'WITHDRAWAL', p_amount, v_balance - p_amount, p_description);

    COMMIT;
    p_status := 'SUCCESS : Rs.' || TO_CHAR(p_amount, '999,999,990.00') || ' withdrawn from account ' || p_account_no ||
               '. New balance Rs.' || TO_CHAR(v_balance - p_amount, '999,999,990.00');
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        p_status := 'ERROR : Account ' || p_account_no || ' not found or not active.';
END withdraw_funds;
/

PROMPT === CREATE PROCEDURE OPEN_ACCOUNT ===
CREATE OR REPLACE PROCEDURE open_account (
    p_customer_id  IN  NUMBER,
    p_account_type IN  VARCHAR2,
    p_opening_bal  IN  NUMBER    DEFAULT 0,
    p_status       OUT VARCHAR2
) IS
    v_acct_no NUMBER(12);
    v_count   NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM customer WHERE customer_id = p_customer_id;
    IF v_count = 0 THEN
        p_status := 'ERROR : Customer ' || p_customer_id || ' does not exist.';
        RETURN;
    END IF;

    IF p_account_type NOT IN ('SAVINGS','CURRENT','FIXED') THEN
        p_status := 'ERROR : Invalid account type. Use SAVINGS, CURRENT or FIXED.';
        RETURN;
    END IF;

    v_acct_no := seq_acct.NEXTVAL;
    INSERT INTO account (account_no, customer_id, account_type, opening_balance, current_balance, status, opened_on)
    VALUES (v_acct_no, p_customer_id, p_account_type, p_opening_bal, p_opening_bal, 'ACTIVE', SYSDATE);

    COMMIT;
    p_status := 'SUCCESS : Account ' || v_acct_no || ' (' || p_account_type || ') opened for customer ' || p_customer_id ||
               ' with opening balance Rs.' || TO_CHAR(p_opening_bal, '999,999,990.00');
END open_account;
/

PROMPT === All PL/SQL procedures created successfully ===
