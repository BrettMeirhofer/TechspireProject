--Srijana Shrestha
--Active Customer with a specific Birth Month
--The client can use this report to view customers that all have the same birth month from all the stores, depending on the client's selected month. This report is beneficial for the client because the client can view customers born in the current month or next month and anticipate a rise in reward usages. Furthermore, the client will be able to view all the customer emails to send them marketing emails for their birthday.
--Displays only the customers that were born in the selected month and active. It is ordered by the customer's birthdate. Information about the customer's address is included(if available).
--Full name,Email,Birth Date,Store Name,Customer Status
--,,,,
DECLARE @customer_birthmonth INT
SELECT @customer_birthmonth = 8

SELECT "Full_Name", "Email", "Birth_Date", "Store_Name", "Customer_status"
FROM
(SELECT DISTINCT "Customer".id AS "Customer_Id",
"Customer".first_name + ' ' + "Customer".last_name AS "Full_Name",
"Customer".email_address AS "Email",
"Customer".birthdate AS "Birth_Date",
"Store".store_name AS "Store_Name" ,
"CustomerStatus".status_name AS "Customer_status"
FROM "Store" INNER JOIN "Order" ON "Store".id = "Order".store_id
INNER JOIN "Customer" ON "Order".customer_id = "Customer".id
INNER JOIN "CustomerStatus" ON "Customer".customer_status_id = "CustomerStatus".id
WHERE "CustomerStatus".id = 1 and
month("Customer".birthdate) = @customer_birthmonth) AS Cust
ORDER BY "Cust".Birth_Date
