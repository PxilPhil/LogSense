import psycopg2.errorcodes

from db_access import conn_pool
import pandas as pd
from datetime import datetime

from exceptions.DataBaseExcepion import DataBaseException
from exceptions.NotFoundExcepion import NotFoundException
from model.data import PCTimeSeriesData
from pydantic import BaseModel, create_model

from model.pc import NetworkInterface, Connection, Disk, DiskPartition, PCState, PCSpecs
from model.pc import DISK, PARTITION, DISKS


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


def get_total_pc_application_data_between(pc_id, start, end):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
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
        ram,
        cpu,
        context_switches,
        major_faults,
        open_files,
        thread_count,
        AVG(ram) OVER (ORDER BY measurement_time ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS moving_average_ram,
        AVG(cpu) OVER (ORDER BY measurement_time ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS moving_average_cpu
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
            for _, row in df.iterrows():
                data_list.append(PCTimeSeriesData(**row.to_dict()))
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
            return 0, 0
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def select_network_interfaces(pc_id):
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
        query = """
        SELECT ni.*
        FROM networkinterface ni
        JOIN pcdata pd ON ni.pcdata_id = pd.id
        WHERE pd.pc_id = %s AND pd.measurement_time = (SELECT MAX(measurement_time) from pcdata p where p.pc_id = %s);
        """

        cursor.execute(query, (pc_id, pc_id))
        result = cursor.fetchall()

        network_interfaces = [NetworkInterface(
            id=row[0],
            pcdata_id=row[1],
            name=row[2],
            display_name=row[3],
            ipv4_address=row[4],
            ipv6_address=row[5],
            subnet_mask=row[6],
            mac_address=row[7],
            bytes_received=row[8],
            bytes_sent=row[9],
            packets_received=row[10],
            packets_sent=row[11]
        ) for row in result]

        return network_interfaces
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def select_connections(pc_id):
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
        query = """
            SELECT con.*
            FROM connection con
            JOIN pcdata pd ON con.pcdata_id = pd.id
            WHERE pd.pc_id = %s AND pd.measurement_time = (SELECT MAX(measurement_time) from pcdata p where p.pc_id = %s);
        """

        cursor.execute(query, (pc_id, pc_id))
        result = cursor.fetchall()

        # Parse the query result into a list of Connection instances
        connections = [Connection(
            id=row[0],
            pcdata_id=row[1],
            localaddress=row[2],
            localport=row[3],
            foreignaddress=row[4],
            foreignport=row[5],
            state=row[6],
            type=row[7],
            owningprocessid=row[8]
        ) for row in result]

        return connections
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def select_disks(pc_id):
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
        query = """
            SELECT dp.id, dp.disk_id, dp.disk_store_name, dp.identification, dp.name, dp.type, dp.mount_point, dp.size, dp.major_faults, dp.minor_faults,
                   d.id AS disk_id, d.state_id, d.measurement_time, d.serialnumber, d.model, d.name AS disk_name, d.size AS disk_size
            FROM diskpartition dp
            JOIN disk d ON dp.disk_id = d.id
            WHERE d.state_id IN (
                SELECT id FROM pcstate WHERE pc_id = %s
            );
        """

        cursor.execute(query, (pc_id,))
        result = cursor.fetchall()

        disks = {}

        for row in result:
            disk_partition = DiskPartition(
                id=row[0],
                disk_id=row[1],
                disk_store_name=row[2],
                identification=row[3],
                name=row[4],
                type=row[5],
                mount_point=row[6],
                size=row[7],
                major_faults=row[8],
                minor_faults=row[9]
            )
            disk = Disk(
                id=row[10],
                state_id=row[11],
                measurement_time=row[12],
                serialnumber=row[13],
                model=row[14],
                name=row[15],
                size=row[16]
            )

            # Check if the disk is already in the dictionary, if not, add it
            if disk.id not in disks:
                disks[disk.id] = disk

            # Append the disk partition to the corresponding disk
            disks[disk.id].disk_partition_list.append(disk_partition)

        return list(disks.values())
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_recent_disk_and_partition(pcid):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query_state = f"SELECT id FROM PCState WHERE pc_id = {pcid} ORDER BY measurement_time DESC LIMIT 1;"
        cursor.execute(query_state)
        state_row = cursor.fetchall()

        if state_row:
            state_id = state_row[0]

            query_disk = """
                SELECT id, state_id, measurement_time, serialnumber, model, name, size FROM disk
                WHERE state_id = %s
                AND measurement_time = (
                    SELECT MAX(measurement_time) FROM disk WHERE state_id = %s
                )
            """
            cursor.execute(query_disk, (state_id, state_id))
            disk_row = cursor.fetchall()

            i = 1
            disks = []
            for row in disk_row:
                query_partition = """
                    SELECT id, disk_id, disk_store_name, identification, name, type, mount_point, size, major_faults,
                 minor_faults FROM diskpartition
                    WHERE disk_id = %s
                """
                cursor.execute(query_partition, (row[0],))
                partition = cursor.fetchall()

                partitions = []
                for partition_row in partition:
                    partition = PARTITION(id=partition_row[0],
                                          disk_id=partition_row[1],
                                          disk_store_name=partition_row[2],
                                          identification=partition_row[3],
                                          name=partition_row[4],
                                          type=partition_row[5],
                                          mount_point=partition_row[6],
                                          size=partition_row[7],
                                          major_faults=partition_row[8],
                                          minor_faults=partition_row[9])
                    partitions.append(partition)
                disk = DISK(id=row[0], state_id=row[1], measurement_time=row[2], serialnumber=row[3], model=row[4],
                            name=row[5], size=row[6], partitions=partitions)
                disks.append(disk)
                i = i + 1
            return DISKS(disks=disks)
    except Exception as e:
        print(e)
    finally:
        conn_pool.putconn(conn)
    return None


def select_recent_state():
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = "select * from pcstate where measurement_time=(select MAX(measurement_time) from pcstate)"

        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            state_dict = {
                "id": result[0],
                "measurement_time": result[1].isoformat(),
                "pc_id": result[2],
                "ram": result[3],
                "memory_page_size": result[4],
                "processor_name": result[5],
                "processor_identifier": result[6],
                "processor_id": result[7],
                "processor_vendor": result[8],
                "processor_bitness": result[9],
                "physical_package_count": result[10],
                "physical_processor_count": result[11],
                "logical_processor_count": result[12],
            }
            return state_dict
        return None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_recent_pc_total_data(pc_id, limit):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
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
        ram,
        cpu,
        context_switches,
        major_faults,
        open_files,
        thread_count
    FROM
        pcdata
    WHERE
        pc_id = %s AND
        measurement_time IN 
        (SELECT measurement_time from pcdata group by measurement_time order by measurement_time desc limit %s)
        """

        cursor.execute(query, (pc_id, limit))
        result = cursor.fetchall()

        if result:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            data_list = []
            for _, row in df.iterrows():
                data_list.append(PCTimeSeriesData(**row.to_dict()))
            return df, data_list
        return None, None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def general_specs(user_id):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        querry = """
        select 
        processor_name, 
        processor_identifier, 
        processor_id, 
        processor_vendor, 
        processor_bitness, 
        physical_package_count, 
        physical_processor_count,
        logical_processor_count 
        from pcstate
        WHERE pc_id = %s
        """

        querry2 = """
        select
            context_switches_processor,
             interrupts_processor
        from pcdata
        WHERE pc_id = %s
        ORDER BY measurement_time desc 
        """

        cursor.execute(querry, user_id)
        result = cursor.fetchone()

        cursor.execute(querry2, user_id)
        result2 = cursor.fetchone()

        if result and result2:
            processor_name, processor_identifier, processor_id, processor_vendor, processor_bitness, physical_package_count, physical_processor_count, logical_processor_count = result
            context_switches, interrupts = result2

            # Create an instance of PCSpecs
            pc_specs = PCSpecs(
                processor_name=processor_name,
                processor_identifier=processor_identifier,
                processor_id=processor_id,
                processor_vendor=processor_vendor,
                processor_bitness=processor_bitness,
                physical_package_count=physical_package_count,
                physical_processor_count=physical_processor_count,
                logical_processor_count=logical_processor_count,
                context_switches=context_switches,
                interrupts=interrupts
            )
            return pc_specs
        return None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def get_pc_data_at_measurement(ram_multiplier, timestamp: datetime, pc_id: int):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        query = """
        SELECT ram * %s AS ram FROM pcdata WHERE measurement_time = %s AND pc_id=%s;
        """

        cursor.execute(query, (ram_multiplier, timestamp, pc_id))
        result = cursor.fetchone()

        if result:
            return result[0]
        return None
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)
