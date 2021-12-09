import sqlite3

conn = sqlite3.connect("mydatabase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()


class Database(object):
    def __init__(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS users
                          (id text PRIMARY KEY, state text, pizza_size text,
                           payment_method text)
                       """)
        conn.commit()

    def add_user(self, person_id, state):
        cursor.execute("""
                INSERT INTO users (id, state, pizza_size, payment_method) VALUES ({},{},{},{})
                """.format(person_id, state, '', ''))
        conn.commit()

    def update_info(self, person_id, newState, pizza_size, payment_method):
        cursor.execute("""
        UPDATE users SET state = {}, pizza_size = {}, payment_method = {}  WHERE id = {}
        """.format(newState, pizza_size, payment_method, person_id))
        conn.commit()

    def has_user(self, person_id):
        info = cursor.execute('SELECT * FROM users WHERE id={}'.format(person_id))
        if info.fetchone() is None:
            return False
        else:
            return True
