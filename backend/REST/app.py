from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import extras
import configparser
import logging

app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

db_host = config.get('Database', 'db_host')
db_port = config.get('Database', 'db_port')
db_name = config.get('Database', 'db_name')
db_user = config.get('Database', 'db_user')
db_password = config.get('Database', 'db_password')

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
    print("Tables generated successfully.")
except FileNotFoundError:
    logging.error("SQL file not found.")
except Exception as e:
    logging.error(f"Error generating tables: {str(e)}")

@app.route('/', methods=["POST", "GET"])
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
