# main_db.py
import sqlite3
from db import queries


# db = sqlite3.connect('db/registered.sqlite3')
db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()


async def DataBase_create():
    if db:
        print('База данных подключена!')
    cursor.execute(queries.CREATE_TABLE_registered)
    cursor.execute(queries.CREATE_TABLE_store)
    cursor.execute(queries.CREATE_TABLE_store_details)


async def sql_insert_registered(fullname, age, gender, email, photo):
    cursor.execute(queries.INSERT_registered_QUERY, (
        fullname, age, gender, email, photo
    ))
    db.commit()

async def sql_insert_store(name_product, size, price, product_id, photo):
    cursor.execute(queries.INSERT_store_QUERY, (
        name_product, size, price, product_id, photo
    ))
    db.commit()

async def sql_insert_store_detail(category, product_id, info_product):
    cursor.execute(queries.INSERT_store_details_QUERY, (
        category, product_id, info_product
    ))
    db.commit()



# CRUD - Read
# =====================================================

# Основное подключение к базе (Для CRUD)
def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * from store s
    INNER JOIN store_details  sd ON s.product_id = sd.product_id
    """).fetchall()
    conn.close()
    return products


# CRUD - Delete
# =====================================================

def delete_product(product_id):
    conn = get_db_connection()

    conn.execute('DELETE FROM store WHERE product_id = ?', (product_id,))

    conn.commit()
    conn.close()



# CRUD - Update
# =====================================================
def update_product_field(product_id, field_name, new_valeu):
    store_table = ["name_product", "size", "price", "photo"]
    store_detail_table = ["info_product", "category"]
    conn = get_db_connection()
    try:
        if field_name in store_table:
            query = f'UPDATE store SET {field_name} = ? WHERE product_id = ?'
        elif field_name in store_detail_table:
            query = f'UPDATE store_detail SET {field_name} = ? WHERE product_id = ?'
        else:
            raise ValueError(f'Нет такого поля {field_name}')

        conn.execute(query, (new_valeu, product_id))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f'Ошибка - {e}')
    finally:
        conn.close()