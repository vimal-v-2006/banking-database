-- =====================================================================
--  BANKING DATABASE - SAMPLE CUSTOMER & ACCOUNT DATA
-- =====================================================================
SET ECHO OFF
SET FEEDBACK ON
SET PAGESIZE 100 LINESIZE 170

PROMPT Inserting customer records...
INSERT INTO customer VALUES (1, 'Arun',     'Kumar',    'arun.kumar@gmail.com',  '9843012345', TO_DATE('12-APR-1988','DD-MON-YYYY'), '12, Hill Road',        'Kotagiri',   SYSDATE);
INSERT INTO customer VALUES (2, 'Priya',    'Lakshmi',  'priya.l@gmail.com',     '9791122334', TO_DATE('25-AUG-1992','DD-MON-YYYY'), '45, Town Panchayat Rd', 'Coimbatore', SYSDATE);
INSERT INTO customer VALUES (3, 'Mohammed', 'Rasheed',  'rasheed.m@yahoo.com',   '9442233445', TO_DATE('30-JAN-1990','DD-MON-YYYY'), '8, Bus Stand Road',    'Kotagiri',   SYSDATE);
INSERT INTO customer VALUES (4, 'Kavya',    'S',        'kavya.s@outlook.com',   '9003344556', TO_DATE('02-NOV-1995','DD-MON-YYYY'), '23, Ooty Road',        'Ooty',       SYSDATE);
INSERT INTO customer VALUES (5, 'Suresh',   'Babu',     'suresh.b@gmail.com',    '9864455667', TO_DATE('18-JUN-1985','DD-MON-YYYY'), '67, Main Street',      'Pollachi',   SYSDATE);
INSERT INTO customer VALUES (6, 'Divya',    'R',        'divya.r@gmail.com',     '9952266778', TO_DATE('09-MAR-1998','DD-MON-YYYY'), '5, Lake View Layout',  'Kotagiri',   SYSDATE);
COMMIT;

PROMPT Opening accounts (SAVINGS / CURRENT / FIXED)...
INSERT INTO account VALUES (100010000001, 1, 'SAVINGS', 10000,  10000,  'ACTIVE', SYSDATE);
INSERT INTO account VALUES (100010000002, 1, 'CURRENT', 25000,  25000,  'ACTIVE', SYSDATE);
INSERT INTO account VALUES (100010000003, 2, 'SAVINGS', 15000,  15000,  'ACTIVE', SYSDATE);
INSERT INTO account VALUES (100010000004, 3, 'FIXED',   100000, 100000, 'ACTIVE', SYSDATE);
INSERT INTO account VALUES (100010000005, 4, 'SAVINGS',  8000,   8000,   'ACTIVE', SYSDATE);
INSERT INTO account VALUES (100010000006, 5, 'CURRENT', 50000,  50000,  'ACTIVE', SYSDATE);
INSERT INTO account VALUES (100010000007, 6, 'SAVINGS',  5000,   5000,   'ACTIVE', SYSDATE);
COMMIT;
