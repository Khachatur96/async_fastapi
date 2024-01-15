SELECT orders_1.id          AS orders_1_id,
       products.name        AS products_name,
       products.price       AS products_price,
       products.description AS products_description,
       products.id          AS products_id
FROM orders AS orders_1
         JOIN order_product_association AS order_product_association_1
              ON orders_1.id = order_product_association_1.order_id
         JOIN products ON products.id = order_product_association_1.product_id
WHERE orders_1.id IN (1, 2);
