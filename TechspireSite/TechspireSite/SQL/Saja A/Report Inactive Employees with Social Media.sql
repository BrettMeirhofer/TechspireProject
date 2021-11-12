--Saja Alyasin
--Inactive Employees with a Social Media
--The client can utilize this report to determine which employee are currently inactive in order to remove them from being contacted or updated with future business practices. Most employees when hired share their social media information with the business in order to receive additional updates about the business and as another means of contact, after those employees leave the business, they must be removed from the store’s social media account since they are no longer actively working there anymore.
--This report displays the inactive employees with their social media information, it is sorted in ascending order by employee first name.
--Row Number, Employee First Name, Employee Last Name, Social Media Type, User Handle
--,,,,,

SELECT ROW_NUMBER()
OVER(ORDER BY Employee.first_name ASC) AS Row_Num,
Employee.first_name AS "First Name",
Employee.last_name AS "Last Name",
SocialMediaType.social_media_name AS "Social Media Type",
EmployeeSocialMedia.social_media_code AS "User Handle"
FROM EmployeeSocialMedia
INNER JOIN Employee ON EmployeeSocialMedia.employee_id = Employee.id
INNER JOIN SocialMediaType ON SocialMediaType.id = EmployeeSocialMedia.social_media_type_id
INNER JOIN EmployeeStatus ON EmployeeStatus.id = Employee.employee_status_id
WHERE "EmployeeStatus".is_active = 0
