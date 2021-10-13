CREATE TABLE Employee(
id int NOT NULL PRIMARY KEY IDENTITY(1,1),
first_name nvarchar(40) NOT NULL,
last_name nvarchar(40) NOT NULL,
email_address nvarchar(254) NOT NULL,
phone_number nvarchar(14) NOT NULL,
comments nvarchar(max),
birthdate date NOT NULL
begin_date date NOT NULL,
end_date date,
);

CREATE TABLE EmployeeJob(
id int NOT NULL PRIMARY KEY IDENTITY(1,1),
assign_date date NOT NULL
);

CREATE TABLE Job(
id int NOT NULL PRIMARY KEY IDENTITY(1,1),
job_name nvarchar(40) NOT NULL,
job_desc nvarchar(200),
);

CREATE TABLE Location(
id int NOT NULL PRIMARY KEY IDENTITY(1,1),
zip_code nvarchar(10) NOT NULL,
city nvarchar(35) NOT NULL,
address nvarchar(100) NOT NULL,
);

CREATE TABLE PointReasonType(
id int NOT NULL PRIMARY KEY IDENTITY(1,1),
reason_name varchar(40) NOT NULL,
reason_desc varchar(200) NOT NULL
);