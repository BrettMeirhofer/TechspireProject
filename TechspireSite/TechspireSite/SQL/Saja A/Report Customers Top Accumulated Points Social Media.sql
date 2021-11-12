-- Saja Alyasin
-- Customers with Most Points Social Media
-- The client can utilize this report to determine the customers with the most points and the social media handle associated with them to potentially give incentives, such as loyalty points, to those customers. One of the most popular marketing tools used today, with the help of social media, is influencer sponsorships where customers with a good following amount can post advertisements, reviews, and commentary on the social media about the product for an exchange of points since they are already active customers with a loyalty point earning.
-- This report displays the customers with the most accumulated points and the social media handle associated with that customer.
-- Row Number, Customer First Name, Customer Last Name, Points Accumulated, Social Media Type, Customer Social Media Name
-- ,,,,,

SELECT ROW_NUMBER() 
OVER(ORDER BY Points."Points Accumulated" ASC) AS Row_Num, 
Customer.first_name AS "First Name",
Customer.last_name AS "Last Name",
Points."Points Accumulated",
SocialMediaType.social_media_name AS "Social Media Type", 
CustomerSocialMedia.social_media_code AS "Customer Social Media Handle"


FROM Customer
INNER JOIN CustomerStatus ON CustomerStatus.id = Customer.customer_status_id
INNER JOIN "Order" ON Customer.id = "Order".customer_id
INNER JOIN (SELECT SUM(PointLog.points_amount) AS "Points Accumulated", PointLog.order_id
			FROM PointLog
			WHERE PointLog.points_amount > 0
			GROUP BY PointLog.order_id) 
			AS Points ON "Order".id = Points.order_id
INNER JOIN CustomerSocialMedia ON Customer.id = CustomerSocialMedia.customer_id
INNER JOIN SocialMediaType ON CustomerSocialMedia.social_media_type_id = SocialMediaType.id;
