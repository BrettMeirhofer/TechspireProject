--Alanna Gilcrease
--Mailing List
--The client can utilize this report to mail seasonal promotions, coupons, or vouchers.
--The report will display the clients customers email and mailing address from a specific store.
--Customer_ID, Full_Name, Email, Address, City, Zip_Code, Store_Name
--,,,,,,,

DECLARE @store_name INT = 1
SELECT Full_Name, Email, Address, City, Zip_Code, Store_Name From (

SELECT Distinct Customer.id AS 'Customer_ID',
first_name + ' ' + last_name AS 'Full_Name', 
Customer.email_address as 'Email' ,
Location.address as Address, Location.city AS 'City', 
Location.zip_code AS 'Zip_Code',
Store.store_name AS 'Store_Name'

FROM Customer

INNER JOIN "Order" 
ON Customer.id = "Order".customer_id

INNER JOIN Store 
ON "Order".store_id = Store.id

INNER JOIN  "Location" 
ON  Customer.location_id = Location.id

WHERE Store.id = @store_name) AS Cust
ORDER BY Full_Name


