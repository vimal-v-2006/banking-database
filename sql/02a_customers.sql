-- CUSTOMER REGISTRATION
SET ECHO OFF
SET DEFINE OFF
SET FEEDBACK ON
SET PAGESIZE 100 LINESIZE 170
COL first_name  FORMAT A10
COL last_name   FORMAT A10
COL email       FORMAT A22
COL phone       FORMAT A12
COL dob         FORMAT A12
COL addr        FORMAT A22
COL city        FORMAT A10
COL created_on  FORMAT A12

PROMPT === REGISTERING CUSTOMER RECORDS ===
PROMPT SQL> INSERT INTO customer VALUES (1, 'Arun', 'Kumar', 'arun.kumar@gmail.com', '9843012345', TO_DATE('12-APR-1988'
PROMPT        'DD-MON-YYYY'), '12, Hill Road', 'Kotagiri', SYSDATE);
INSERT INTO customer VALUES (1, 'Arun', 'Kumar', 'arun.kumar@gmail.com', '9843012345', TO_DATE('12-APR-1988','DD-MON-YYYY'), '12, Hill Road', 'Kotagiri', SYSDATE);
PROMPT SQL> INSERT INTO customer VALUES (2, 'Priya', 'Lakshmi', 'priya.l@gmail.com', '9791122334', TO_DATE('25-AUG-1992'
PROMPT        'DD-MON-YYYY'), '45, Town Panchayat Rd', 'Coimbatore', SYSDATE);
INSERT INTO customer VALUES (2, 'Priya', 'Lakshmi', 'priya.l@gmail.com', '9791122334', TO_DATE('25-AUG-1992','DD-MON-YYYY'), '45, Town Panchayat Rd', 'Coimbatore', SYSDATE);
PROMPT SQL> INSERT INTO customer VALUES (3, 'Mohammed', 'Rasheed', 'rasheed.m@yahoo.com', '9442233445', TO_DATE('30-JAN-1990'
PROMPT        'DD-MON-YYYY'), '8, Bus Stand Road', 'Kotagiri', SYSDATE);
INSERT INTO customer VALUES (3, 'Mohammed', 'Rasheed', 'rasheed.m@yahoo.com', '9442233445', TO_DATE('30-JAN-1990','DD-MON-YYYY'), '8, Bus Stand Road', 'Kotagiri', SYSDATE);
PROMPT SQL> INSERT INTO customer VALUES (4, 'Kavya', 'S', 'kavya.s@outlook.com', '9003344556', TO_DATE('02-NOV-1995'
PROMPT        'DD-MON-YYYY'), '23, Ooty Road', 'Ooty', SYSDATE);
INSERT INTO customer VALUES (4, 'Kavya', 'S', 'kavya.s@outlook.com', '9003344556', TO_DATE('02-NOV-1995','DD-MON-YYYY'), '23, Ooty Road', 'Ooty', SYSDATE);
PROMPT SQL> INSERT INTO customer VALUES (5, 'Suresh', 'Babu', 'suresh.b@gmail.com', '9864455667', TO_DATE('18-JUN-1985'
PROMPT        'DD-MON-YYYY'), '67, Main Street', 'Pollachi', SYSDATE);
INSERT INTO customer VALUES (5, 'Suresh', 'Babu', 'suresh.b@gmail.com', '9864455667', TO_DATE('18-JUN-1985','DD-MON-YYYY'), '67, Main Street', 'Pollachi', SYSDATE);
PROMPT SQL> INSERT INTO customer VALUES (6, 'Divya', 'R', 'divya.r@gmail.com', '9952266778', TO_DATE('09-MAR-1998'
PROMPT        'DD-MON-YYYY'), '5, Lake View Layout', 'Kotagiri', SYSDATE);
INSERT INTO customer VALUES (6, 'Divya', 'R', 'divya.r@gmail.com', '9952266778', TO_DATE('09-MAR-1998','DD-MON-YYYY'), '5, Lake View Layout', 'Kotagiri', SYSDATE);
PROMPT SQL> COMMIT;
COMMIT;

PROMPT === DISPLAY CUSTOMER INFORMATION ===
PROMPT SQL> SELECT customer_id AS id,
PROMPT        first_name,
PROMPT        last_name,
PROMPT        email,
PROMPT        phone,
PROMPT        TO_CHAR(date_of_birth,'DD-MON-YYYY') AS dob,
PROMPT        address AS addr,
PROMPT        city,
PROMPT        TO_CHAR(created_on,'DD-MON-YYYY')   AS created_on
PROMPT        FROM   customer
PROMPT        ORDER BY customer_id;
SELECT customer_id AS id,
       first_name,
       last_name,
       email,
       phone,
       TO_CHAR(date_of_birth,'DD-MON-YYYY') AS dob,
       address AS addr,
       city,
       TO_CHAR(created_on,'DD-MON-YYYY')   AS created_on
FROM   customer
ORDER BY customer_id;
