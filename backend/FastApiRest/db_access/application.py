from db_access import conn_pool
import pandas as pd
import logging

from datetime import datetime

import psycopg2

from db_access import cursor, conn
from psycopg2 import extras
from model.data import ApplicationTimeSeriesData


def get_application(pc_id: int, application_name, start, end):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        select_application_query = """
        SELECT
            app.id,
            app.pcdata_id,
            app.measurement_time,
            app.name,
            app.path,
            app.cpu,
            app.ram,
            app.state,
            app."user",
            app.context_switches,
            app.major_faults,
            app.bitness,
            app.commandline,
            app."current_Working_Directory",
            app.open_files,
            app.parent_process_id,
            app.thread_count,
            app.uptime,
            app.process_count_difference,
            AVG(app.ram) OVER (PARTITION BY app.name ORDER BY app.measurement_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_ram
        FROM
            applicationdata AS app
        JOIN
            pcdata AS pc ON app.pcdata_id = pc.id
        WHERE
            pc.pc_id = %s AND
            app.name = %s AND
            app.measurement_time BETWEEN %s AND %s
        ORDER BY
            app.measurement_time;
        """

        cursor.execute(select_application_query, (pc_id, application_name, start, end))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            #data_list = df.to_dict(orient='records')
            #TODO: Move into manipulation
            application_list = []
            for _, row in df.iterrows():
                # Convert the 'measurement_time' from string to a datetime object
                application_list.append(ApplicationTimeSeriesData(**row.to_dict()))

            return df, application_list
        else:
            return None, None
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(str(e))
    finally:
        conn_pool.putconn(conn)


def get_application_list(pc_id: int, start, end):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        select_app_list_query = """
        SELECT
        app.name
        FROM
        applicationdata AS app
        JOIN
        pcdata AS pc ON app.pcdata_id = pc.id
        WHERE
        pc.pc_id = %s AND
        app.measurement_time BETWEEN %s AND %s
        GROUP BY
        app.name"""

        cursor.execute(select_app_list_query, (pc_id, start, end))
        result = cursor.fetchall()

        application_list = []  # List to hold the dictionaries
        if result:
            for row in result:
                application_list.append(row[0])
        return application_list
    finally:
        conn_pool.putconn(conn)


def get_latest_application_data(pc_id: int):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
        SELECT
        app.id,
        app.pcdata_id,
        app.measurement_time,
        app.name,
        app.path,
        app.cpu,
        app.ram,
        app.state,
        app."user",
        app.context_switches,
        app.major_faults,
        app.bitness,
        app.commandline,
        app."current_Working_Directory",
        app.open_files,
        app.parent_process_id,
        app.thread_count,
        app.uptime,
        app.process_count_difference
        FROM
        applicationdata AS app
        JOIN
        pcdata AS pc ON app.pcdata_id = pc.id
        WHERE
        pc.pc_id = %s AND
        app.measurement_time = (SELECT
        MAX(measurement_time) AS latest_measurement_time
        FROM
        applicationdata);
        """

        cursor.execute(query, (pc_id,))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            data_list = df.to_dict(orient='records')

            return df, data_list
        else:
            return None, None
    finally:
        conn_pool.putconn(conn)
