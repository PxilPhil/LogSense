from db_access import cursor, conn
import pandas as pd
from datetime import datetime
from model.data import PCTimeSeriesData


def add_pc(user_id, hardware_uuid, client_name):
    # TODO: check if user exsists

    query = "INSERT INTO PC (USER_ID, hardware_uuid, client_name) VALUES (%s, %s, %s) RETURNING ID;"
    params = (str(user_id), str(hardware_uuid), str(client_name))

    pc_id = -1
    try:
        cursor.execute(query, params)
        pc_id = cursor.fetchone()[0]
        print("Insertion successful. PC ID:", pc_id)
    except Exception as e:
        print("Error occurred:", str(e))

    conn.commit()

    return pc_id


def get_pcs():
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


def get_pcs_by_userid(user_id):
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


def get_total_pc_data(pc_id, start, end, type):
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
    thread_count
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
        #TODO: Move into manipulation
        for _, row in df.iterrows():
            # Convert the 'measurement_time' from string to a datetime object
            data_list.append(PCTimeSeriesData(**row.to_dict()))
        return df, data_list
    return None, None


def get_pc_data(pc_id, start, end):
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

def get_free_disk_space_data(pc_id):
    query = "select measurement_time,free_disk_space from pcdata where pc_id = %s"
    cursor.execute(query, (pc_id,))
    result = cursor.fetchall()

    if result:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns)
        return df
    return None
