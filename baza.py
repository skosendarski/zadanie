import sqlite3


db_path = 'zbiory.db'
conn = sqlite3.connect(db_path)

c = conn.cursor()

c.execute('''
          CREATE TABLE zbior
          ( id INTEGER PRIMARY KEY,
            przedmiot VARCHAR(100),
            ilosc NUMERIC NOT NULL
          )
          ''')


c.execute('''
          CREATE TABLE zadania
          ( lista VARCHAR(100),
            amount NUMERIC NOT NULL,
            przedmiot_id INTEGER,
            FOREIGN KEY(przedmiot_id) REFERENCES przedmiot(id),
            PRIMARY KEY (lista, przedmiot_id))
          ''')
