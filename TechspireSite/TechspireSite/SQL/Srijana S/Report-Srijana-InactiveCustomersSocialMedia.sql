--Srijana Shrestha
--Inactive-Cancel Customer with Social media details
--The client can use this report to view customers that have declared themselves "inactive" within the loyalty system, specifically customers that have social media. This report is beneficial for the client because the client may want to reach out to her inactive customers to resume business relations. Particularly those that use social media, it is a priority to reach out to those customers first because they might leave negative reviews.
--Displays only the customers that have been categorized as "inactive-cancel" with social media handle
--Full Name,Email,Social Media,Customer Handle, City,Customer Status,Status Desc
--,,,,,,
SELECT Full_Name, Email, Social_Media, Customer_Handle, City, 
status_name AS "Customer_Status", status_desc AS "Status_Desc" FROM (

SELECT Customer.customer_status_id AS id,
Customer.email_address AS Email,
Customer.first_name + ' ' + "Customer".last_name AS "Full_Name",
CustomerSocialMedia.social_media_code AS "Customer_Handle",
SocialMediaType.social_media_name AS "Social_Media",
city AS "City"
FROM "SocialMediaType" 
INNER JOIN "CustomerSocialMedia" ON "SocialMediaType".id = "CustomerSocialMedia".social_media_type_id
INNER JOIN "Customer" ON "CustomerSocialMedia".customer_id = "Customer".id
INNER JOIN "location" ON "Customer".location_id = "location".id
INNER JOIN "StateProvince" ON "StateProvince".id = "Location".state_id
WHERE "StateProvince".state_name = 'Texas'
and "SocialMediaType".id IN (1,3)) A

INNER JOIN "CustomerStatus" ON A.id = "CustomerStatus".id
WHERE "CustomerStatus".id = 3
ORDER BY Full_Name;