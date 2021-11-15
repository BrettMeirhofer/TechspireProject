--Torrey Brett
--Product Name and Total Sales Report
--This report will give the client insight into the total sales of a product. She can find this data useful to view which products have sold the most dollar amount overtime. The client will utilize this report during tax season or for general record keeping purposes. The reason for this is to help with financial preparations or to help the client make informed decisions about which products she offers that has the highest total sales in monetary value.
--Included in this report is the product name and the sum sales of that product.
--Row Number, Product Name, Sum Sales, Item Price, Number of Items Sold 
--,,right,right,right

SELECT ROW_NUMBER() OVER(ORDER BY Sum(Orderline.total_price) desc) AS Num_Row,
MAX(Product.product_name) AS Product_Name, (concat('$', cast(Sum(OrderLine.total_price) AS decimal(18,2)))) AS Sum_Sales, 
(concat('$', cast(OrderLine.total_price AS decimal(18,2)))) as Item_Price, count(OrderLine.total_price) as Number_Items_Sold
From OrderLine
INNER JOIN "Order"
ON OrderLine.order_id = "Order".ID
INNER JOIN Product
ON OrderLine.product_id = Product.id
INNER JOIN ProductStatus
ON Product.product_status_id = productStatus.id
Group By Orderline.total_price
