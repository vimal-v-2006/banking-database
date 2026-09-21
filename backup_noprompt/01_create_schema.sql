-- =====================================================================
--  BANKING DATABASE - SCHEMA CREATION SCRIPT
--  Database : Oracle Database XE 21c
-- =====================================================================
SET ECHO OFF
SET DEFINE OFF
SET FEEDBACK ON
SET PAGESIZE 100 LINESIZE 170

PROMPT === STEP 1 : Create sequences SEQ_TXN and SEQ_ACCT ===
CREATE SEQUENCE seq_txn  START WITH 1001  INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_acct START WITH 100010000001 INCREMENT BY 1 NOCACHE NOCYCLE;

PROMPT === STEP 2 : Create CUSTOMER table (customer information) ===
CREATE TABLE customer (
    customer_id    NUMBER(4)      CONSTRAINT pk_customer    PRIMARY KEY,
    first_name     VARCHAR2(30)   NOT NULL,
    last_name      VARCHAR2(30)   NOT NULL,
    email          VARCHAR2(50)   CONSTRAINT uk_customer_email UNIQUE NOT NULL,
    phone          VARCHAR2(15)   CONSTRAINT ck_customer_phone CHECK (REGEXP_LIKE(phone, '^9[0-9]{9}$')),
    date_of_birth  DATE,
    address        VARCHAR2(100),
    city           VARCHAR2(30)   DEFAULT 'Kotagiri',
    created_on     DATE           DEFAULT SYSDATE
);

PROMPT === STEP 3 : Create ACCOUNT table (account details and types) ===
CREATE TABLE account (
    account_no      NUMBER(12)    CONSTRAINT pk_account        PRIMARY KEY,
    customer_id     NUMBER(4)     CONSTRAINT fk_account_customer REFERENCES customer(customer_id),
    account_type    VARCHAR2(10)  CONSTRAINT ck_account_type   CHECK (account_type IN ('SAVINGS','CURRENT','FIXED')),
    opening_balance NUMBER(12,2)  DEFAULT 0,
    current_balance NUMBER(12,2)  DEFAULT 0,
    status          VARCHAR2(10)  DEFAULT 'ACTIVE'
                                       CONSTRAINT ck_account_status CHECK (status IN ('ACTIVE','FROZEN','CLOSED')),
    opened_on       DATE          DEFAULT SYSDATE
);

PROMPT === STEP 4 : Create TRANSACTION table (transaction history) ===
CREATE TABLE transaction (
    txn_id        NUMBER(10)   CONSTRAINT pk_transaction       PRIMARY KEY,
    account_no    NUMBER(12)   CONSTRAINT fk_transaction_account REFERENCES account(account_no),
    txn_date      TIMESTAMP    DEFAULT SYSTIMESTAMP,
    txn_type      VARCHAR2(10) CONSTRAINT ck_txn_type          CHECK (txn_type IN ('DEPOSIT','WITHDRAWAL')),
    amount        NUMBER(12,2) CONSTRAINT ck_txn_amount        CHECK (amount > 0),
    balance_after NUMBER(12,2),
    description   VARCHAR2(100)
);

PROMPT === STEP 5 : Create indexes and V_ACCOUNT_SUMMARY view ===
CREATE INDEX idx_txn_account ON transaction (account_no);
CREATE INDEX idx_txn_date    ON transaction (txn_date);
CREATE OR REPLACE VIEW v_account_summary AS
SELECT a.account_no,
       c.first_name || ' ' || c.last_name AS customer_name,
       a.account_type,
       a.opening_balance,
       a.current_balance,
       a.status,
       a.opened_on
FROM   account a, customer c
WHERE  a.customer_id = c.customer_id;

PROMPT === Database schema created successfully ===
