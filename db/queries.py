# queries.py

CREATE_TABLE_registered = """
    CREATE TABLE IF NOT EXISTS registered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    age TEXT,
    gender TEXT, 
    email TEXT,
    photo TEXT
    )
"""

INSERT_registered_QUERY = """
    INSERT INTO registered (fullname, age, gender, email, photo)
    VALUES (?, ?, ?, ?, ?)
"""

CREATE_TABLE_store = """
    CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    size TEXT,
    price TEXT, 
    product_id TEXT,
    photo TEXT
    )
"""


CREATE_TABLE_store_details = """
    CREATE TABLE IF NOT EXISTS store_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    product_id TEXT,
    info_product TEXT
    )
"""

INSERT_store_QUERY = """
    INSERT INTO store (name_product, size, price, product_id, photo)
    VALUES (?, ?, ?, ?, ?)
"""


INSERT_store_details_QUERY = """
    INSERT INTO store_details (category, product_id, info_product)
    VALUES (?, ?, ?)
"""