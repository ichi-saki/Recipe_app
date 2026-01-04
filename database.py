import sqlite3

def db_init():
    connection = sqlite3.connect('database/recipes.db')

    with open('schema.sql', 'r') as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()


if __name__ == '__main__':
    db_init()
    print('Database is initialized')