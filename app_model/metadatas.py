import pandas as pd
import sqlite3

def migrate_datasets_metadata(conn):
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn, if_exists='replace', index=False)

def get_all_datasets_metadata(conn):
    try:
        sql = 'SELECT * FROM datasets_metadata'
        data = pd.read_sql(sql, conn)
        return data
    except (pd.errors.DatabaseError, sqlite3.OperationalError):
        migrate_datasets_metadata(conn)
        sql = 'SELECT * FROM datasets_metadata'
        return data(sql, conn)
