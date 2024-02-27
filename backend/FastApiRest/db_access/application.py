from datetime import datetime
from typing import List

from db_access import conn_pool
from exceptions.InvalidParametersException import InvalidParametersException
import pandas as pd
import psycopg2

from exceptions.DataBaseExcepion import DataBaseException
from model.application import ApplicationTimeSeriesData, TimeMetricData, TimeMetricDataList, ApplicationInfo


def get_application_between(pc_id: int, application_name, start, end, bucket_value: str = '1 minutes'):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        select_application_query = """
SELECT
    time_bucket(%s, measurement_time) AS bucket_time,
    mode() WITHIN GROUP (ORDER BY name) AS name,
    AVG(app.cpu) AS cpu,
    AVG(app.ram) AS ram,
    AVG(app.context_switches) AS context_switches,
    AVG(app.major_faults) AS major_faults,
    AVG(app.bitness) AS bitness,
    AVG(app.thread_count) AS thread_count,
    AVG(app.uptime) AS uptime,
    AVG(app.open_files) AS open_files,
    SUM(app.process_count_difference) AS process_count_difference
FROM
    applicationdata app
WHERE
    pc_id = %s AND
    name = %s AND
    measurement_time BETWEEN %s AND %s
GROUP BY
    bucket_time
ORDER BY
    bucket_time;

        """

        cursor.execute(select_application_query, (bucket_value, pc_id, application_name, start, end))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            df = df.rename(columns={'bucket_time': 'measurement_time'})
            # clearly define types
            df['ram'] = df['ram'].astype(float)
            df['cpu'] = df['cpu'].astype(float)

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
        app.name
        ORDER BY 
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


def get_relevant_application_data(pc_id: int, measurement_time, ram_threshold, cpu_threshold):  # gets all data contained in application data table
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
WITH MaxValues AS (
    SELECT
        app.id AS application_id,
        MAX(app.ram) AS max_ram,
        MAX(app.cpu) AS max_cpu
    FROM
        applicationdata AS app
    WHERE
        app.pc_id = %s AND
        app.measurement_time BETWEEN
            %s - INTERVAL '5 minutes' AND %s
    GROUP BY app.id
)
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
    MaxValues AS mv ON app.id = mv.application_id
WHERE
    app.pc_id = %s
    AND (
        mv.max_ram > %s
        OR
        mv.max_cpu > %s
    )
    AND app.measurement_time BETWEEN
        %s - INTERVAL '5 minutes' AND %s
ORDER BY app.measurement_time;
        """

        cursor.execute(query, (pc_id, measurement_time, measurement_time, pc_id, ram_threshold, cpu_threshold, measurement_time, measurement_time))
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
        (SELECT measurement_time from applicationdata where pc_id = %s group by measurement_time order by measurement_time desc limit %s)
        """

        if application_name:
            query += "AND app.name = %s"
            cursor.execute(query, (pc_id, pc_id, limit, application_name))
        else:
            cursor.execute(query, (pc_id, pc_id, limit))

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


def select_total_running_time_application(start: datetime, end: datetime, application_name: str, pc_id: int):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        total_running_time_query = """
        WITH app_with_lead AS (
            SELECT
                id,
                pcdata_id,
                pc_id,
                name,
                path,
                measurement_time,
                ram,
                cpu,
                LEAD(measurement_time) OVER (PARTITION BY pc_id, name ORDER BY measurement_time) AS next_measurement_time
            FROM
                applicationdata
            WHERE
                pc_id = %s AND
                name LIKE %s
        )
        SELECT
            name,
            SUM(
                CASE
                    WHEN EXTRACT(EPOCH FROM next_measurement_time - measurement_time) >= 30 AND EXTRACT(EPOCH FROM next_measurement_time - measurement_time) <= 90 THEN EXTRACT(EPOCH FROM next_measurement_time - measurement_time)
                    ELSE 0
                END
            ) AS total_running_time_seconds
        FROM
            app_with_lead
        WHERE
            next_measurement_time IS NOT NULL
            AND measurement_time BETWEEN %s AND %s
        GROUP BY
            name
        HAVING
            SUM(
                CASE
                    WHEN EXTRACT(EPOCH FROM next_measurement_time - measurement_time) >= 30 AND EXTRACT(EPOCH FROM next_measurement_time - measurement_time) <= 90 THEN EXTRACT(EPOCH FROM next_measurement_time - measurement_time)
                    ELSE 0
                END
            ) > 0
        ORDER BY
            SUM(ram) DESC, SUM(cpu) DESC;
        """

        cursor.execute(total_running_time_query, (pc_id, application_name, start, end))
        results = cursor.fetchall()

        if results:
            data_time = []
            for row in results:
                data_time.append(TimeMetricData(name= row[0], total_running_time_seconds= float(row[1])))
            result_class= TimeMetricDataList(data = data_time)
            return result_class
        else:
            return None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    except KeyError as e:
        raise InvalidParametersException()
    finally:
        conn_pool.putconn(conn)


def select_info_application(application_name, pc_id, start, end):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
        SELECT
            MAX (parent_process_id) as process_id,
            MAX (path) as path,
            MAX ("current_Working_Directory") AS working_directory,
            MAX (commandline) AS command_line,
            MAX ("user") AS windows_user_name,
            MAX (bitness) as bitness,
            MIN (state) as state,
            SUM (major_faults) as major_faults,
            SUM (context_switches) as context_switches,
            AVG (thread_count) AS threads,
            AVG (open_Files) AS open_files
        FROM applicationdata
        WHERE pc_id = %s AND name = %s 
        AND measurement_time BETWEEN %s AND %s
        GROUP BY name
        """

        cursor.execute(query, (pc_id, application_name, start, end))
        result = cursor.fetchone()

        if result:
            app_info = ApplicationInfo(
                process_id = result[0],
                path = result[1],
                working_directory= result[2],
                command_line= result[3],
                windows_user_name= result[4],
                bitness= result[5],
                state= result[6],
                major_faults= result[7],
                context_switches= result[8],
                threads= int(result[9]),
                open_files= int(result[10])
            )
            return app_info
        else:
            return None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    except KeyError as e:
        raise InvalidParametersException()
    finally:
        conn_pool.putconn(conn)


def get_application_data_at(pc_id: int, end: datetime, application_name):
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
        app.measurement_time = %s
        """

        if application_name:
            query += "AND app.name = %s"
            cursor.execute(query, (pc_id, end, application_name))
        else:
            cursor.execute(query, (pc_id, end))

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
