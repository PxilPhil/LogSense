from db_access import cursor, conn
import pandas as pd

from datetime import datetime

import psycopg2

from db_access import cursor, conn
from psycopg2 import extras


def get_application(pc_id: int, application_name, start, end):
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
    app.process_count_difference
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
        data_list = df.to_dict(orient='records')

        return df, data_list
    else:
        return None, None


def get_application_list(pc_id: int, start, end):
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
            application_list.append(row)
    return application_list


def get_latest_application_data(pc_id: int):
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
