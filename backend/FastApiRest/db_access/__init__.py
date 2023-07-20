import configparser
import logging

import psycopg2


def get_database_config(path):
    config = configparser.ConfigParser()
    config.read(path)

    db_host = config.get('Database', 'db_host')
    db_port = config.get('Database', 'db_port')
    db_name = config.get('Database', 'db_name')
    db_user = config.get('Database', 'db_user')
    db_password = config.get('Database', 'db_password')

    return db_host, db_port, db_name, db_user, db_password


def generate_tables(db_host, db_port, db_name, db_user, db_password):
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password,
    )
    cursor = conn.cursor()

    try:
        with open('tables.sql', 'r') as file:
            sql_statements = file.read()
            cursor.execute(sql_statements)
            conn.commit()
        logging.info("Tables generated successfully.")
        return True, conn, cursor
    except FileNotFoundError:
        logging.error("SQL file not found.")
        return False
    except Exception as e:
        logging.error(f"Error generating tables: {str(e)}")
        return False


logging.basicConfig(filename='app.log', level=logging.INFO)

db_host, db_port, db_name, db_user, db_password = get_database_config('config.ini')
bool, conn, cursor = generate_tables(db_host, db_port, db_name, db_user, db_password)