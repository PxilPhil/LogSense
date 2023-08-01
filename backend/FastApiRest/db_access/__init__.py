import configparser
import logging

import psycopg2
from psycopg2 import pool


def get_database_config(path):
    config = configparser.ConfigParser()
    config.read(path)

    db_host = config.get('Database', 'db_host')
    db_port = config.get('Database', 'db_port')
    db_name = config.get('Database', 'db_name')
    db_user = config.get('Database', 'db_user')
    db_password = config.get('Database', 'db_password')

    return db_host, db_port, db_name, db_user, db_password

def create_tables(conn_pool):
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
        with open('tables.sql', 'r') as file:
            sql_statements = file.read()
            cursor.execute(sql_statements)
            conn.commit()
        logging.info("Tables generated successfully.")
    except FileNotFoundError:
        logging.error("SQL file not found.")
    except Exception as e:
        logging.error(f"Error generating tables: {str(e)}")
    finally:
        conn_pool.putconn(conn)

def create_standard_anomalie(conn_pool):
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
        with open('standardAnomaly.sql', 'r') as file:
            sql_statements = file.read()
            cursor.execute(sql_statements)
            conn.commit()
        logging.info("Anomalie generated successfully.")
    except FileNotFoundError:
        logging.error("SQL file not found.")
    except Exception as e:
        logging.error(f"Error generating Anomalies: {str(e)}")
    finally:
        conn_pool.putconn(conn)

logging.basicConfig(filename='app.log', level=logging.INFO)

db_host, db_port, db_name, db_user, db_password = get_database_config('config.ini')

conn_pool = pool.SimpleConnectionPool(
    0,
    8,
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password,
)

create_tables(conn_pool)
create_standard_anomalie(conn_pool)