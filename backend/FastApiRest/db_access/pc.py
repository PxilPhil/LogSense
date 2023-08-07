import psycopg2.errorcodes

from db_access import conn_pool
import pandas as pd
from datetime import datetime

from exceptions.DataBaseExcepion import DataBaseException
from exceptions.NotFoundExcepion import NotFoundException
from model.data import PCTimeSeriesData


def add_pc(user_id, hardware_uuid, client_name):
    # TODO: check if user exsists
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO PC (USER_ID, hardware_uuid, client_name) VALUES (%s, %s, %s) RETURNING ID;"
        params = (str(user_id), str(hardware_uuid), str(client_name))

        pc_id = -1
        cursor.execute(query, params)
        pc_id = cursor.fetchone()[0]
        print("Insertion successful. PC ID:", pc_id)

        conn.commit()

        return pc_id
    except psycopg2.DatabaseError as e:
        conn.rollback()
        if e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
            raise NotFoundException(detail="User not found.")
        else:
            raise DataBaseException()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn_pool.putconn(conn)


def get_pcs():
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
            SELECT u.Name AS username, u.EMail AS email, pc.hardware_uuid, pc.client_name, pc.manufacturer, pc.model
            FROM logSenseUser u
            JOIN PC pc ON u.ID = pc.USER_ID;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        pcs = []
        for row in rows:
            pc = {'user_name': row[0], 'email': row[1], 'hardware_uuid': row[2], 'client_name': row[3],
                  'manufacturer': row[4], 'model': row[5]}
            pcs.append(pc)
        return pcs
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_pcs_by_userid(user_id):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
            SELECT pc.hardware_uuid, pc.client_name, pc.manufacturer, pc.model
            FROM PC pc
            WHERE pc.USER_ID = %s;
    
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        pcs = []
        for row in rows:
            pc = {'hardware_uuid': row[0], 'client_name': row[1], 'manufacturer': row[2], 'model': row[3]}
            pcs.append(pc)
        return pcs
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_total_pc_data(pc_id, start, end, type):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = f"""
        SELECT
        id,
        state_id,
        pc_id,
        measurement_time,
        free_disk_space,
        read_bytes_disks,
        reads_disks,
        write_bytes_disks,
        writes_disks,
        partition_major_faults,
        partition_minor_faults,
        available_memory,
        names_power_source,
        charging_power_sources,
        discharging_power_sources,
        power_online_power_sources,
        remaining_capacity_percent_power_sources,
        context_switches_processor,
        interrupts_processor,
        {type}, 
        context_switches,
        major_faults,
        open_files,
        thread_count,
        AVG(ram) OVER (ORDER BY measurement_time ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS moving_average_ram
    FROM
        pcdata
    WHERE
        pc_id = %s AND
        measurement_time BETWEEN %s AND %s;
        """

        cursor.execute(query, (pc_id, start, end))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            data_list = []
            # TODO: Move into manipulation
            for _, row in df.iterrows():
                # Convert the 'measurement_time' from string to a datetime object
                data_list.append(PCTimeSeriesData(**row.to_dict()))
            return df, data_list
        return None, None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_pc_data(pc_id, start, end):
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
        app.measurement_time BETWEEN %s AND %s;
        """

        cursor.execute(query, (pc_id, start, end))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            data_list = df.to_dict(orient='records')
            return df, data_list
        return None, None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_free_disk_space_data(pc_id):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = "select measurement_time,free_disk_space from pcdata where pc_id = %s"
        cursor.execute(query, (pc_id,))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            return df
        return None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_latest_moving_avg(pc_id: int):  # returns moving avg of the last 5 columns for the total pc
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        moving_avg_query = """
        SELECT
        AVG(ram) OVER (ORDER BY measurement_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_ram,
        AVG(cpu) OVER (ORDER BY measurement_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_cpu
        FROM
        pcdata
        WHERE
        pc_id = %s
        ORDER BY
        measurement_time desc
        LIMIT 1;
        """

        cursor.execute(moving_avg_query, (pc_id,))
        result = cursor.fetchone()

        if result:
            return result[0], result[1]
        else:
            return 0,0
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)
