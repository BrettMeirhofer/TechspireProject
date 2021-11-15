--Torrey Brett
--Customer Total Dollar Spent and Point Amount Available
--This report will allow the client to view the loyalty customer and their dollar spending totals to show which customers have spent the most money at the bakeries. Included are the customer points used and total points available. This, used in conjunction with the employee name can help determine which employee took that order and the client can ask the employee if they are offering the opportunity for the customer to use their points.
--Included in this report is the customer first and last name, their spending totals, their points used,  and the employee name and information that took the customer order. 
--Row Number,First Name,Last Name,Spending Total,Point Total, Employee First Name, Employee Last Name
--,,,right,right,,

SELECT ROW_NUMBER() OVER(ORDER BY Points.total desc) AS Num_Row,
Customer.first_name AS First_Name, Customer.last_name AS Last_Name, (concat('$', cast(Totals.total  AS decimal(18,2)))) AS Customer_Spending_Total, Points.total AS Customer_Total_Points, Employee.first_name AS Employee_FName, Employee.last_name AS Employee_LName
FROM (SELECT
SUM ("ORDER".final_total) AS total, "Order".customer_id
FROM "ORDER"
GROUP BY "Order".customer_id)
AS Totals
INNER JOIN Customer 
ON Customer.id = Totals.customer_id
INNER JOIN PointLog 
ON PointLog.id = Customer.id
INNER JOIN Employee
ON Employee.id = PointLog.employee_id
INNER JOIN (SELECT
SUM (PointLog.points_amount) AS total, PointLog.customer_id
FROM PointLog
GROUP BY PointLog.customer_id)
AS Points 
ON Points.customer_id = Totals.customer_id
ORDER BY Points.total desc
