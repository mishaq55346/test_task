import sqlite3

conn = sqlite3.connect("mydatabase.db", check_same_thread=False)  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()


class Database(object):
    def __init__(self):
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id text PRIMARY KEY, state text, pizza_size text, '
                       'payment_method text)')
        conn.commit()

    def add_user(self, person_id, state):
        cursor.execute('INSERT INTO users (id, state) VALUES ("{}","{}")'.format(str(person_id), state))
        conn.commit()

    def update_info(self, person_id, newState, pizza_size, payment_method):
        cursor.execute(
            'UPDATE users SET state = "{}", pizza_size = "{}", payment_method = "{}"  WHERE id = "{}"'.format(newState,
                                                                                                              pizza_size,
                                                                                                              payment_method,
                                                                                                              person_id))
        conn.commit()

    def has_user(self, person_id):
        info = cursor.execute('SELECT * FROM users WHERE id="{}"'.format(str(person_id)))
        if info.fetchone() is None:
            return False
        else:
            return True

    def get_state(self, person_id):
        state = cursor.execute('SELECT state FROM users WHERE id="{}"'.format(str(person_id)))
        return str(state.fetchone()).replace("(\'", '').replace("\',)", '')

    def get_pizza_size(self, person_id):
        pizza_size = cursor.execute('SELECT pizza_size FROM users WHERE id="{}"'.format(str(person_id)))
        return str(pizza_size.fetchone()).replace("(\'", '').replace("\',)", '')

    def get_payment_method(self, person_id):
        payment_method = cursor.execute('SELECT payment_method FROM users WHERE id="{}"'.format(str(person_id)))
        return str(payment_method.fetchone()).replace("(\'", '').replace("\',)", '')
