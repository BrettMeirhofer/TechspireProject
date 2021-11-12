-- Saja Alyasin
-- Points accumulated by an active customer by a given year
-- This report displays the points accumulated by an active customer in a given year.
-- The client can utilize this report to determine an active customer’s accumulation of points in a given year, this report can later be manipulated to display year the business owner would like to see. This report is useful for determining the customer with the most accumulated points in that given year in order for the business owner to potentially reward those active customers with special promotions, free products, loyalty points, etc.
-- Row Number, First name, Last name, Points Accumulated, Category name
--,,,,,


SELECT ROW_NUMBER() 
OVER(ORDER BY Points."Points Accumulated" DESC) AS Row_Num, 
Customer.first_name AS "Customer First Name", 
Customer.last_name AS "Customer Last Name",
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

GROUP BY Customer.first_name, Customer.last_name, Points.order_id, Points."Points Accumulated", CustomerCategory.category_name
ORDER BY MIN(Customer.created_date);
