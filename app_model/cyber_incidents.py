import pandas as pd
import sqlite3

def migrate_cyber_incidents(conn):
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn, if_exists='replace', index=False)

def get_all_cyber_incidents(conn):
    try:
        sql = 'SELECT * FROM cyber_incidents'
        data = pd.read_sql(sql, conn)
        return data
    except (pd.errors.DatabaseError, sqlite3.OperationalError):
        migrate_cyber_incidents(conn)
        sql = 'SELECT * FROM cyber_incidents'
        return data(sql, conn)
