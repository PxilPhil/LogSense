from db_access import conn_pool
from exceptions.InvalidParametersException import InvalidParametersException
import pandas as pd
import psycopg2

from exceptions.DataBaseExcepion import DataBaseException
from model.application import ApplicationTimeSeriesData


def get_application_between(pc_id: int, application_name, start, end):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        select_application_query = """
        SELECT
            id,
            pcdata_id,
            measurement_time,
            name,
            path,
            cpu,
            ram,
            state,
            "user",
            context_switches,
            major_faults,
            bitness,
            commandline,
            "current_Working_Directory",
            open_files,
            parent_process_id,
            thread_count,
            uptime,
            process_count_difference,
            AVG(ram) OVER (PARTITION BY name ORDER BY measurement_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_ram,
            AVG(cpu) OVER (PARTITION BY name ORDER BY measurement_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_cpu
        FROM
            applicationdata
        WHERE
            pc_id = %s AND
            name = %s AND
            measurement_time BETWEEN %s AND %s
        ORDER BY
            measurement_time;
        """

        cursor.execute(select_application_query, (pc_id, application_name, start, end))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            application_list = []
            for _, row in df.iterrows():
                # Convert the 'measurement_time' from string to a datetime object
                application_list.append(ApplicationTimeSeriesData(**row.to_dict()))

            return df, application_list
        else:
            return None, None
    except psycopg2.DatabaseError as e:
        if e.pgerror == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
            raise InvalidParametersException()
        raise DataBaseException()
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
    except psycopg2.DatabaseError as e:
        if e.pgerror == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
            raise InvalidParametersException()
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_latest_application_data(pc_id: int, limit, application_name):
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
        WHERE
        app.pc_id = %s AND
        app.measurement_time IN 
        (SELECT measurement_time from applicationdata group by measurement_time order by measurement_time desc limit %s)
        """

        if application_name:
            query += "AND app.name = %s"
            cursor.execute(query, (pc_id, limit, application_name))
        else:
            cursor.execute(query, (pc_id, limit))

        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            data_list = df.to_dict(orient='records')

            return df, data_list
        else:
            return None, None
    except psycopg2.DatabaseError as e:
        if e.pgerror == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
            raise InvalidParametersException()
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_grouped_by_interval_application(pc_id: int, application_name: str, start, end, time_bucket_value,
                                        limit):  # time bucket value can be '5 minutes' for instance
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        # If we don't want moving avg we can drop the first part of the query and only keep the subquery
        query = """
        SELECT
            date_interval,
            cpu,
            ram,
            context_switches,
            major_faults,
            bitness,
            open_files,
            thread_count,
            uptime,
            process_count_difference,
            AVG(ram) OVER (PARTITION BY %s ORDER BY date_interval ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_ram
        FROM (
            SELECT
                time_bucket(%s, measurement_time) AS date_interval,
                AVG(cpu) AS cpu,
                AVG(ram) AS ram,
                AVG(context_switches) AS context_switches,
                AVG(major_faults) AS major_faults,
                AVG(bitness) AS bitness,
                AVG(open_files) AS open_files,
                AVG(thread_count) AS thread_count,
                AVG(uptime) AS uptime,
                SUM(process_count_difference) AS process_count_difference
            FROM
                applicationdata
            WHERE
                pc_id=%s AND name=%s AND measurement_time BETWEEN %s AND %s
            GROUP BY
                date_interval
        ) AS subquery
        ORDER BY
            date_interval
        LIMIT %s    
        """

        cursor.execute(query, (application_name, time_bucket_value, pc_id, application_name, start, end, limit))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            data_list = df.to_dict(orient='records')

            return df, data_list
        else:
            return None, None
    except psycopg2.DatabaseError as e:
        if e.pgerror == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
            raise InvalidParametersException()
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)
