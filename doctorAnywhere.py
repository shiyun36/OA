import pandas as pd
import pandasql as psql
import sqlite3

Customers = {
    'id': [1, 2, 3, 4, 5, 6],
    'name': ['John', 'Jane', 'Bob', 'Mary', 'Scott','Peter'],
    'age': [25, 35, 45, 30, 28, 23]
}
Orders = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    'customer_id': [1, 2, 1, 3, 4, 2, 1, 3, 4, 2, 1, 3, 6],
    'order_date': ['2022-01-01', '2022-01-02','2022-01-03','2022-01-04','2022-02-01','2022-02-021','2022-02-03','2022-02-04','2022-03-01','2022-03-02','2022-03-03','2022-03-04','2022-03-05'],
    'amount': [100, 200, 50, 300, 150, 100, 75, 200, 250, 50, 125, 175, 60]
}
Products = {
    'id': [1, 2, 3, 4],
    'name': ['Vitamin', 'Gadget', 'Medicine', 'Baby Care'],
    'price': [10, 20, 15, 5]
}
Order_Items = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    'order_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    'product_id': [1, 1, 2, 3, 4, 2, 4, 3, 1, 2, 4, 3, 2]
}

customers = pd.DataFrame(Customers)
orders = pd.DataFrame(Orders)
products = pd.DataFrame(Products)
order_items = pd.DataFrame(Order_Items)

#1 
query1 = '''
SELECT * FROM orders;
'''
result1 = psql.sqldf(query1, locals())
#print(result1)

#2
query2 = '''
SELECT * FROM orders
WHERE order_date LIKE '2022-03%';
'''
result2 = psql.sqldf(query2, locals())
#print(result2)

#3
query3 = '''
SELECT o.id AS order_id, c.name AS customer_name, o.order_date, o.amount
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.id;
'''

result3 = psql.sqldf(query3, locals())
#print(result3)

#4
query4 = '''
SELECT o.id AS order_id, 
       c.name AS customer_name, 
       p.name AS product_name, 
       o.order_date, 
       o.amount
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id;

'''
result4 = psql.sqldf(query4, locals())
#print(result4)

#5 
query5 = '''
SELECT o.id AS order_id, 
       c.name AS customer_name, 
       p.name AS product_name, 
       o.order_date, 
       o.amount
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE customer_name = 'Bob';

'''
result5 = psql.sqldf(query5, locals())
# print(result5)

#6 
query6 = '''
SELECT c.id, 
       c.name AS customer_name, 
       SUM(o.amount * p.price) AS total_spend
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
GROUP BY c.name
ORDER BY total_spend DESC 

'''
#LIMIT 2;
result6 = psql.sqldf(query6, locals())
#print(result6)

#7 
query7 = '''
SELECT c.name AS customer_name, 
       SUM(o.amount * p.price) / COUNT(DISTINCT strftime('%Y-%m', o.order_date)) AS ARPU 
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.order_date >= '2022-02-01' AND o.order_date < '2022-04-01'
GROUP BY c.name;
'''

result7 = psql.sqldf(query7, locals())
#print(result7)

query7a = '''
SELECT c.name AS customer_name, 
       (SUM(o.amount * p.price) / 2) AS ARPU 
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.order_date >= '2022-02-01' AND o.order_date < '2022-04-01'
GROUP BY c.name;
'''
result7a = psql.sqldf(query7a, locals())
#print(result7a)


#8 
query8 = '''
SELECT c.id, c.name, MIN(o.order_date) AS order_date
FROM customers c
LEFT JOIN orders o
ON c.id = o.customer_id
GROUP BY c.id
'''
result8 = psql.sqldf(query8, locals())
#print(result8)


#9 
query9 = '''
WITH ranked_orders AS (
    SELECT 
        o.id AS order_id,
        o.customer_id,
        o.order_date,
        LEAD(o.order_date) OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS next_order_date
    FROM orders o
)
SELECT 
    c.id AS customer_id,
    c.name AS customer_name,
    AVG(julianday(next_order_date) - julianday(order_date)) AS avg_duration_days
FROM ranked_orders ro
LEFT JOIN customers c ON ro.customer_id = c.id
WHERE next_order_date IS NOT NULL  
GROUP BY c.name
HAVING COUNT(*) > 1 ;

'''
## Note: DATEDIFF only exists in MySQL, 
result9 = psql.sqldf(query9, locals())
print(result9)
