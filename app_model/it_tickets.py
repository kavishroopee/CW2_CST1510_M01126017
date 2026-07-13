import pandas as pd
import sqlite3

def migrate_it_tickets(conn):
    data = pd.read_csv('DATA/it_tickets.csv')
    data.to_sql('it_tickets', conn, if_exists='replace', index=False)

def get_all_it_tickets(conn):
    try:
        sql = 'SELECT * FROM it_tickets'
        data = pd.read_sql(sql, conn)
        return data
    except (pd.errors.DatabaseError, sqlite3.OperationalError):
        migrate_it_tickets(conn)
        sql = 'SELECT * FROM it_tickets'
        return data(sql, conn)
