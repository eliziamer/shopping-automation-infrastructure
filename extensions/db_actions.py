import sqlite3

from utils.common_ops import load_config


CONFIG = load_config() 

class DBActions:
    def __init__(self, data_base):
        self.data_base = data_base

    def close_db(self):
        self.data_base.close()


    def get_product_price(self, product_name):
        query = "SELECT price FROM products WHERE product_name = ?"
        cursor = self.data_base.cursor()
        cursor.execute(query, (product_name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_random_products(self, count=3):
        query = f"SELECT product_name FROM products ORDER BY RANDOM() LIMIT {count}"
        cursor = self.data_base.cursor()
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]


    @staticmethod
    def get_all_product_names():
        with sqlite3.connect(CONFIG["DB_PATH"]) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT product_name FROM products")
            return [row[0] for row in cursor.fetchall()]