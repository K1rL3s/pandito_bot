ALTER DATABASE bot SET TIMEZONE TO 'Europe/Moscow';

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tg BIGINT UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    stage INTEGER DEFAULT 0,
    can_pay BOOLEAN NOT NULL DEFAULT FALSE,
    can_clear_purchases BOOLEAN NOT NULL DEFAULT FALSE,
    balance INT NOT NULL DEFAULT 0 CHECK (balance >= 0),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(63) NOT NULL UNIQUE,
    description TEXT,
    price INT NOT NULL CHECK (price >= 0),
    stock INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    quantity INT NOT NULL CHECK (quantity >= 0),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id)  ON DELETE CASCADE,
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION transfer_funds(
    sender_id INT,
    receiver_id INT,
    amount INT
) RETURNS INT AS $$
DECLARE
    updated_balance INT;
BEGIN
    IF (SELECT balance FROM users WHERE id = sender_id) < amount THEN
        RAISE EXCEPTION 'Insufficient balance';
    END IF;

    UPDATE users
    SET balance = balance - amount
    WHERE id = sender_id
    RETURNING balance INTO updated_balance;

    UPDATE users
    SET balance = balance + amount
    WHERE id = receiver_id;

    INSERT INTO logs (user_id, description) 
    VALUES (sender_id, 'Transferred ' || amount || ' to user ' || receiver_id),
    (receiver_id, 'Received ' || amount || ' from user ' || sender_id);

    RETURN updated_balance;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION buy_product(
    user_id INT,
    product_id INT,
    quantity INT
) RETURNS INT AS $$
DECLARE
    product_price INT;
    total_cost INT;
    product_stock INT;
    updated_balance INT;
BEGIN
    SELECT price, stock INTO product_price, product_stock 
    FROM products 
    WHERE id = product_id;
    
    IF product_stock < quantity THEN
        RAISE EXCEPTION 'Not enough stock for this product';
    END IF;

    total_cost := product_price * quantity;

    IF (SELECT balance FROM users WHERE id = user_id) < total_cost THEN
        RAISE EXCEPTION 'Insufficient balance';
    END IF;

    UPDATE users 
    SET balance = balance - total_cost 
    WHERE id = user_id
    RETURNING balance INTO updated_balance;

    UPDATE products 
    SET stock = stock - quantity 
    WHERE id = product_id;

    INSERT INTO purchases (user_id, product_id, quantity)
    VALUES (user_id, product_id, quantity);

    INSERT INTO logs (user_id, description)
    VALUES (user_id, 'Bought ' || quantity || ' of ' || (SELECT name FROM products WHERE id = product_id) || ' for ' || total_cost || ' units.');

    RETURN updated_balance;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_timestamp
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_product_timestamp
BEFORE UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_purchase_timestamp
BEFORE UPDATE ON purchases
FOR EACH ROW EXECUTE FUNCTION update_timestamp();