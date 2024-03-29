import logging
from datetime import datetime

import pandas as pd
import psycopg2
from fastapi import UploadFile

from db_access import conn_pool
from exceptions.DataBaseExcepion import DataBaseException
from exceptions.InvalidParametersException import InvalidParametersException


def update_pc_description(pc_id, client_df):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        row = client_df.iloc[0]
        manufacturer = row['computerManufacturer']
        model = row['computerModel']
        update_pc = """
        UPDATE PC
        SET manufacturer = %s,
        model = %s
        WHERE ID = %s;
        """
        cursor.execute(update_pc, (manufacturer, model, pc_id))
        conn.commit()

        return True
    except Exception as e:
        print(f"Error updating PC description: {e}")
        return False
    finally:
        conn_pool.putconn(conn)


def get_pc_state_df(client_df, conn):
    pc_id, state_id = get_pc_state_by_attributes_df(client_df)

    if pc_id:
        update_pc_description(pc_id, client_df,)

    if state_id:
        return state_id
    elif pc_id:
        state_id = insert_new_state_df(pc_id, client_df, conn)
        return state_id
    else:
        return None


def insert_new_state_df(pc_id, client_df, conn):
    row = client_df.iloc[0]
    try:
        measurement_time = datetime.fromtimestamp(int(int(row['measurement_time']) / 1000))
        return insert_new_state(pc_id,
                                measurement_time,
                                int(row['memoryTotalSize']),
                                int(row['memoryPageSize']),
                                row['processorName'],
                                row['processorIdentifier'],
                                row['processorID'],
                                row['processorVendor'],
                                int(row['processorBitness']),
                                int(row['physicalPackageCount']),
                                int(row['physicalProcessorCount']),
                                int(row['logicalProcessorCount']),
                                conn)
    except KeyError as e:
        raise InvalidParametersException()


def insert_new_state(pc_id,
                     measurement_time,
                     provided_total_memory_size,
                     provided_memory_page_size,
                     provided_processor_name,
                     provided_processor_identifier,
                     provided_processor_id,
                     provided_processor_vendor,
                     provided_processor_bitness,
                     provided_package_count,
                     provided_physical_processor_count,
                     provided_logical_processor_count,
                     conn):
    cursor = conn.cursor()
    try:
        pcdata = (
            pc_id,
            measurement_time,
            provided_total_memory_size,
            provided_memory_page_size,
            provided_processor_name,
            provided_processor_identifier,
            provided_processor_id,
            provided_processor_vendor,
            provided_processor_bitness,
            provided_package_count,
            provided_physical_processor_count,
            provided_logical_processor_count)

        sql_query = """
            INSERT INTO PCState (
            pc_id, 
            measurement_time,
            total_memory_size, 
            memory_page_size, 
            processor_name, 
            processor_identifier, 
            processor_id, 
            processor_vendor, 
            processor_bitness, 
            physical_package_count, 
            physical_processor_count, 
            logical_processor_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """

        cursor.execute(sql_query, pcdata)
        result = cursor.fetchone()

        if result:
            state_id = result[0]
            return state_id
        else:
            return None
    except psycopg2.DatabaseError as e:
        logging.ERROR(str(e))
        raise DataBaseException()


def get_pc_state_by_attributes_df(client_df):
    row = client_df.iloc[0]
    try:
        return get_pc_state_by_attributes(row['computerHardwareUUID'],
                                          int(row['memoryTotalSize']),
                                          int(row['memoryPageSize']),
                                          row['processorName'],
                                          row['processorIdentifier'],
                                          row['processorID'],
                                          row['processorVendor'],
                                          int(row['processorBitness']),
                                          int(row['physicalProcessorCount']),
                                          int(row['logicalProcessorCount']))
    except KeyError as e:
        raise InvalidParametersException()


def get_pc_state_by_attributes(provided_uuid,
                               provided_total_memory_size,
                               provided_memory_page_size,
                               provided_processor_name,
                               provided_processor_identifier,
                               provided_processor_id,
                               provided_processor_vendor,
                               provided_processor_bitness,
                               provided_physical_processor_count,
                               provided_logical_processor_count):

    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        pc = (provided_uuid,)

        sql_query = """
                    SELECT pc.ID AS pc_id
                    FROM PC pc
                    WHERE pc.hardware_UUID = %s;
                """

        cursor.execute(sql_query, pc)
        pcresult = cursor.fetchone()

        if not pcresult:
            return None, None

        pc_id = pcresult[0]

        pcdata = (provided_uuid,
                  int(provided_total_memory_size),
                  int(provided_memory_page_size),
                  provided_processor_name,
                  provided_processor_identifier,
                  provided_processor_id,
                  provided_processor_vendor,
                  int(provided_processor_bitness),
                  int(provided_physical_processor_count),
                  int(provided_logical_processor_count))

        sql_query = """
            SELECT pc.ID AS pc_id, state.id AS state_id
            FROM PC pc
            JOIN PCState state ON pc.ID = state.pc_id
            WHERE pc.hardware_UUID = %s
            AND state.total_memory_size = %s
            AND state.memory_page_size = %s
            AND state.processor_name = %s
            AND state.processor_identifier = %s
            AND state.processor_id = %s
            AND state.processor_vendor = %s
            AND state.processor_bitness = %s
            AND state.physical_processor_count = %s
            AND state.logical_processor_count = %s;
        """

        cursor.execute(sql_query, pcdata)
        result = cursor.fetchone()

        if result:
            pc_id, state_id = result
            return pc_id, state_id
        else:
            return pc_id, None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_dfdict_from_filelist(files: list[UploadFile]):
    df_map = dict()
    for file in files:
        df_map[file.filename] = pd.read_csv(file.file, sep='|')
    return df_map


def update_disk_df(state_id, disk_df, partition_df, conn):
    exists = does_last_disk_overlap(state_id, disk_df)
    if exists:
        return True

    return insert_disk_and_partition(state_id, disk_df, partition_df, conn)


def does_last_disk_overlap(state_id, disk_df):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        querry = """
                SELECT measurement_time
                FROM disk
                WHERE serialnumber = %s
                    AND model = %s
                    AND name = %s
                    AND size = %s
                    AND state_id = %s
                    AND measurement_time = (
                        SELECT MAX(measurement_time)
                        FROM disk
                        WHERE state_id = %s
                    )
                ;"""
        for i, row in disk_df.iterrows():
            cursor.execute(querry, (row['serialNumber'],
                                    row['model'],
                                    row['name'],
                                    row['size'],
                                    state_id,
                                    state_id))
            timestamp = cursor.fetchone()
            if not timestamp:
                return None

        querry = """
                SELECT count(*)
                FROM disk
                WHERE state_id = %s
                    AND measurement_time = (
                        SELECT MAX(measurement_time)
                        FROM disk
                        WHERE state_id = %s
                    )
                ;"""
        cursor.execute(querry, (state_id, state_id))
        disk_amount = cursor.fetchone()


        if disk_amount:
            return disk_amount[0] == len(disk_df.index)
        return None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    except KeyError as e:
        raise InvalidParametersException()
    finally:
        conn_pool.putconn(conn)


def insert_disk_and_partition(state_id, disk_df, partition_df, conn):
    cursor = conn.cursor()
    try:
        insert_disk = """INSERT INTO disk(state_id, measurement_time, serialnumber, model, name, size)VALUES %s RETURNING id;"""
        disks = []
        for i, row in disk_df.iterrows():
            timestamp = datetime.fromtimestamp(int(int(row['measurement_time']) / 1000))
            disk = (state_id, timestamp, row['serialNumber'], row['model'], row['name'], row['size'])
            disks.append(disk)
        psycopg2.extras.execute_values(cursor, insert_disk, disks)

        selct_disk_id = """ 
            SELECT d.id
            FROM disk d
            WHERE d.name = %s
              AND d.state_id = %s
              AND d.measurement_time = (
                SELECT MAX(measurement_time)
                FROM disk
                WHERE name = %s
                  AND state_id = %s
              );
        """
        insert_partition = """
            INSERT INTO diskpartition 
            (disk_id, disk_store_name, identification, name, type, mount_point, size, major_faults, minor_faults)
            VALUES %s;
        """
        partitions = []
        for i, row in partition_df.iterrows():
            cursor.execute(selct_disk_id, (row['diskStoreName'], state_id, row['diskStoreName'], state_id))
            disk_id = cursor.fetchone()
            partition = (disk_id, row['diskStoreName'], row['identification'], row['name'], row['type'], row['mountPoint'], row['size'], row['majorFaults'] , row['minorFaults'])
            partitions.append(partition)
        psycopg2.extras.execute_values(cursor, insert_partition, partitions)

        return True
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    except KeyError as e:
        raise InvalidParametersException()


"""def is_anomaly_subsequent(anomaly_id, pc_id): # TODO: remove Joins
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        querry = ""
        SELECT
        LAG(ad.ID) OVER (PARTITION BY pcd.state_id, ad.name ORDER BY ad.measurement_time) AS preceding_applicationdata_id
        FROM applicationdata ad
        JOIN pcdata pcd ON ad.PcData_ID = pcd.id
        WHERE ad.name = %s and pcdata_id != %s
        ORDER BY pcdata_id desc LIMIT 1;""
    
        cursor.execute(querry, (name, pcdata_id))
        disk_amount = cursor.fetchone()
    
    
        if disk_amount:
            return disk_amount[0] == len(disk_df.index)
        return None
    finally:
        conn_pool.putconn(conn)"""