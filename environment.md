# 测试环境配置文档

数据库名称：shop_test

业务表：用户表 user_info、商品表 goods、订单表 orders

用途：电商小程序手工测试、数据库测试练习，包含增删改查、模糊查询、分页、联表、库存扣减、超时订单处理常用测试SQL。


-- 创建电商测试库
CREATE DATABASE IF NOT EXISTS shop_test DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE shop_test;

-- 创建用户表、商品表、订单表

CREATE TABLE IF NOT EXISTS user_info (

    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    
    phone VARCHAR(11) NOT NULL UNIQUE COMMENT '手机号',
    
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    
    password VARCHAR(64) NOT NULL COMMENT '登录密码',
    
    create_time DATETIME DEFAULT NOW() COMMENT '创建时间',
    
    update_time DATETIME DEFAULT NOW() ON UPDATE NOW() COMMENT '更新时间'
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '小程序用户表';

CREATE TABLE IF NOT EXISTS goods (

    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '商品ID',
    
    goods_name VARCHAR(100) NOT NULL COMMENT '商品名称',
    
    price DECIMAL(10,2) NOT NULL COMMENT '商品单价',
    
    stock INT NOT NULL DEFAULT 0 COMMENT '库存数量',
    
    create_time DATETIME DEFAULT NOW() COMMENT '上架时间',
    
    update_time DATETIME DEFAULT NOW() ON UPDATE NOW() COMMENT '更新时间'
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '商品库存表';

CREATE TABLE IF NOT EXISTS orders (

    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '订单ID',
    
    order_no VARCHAR(32) NOT NULL UNIQUE COMMENT '订单编号',
    
    user_id INT NOT NULL COMMENT '下单用户ID',
    
    goods_id INT NOT NULL COMMENT '商品ID',
    
    buy_num INT NOT NULL DEFAULT 1 COMMENT '购买数量',
    
    total_price DECIMAL(10,2) NOT NULL COMMENT '订单总价',
    
    pay_status TINYINT NOT NULL DEFAULT 0 COMMENT '支付状态 0未支付 1已支付',
    
    create_time DATETIME DEFAULT NOW() COMMENT '下单时间',
    
    pay_time DATETIME NULL COMMENT '支付时间',
    
    FOREIGN KEY (user_id) REFERENCES user_info(id),
    
    FOREIGN KEY (goods_id) REFERENCES goods(id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '订单表';

-- 新增用户

INSERT INTO user_info(phone,username,password) VALUES('13800138000','测试用户','123456');

-- 新增商品

INSERT INTO goods(goods_name,price,stock) VALUES('夏季短袖T恤',59.90,100);

-- 新增订单

INSERT INTO orders(order_no,user_id,goods_id,buy_num,total_price,pay_status) 

VALUES('ORD20260630001',1,1,1,59.90,0);

-- 查询全部用户

SELECT * FROM user_info;

-- 查询库存大于0的商品

SELECT id,goods_name,price,stock FROM goods WHERE stock > 0;

-- 修改用户昵称

UPDATE user_info SET username = '电商测试账号' WHERE id = 1;

-- 删除测试订单（仅测试环境使用）

DELETE FROM orders WHERE id = 1;

-- 查询手机号以138开头的用户

SELECT * FROM user_info WHERE phone LIKE '138%';

-- 查询手机号尾号0000的用户

SELECT * FROM user_info WHERE phone LIKE '%0000';

-- 查询手机号包含13800的用户

SELECT * FROM user_info WHERE phone LIKE '%13800%';

-- 第1页，每页10条（offset从0开始）

SELECT * FROM orders ORDER BY create_time DESC LIMIT 0,10;

-- 第2页，每页10条

SELECT * FROM orders ORDER BY create_time DESC LIMIT 10,10;

-- 通用分页：第n页，每页pageSize条 LIMIT (n-1)*pageSize , pageSize

-- 查询所有用户及对应订单，无订单也展示用户

SELECT 

    u.id user_id,
    
    u.phone,
    
    u.username,
    
    o.order_no,
    
    o.total_price,
    
    o.pay_status,
    
    o.create_time order_time

FROM user_info u

LEFT JOIN orders o ON u.id = o.user_id

ORDER BY u.id DESC;

-- 下单扣库存：商品id=1，购买数量1

START TRANSACTION; -- 开启事务

-- 1. 校验库存并扣减，防止超卖

UPDATE goods 

SET stock = stock - 1 

WHERE id = 1 AND stock >= 1;

-- 2. 判断受影响行数，库存不足则回滚

IF ROW_COUNT() = 0 THEN
 
    ROLLBACK;
    
    SELECT '库存不足，下单失败' AS result;

ELSE

    -- 3. 库存充足，插入订单
    
    INSERT INTO orders(order_no,user_id,goods_id,buy_num,total_price,pay_status)
    
    VALUES('ORD20260630002',1,1,1,59.90,0);
    
    COMMIT; -- 提交事务
    
    SELECT '下单成功，库存已扣减' AS result;

END IF;

-- 需求：找出创建时间超过15分钟、支付状态=0未支付的订单，用于自动取消

SELECT 

    id,order_no,user_id,goods_id,total_price,create_time

FROM orders

WHERE pay_status = 0 

AND create_time < DATE_SUB(NOW(),INTERVAL 15 MINUTE);

-- 拓展：批量取消超时未支付订单，同时回补商品库存

START TRANSACTION;

-- 1. 查询超时未支付订单

CREATE TEMPORARY TABLE timeout_order AS 

SELECT goods_id,buy_num FROM orders 

WHERE pay_status=0 AND create_time < DATE_SUB(NOW(),INTERVAL 15 MINUTE);

-- 2. 库存回补

UPDATE goods g JOIN timeout_order t ON g.id = t.goods_id 

SET g.stock = g.stock + t.buy_num;

-- 3. 更新订单状态为已取消

UPDATE orders 

SET pay_status = 2 -- 2=已取消超时订单

WHERE pay_status=0 AND create_time < DATE_SUB(NOW(),INTERVAL 15 MINUTE);

COMMIT;

DROP TEMPORARY TABLE IF EXISTS timeout_order;
