--Alanna Gilcrease
--Cookies Sold at Houston Hot Breads
--The client can utilize this report to update the cookie recipes dependent on season.
--The purpose of the report is to list all cookies at Houston Hot Breads.
--Product ID, Product, Product Status, Price, Product Type, Store
--,,,right,,

SELECT ROW_NUMBER () OVER(ORDER BY Product.product_name) AS 'Row',
Product.product_name AS 'Product',
ProductStatus.status_name AS 'Product Status',
CONCAT('$', CAST (Product.product_price as decimal(18,2))) AS 'Price',
ProductType.product_type_name AS 'Product Type',
Store.store_name AS 'Store'
FROM Product
INNER JOIN StoreProduct
ON StoreProduct.product_id = Product.id
INNER JOIN Store
ON Store.id = StoreProduct.store_id
INNER JOIN ProductStatus
ON ProductStatus.id = Product.product_status_id
INNER JOIN ProductType
ON ProductType.id = Product.product_type_id
WHERE Store.id = 1 AND ProductType.id = 7
