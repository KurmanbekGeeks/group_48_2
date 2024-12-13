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

