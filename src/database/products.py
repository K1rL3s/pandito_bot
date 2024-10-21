from asyncpg import Pool


class ProductDB:
    def __init__(self, db_pool: Pool) -> None:
        self.db_pool = db_pool

    async def create_product(self, name: str, description: str, price: int, stock: int):
        async with self.db_pool.acquire() as conn:
            sql = """
            INSERT INTO products (name, description, price, stock)
            VALUES ($1, $2, $3, $4)
            RETURNING id;
            """
            return await conn.fetchval(sql, name, description, price, stock)

    async def get_product(self, product_id: int):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT * FROM products WHERE id = $1;"
            return await conn.fetchrow(sql, product_id)

    async def update_product_stock(self, product_id: int, new_stock: int):
        async with self.db_pool.acquire() as conn:
            sql = """
            UPDATE products 
            SET stock = $1, updated_at = NOW() 
            WHERE id = $2
            RETURNING stock;
            """
            return await conn.fetchval(sql, new_stock, product_id)

    async def change_product_price(self, product_id: int, new_price: int):
        async with self.db_pool.acquire() as conn:
            sql = """
            UPDATE products 
            SET price = $1, updated_at = NOW()
            WHERE id = $2
            RETURNING price;
            """
            return await conn.fetchval(sql, new_price, product_id)

    async def get_available_products(self):
        async with self.db_pool.acquire() as conn:
            sql = """
            SELECT * FROM products 
            WHERE stock > 0;
            """
            return await conn.fetch(sql)

    async def buy_product(self, user_id: int, product_id: int, quantity: int):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT buy_product($1, $2, $3);"
            return await conn.fetchval(sql, user_id, product_id, quantity)

    async def delete_product(self, product_id: int):
        async with self.db_pool.acquire() as conn:
            sql = "DELETE FROM products WHERE id = $1;"
            await conn.execute(sql, product_id)

    async def get_all_products(self):
        async with self.db_pool.acquire() as conn:
            sql = "SELECT * FROM products;"
            return await conn.fetch(sql)
