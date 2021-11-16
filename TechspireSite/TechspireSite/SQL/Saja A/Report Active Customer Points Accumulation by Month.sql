-- Saja Alyasin
-- Points accumulated by an active customer by a given month
-- The client can utilize this report to determine an active customer's accumulation of points in a given month, this report can later be manipulated to display the month and year the business owner would like to see. This report is useful for determining the customer with the most accumulated points in that given month in order for the business owner to potentially reward those active customers with special promotions, free products, loyalty points, etc.
-- This report displays the points accumulated by an active customer in a given month.
-- Row Number, First name, Last name, Email, Points Accumulated, Category name
--,,,,right,


SELECT ROW_NUMBER()
OVER(ORDER BY Points."Points Accumulated" DESC) AS Row_Num,
Customer.first_name AS "First Name",
Customer.last_name AS "Last Name",
Customer.email_address AS "Email",
Points."Points Accumulated",
CustomerCategory.category_name AS "Category"


FROM Customer
INNER JOIN CustomerStatus ON CustomerStatus.id = Customer.customer_status_id
INNER JOIN "Order" ON Customer.id = "Order".customer_id
INNER JOIN PointLog ON PointLog.order_id = "Order".id
INNER JOIN (SELECT SUM(PointLog.points_amount) AS "Points Accumulated", PointLog.order_id
			FROM PointLog
			WHERE PointLog.points_amount > 0
			GROUP BY PointLog.order_id) 
			AS Points ON "Order".id = Points.order_id
INNER JOIN CustomerCustomerCategory ON CustomerCustomerCategory.customer_id = Customer.id
INNER JOIN CustomerCategory ON CustomerCustomerCategory.customer_category_id = CustomerCategory.id
 
WHERE DATEPART(yyyy FROM PointLog.created_date) = '2018'
AND CustomerStatus.id = '1'

GROUP BY Customer.begin_date, Customer.first_name, Customer.last_name, Points.order_id, Points."Points Accumulated", CustomerCategory.category_name, Customer.email_address
