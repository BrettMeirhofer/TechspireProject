CREATE TABLE product (
					product_id INT PRIMARY KEY IDENTITY(1,1),
					product_name VARCHAR(40) NOT NULL,
					product_description VARCHAR (200) NOT NULL,
					product_price DECIMAL (10,2) CHECK (product_price >= 0) NOT NULL,
					product_type_id INT NOT NULL,
					store_id INT NOT NULL,
					product_status_id INT NOT NULL,
					ban_reason_id INT );

CREATE TABLE product_type(
					product_type_id INT PRIMARY KEY IDENTITY(1,1),
					product_type_name VARCHAR(40) NOT NULL,
					product_type_description VARCHAR(200)
					);


CREATE TABLE product_status (
					product_status_id INT PRIMARY KEY IDENTITY(100,1),
					product_status_name varchar (50) NOT NULL,
					product_status_desc varchar (50)
					);

CREATE TABLE store(
					store_id INT PRIMARY KEY IDENTITY(1,1),
					store_name VARCHAR(50) NOT NULL,
					store_status_id INT NOT NULL,
					store_address1 VARCHAR(50) NOT NULL,
					store_address2 VARCHAR(50),
					store_country_id CHAR(3)NOT NULL,
					store_city VARCHAR(50) NOT NULL,
					store_zip CHAR(5) NOT NULL,
					store_state_id CHAR(2) NOT NULL,
					store_phone CHAR(10) NOT NULL,
					store_email_address VARCHAR(100) NOT NULL,
					store_social_media_code INT,
					store_launch_date date,
					store_close_date date);
