from __future__ import annotations
from datetime import datetime
import psycopg2.errorcodes

import psycopg2

from exceptions.InvalidParametersException import InvalidParametersException
from db_access import conn_pool
from psycopg2 import extras

from db_access.data_helper import get_pc_state_df, update_disk_df
from db_access.helper import get_pcid_by_stateid
from exceptions.DataBaseExcepion import DataBaseException
from exceptions.DataBaseInsertExcepion import DataBaseInsertException


def insert_running_pcdata(state_id, running_df_dict, pc_total_df, anomaly_list):
    # TODO: Optionally save moving averages into database if its too slow to calculate it every time
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        first_row_pc_total = pc_total_df.iloc[0]
        first_row_pc = running_df_dict['resources'].iloc[0]
        pcdata_id = 0

        timestamp_pc = datetime.fromtimestamp(pc_total_df.index[0] / 1000)
        pc_id = get_pcid_by_stateid(state_id)
        pcdata_values = (
            state_id,
            pc_id,
            timestamp_pc,
            int(first_row_pc["freeDiskSpace"]),
            int(first_row_pc["readBytesDiskStores"]),
            int(first_row_pc["readsDiskStores"]),
            int(first_row_pc["writeBytesDiskStores"]),
            int(first_row_pc["writesDiskStores"]),
            int(first_row_pc["partitionsMajorFaults"]),
            int(first_row_pc["partitionsMinorFaults"]),
            int(first_row_pc["availableMemory"]),
            first_row_pc["namesPowerSources"],
            bool(first_row_pc["chargingPowerSources"]),
            bool(first_row_pc["dischargingPowerSources"]),
            bool(first_row_pc["powerOnLinePowerSources"]),
            int(first_row_pc["remainingCapacityPercentPowerSources"]),
            int(first_row_pc["contextSwitchesProcessor"]),
            int(first_row_pc["interruptsProcessor"]),
            float(pc_total_df["cpuUsage"]),
            int(pc_total_df["residentSetSize"]),
            int(pc_total_df["contextSwitches"]),
            int(pc_total_df["majorFaults"]),
            int(pc_total_df["openFiles"]),
            int(pc_total_df["threadCount"])
        )

        pcdata_query = """
            INSERT INTO pcdata (
                state_id,
                pc_id,
                measurement_time,
                free_disk_space,
                read_bytes_disks,
                reads_disks,
                write_bytes_Disks,
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
                cpu,
                ram,
                context_switches,
                major_faults,
                open_files,
                thread_count
            ) VALUES %s RETURNING id;
            """

        cursor.execute(pcdata_query, (pcdata_values,))
        pcdata_id = cursor.fetchone()[0]

        applications = []
        for index, row in running_df_dict["application"].iterrows():
            # print(index)
            # print(row[index])
            # print(row['residentSetSize'])
            timestamp = datetime.fromtimestamp(index / 1000)
            application_data = (
                pcdata_id,
                pc_id,
                timestamp_pc,
                row['name'],
                row['path'],
                row['cpuUsage'],
                row['residentSetSize'],
                row['state'],
                row['user'],
                row['contextSwitches'],
                row['majorFaults'],
                row['bitness'],
                row['commandLine'],
                row['currentWorkingDirectory'],
                row['openFiles'],
                row['parentProcessID'],
                row['threadCount'],
                row['upTime'],
                row['processCountDifference']
            )
            applications.append(application_data)

        application_data_query = """
            INSERT INTO applicationdata 
            (PcData_ID, PC_id, measurement_time, name, path, cpu, ram, state, "user", context_switches, major_faults, bitness, commandline, "current_Working_Directory", open_Files, parent_Process_ID, thread_count, uptime, process_count_difference)
            VALUES %s;
        """
        psycopg2.extras.execute_values(cursor, application_data_query, applications)

        connections = []
        for index, row in running_df_dict["connection"].iterrows():
            timestamp = datetime.fromtimestamp(index / 1000)
            connection_data = (
                pcdata_id,
                row['localAddress'],
                row['localPort'],
                row['foreignAddress'],
                row['foreignPort'],
                row['state'],
                row['type'],
                row['owningProcessID']
            )
            connections.append(connection_data)

        connection_data_query = """
            INSERT INTO Connection
            (pcdata_ID, localAddress, localPort, foreignAddress, foreignPort, state, type, owningProcessID)
            VALUES %s;
        """
        psycopg2.extras.execute_values(cursor, connection_data_query, connections)

        # Assuming you have imported the required libraries and established a connection to the database

        network_interfaces = []
        for index, row in running_df_dict["network"].iterrows():
            timestamp = datetime.fromtimestamp(index / 1000)
            network_interface_data = (
                pcdata_id,
                row['name'],
                row['displayName'],
                row['ipv4Address'],
                row['ipv6Address'],
                row['subnetMask'],
                row['macAddress'],
                row['packetsReceived'],
                row['bytesSent'],
                row['packetsReceived'],
                row['packetsSent']
            )
            network_interfaces.append(network_interface_data)

        network_interface_data_query = """
            INSERT INTO networkInterface 
            (PcData_ID, name, display_name, ipv4_address, ipv6_address, subnet_mask, mac_address, bytes_received, bytes_sent, packets_received, packets_sent)
            VALUES %s;
        """
        psycopg2.extras.execute_values(cursor, network_interface_data_query, network_interfaces)

        conn.commit()

        insert_anomalies(pcdata_id, anomaly_list)

        return pcdata_id
    except psycopg2.DatabaseError as e:
        conn.rollback()
        if e.pgerror == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
            raise DataBaseInsertException(detail=f"Issue inserting into Table {str(e.diag.table_name)}")
        if e.pgerror == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
            raise InvalidParametersException()
        raise DataBaseException()
    except KeyError as e:
        raise InvalidParametersException()
    finally:
        conn_pool.putconn(conn)


def get_moving_avg_of_application(pc_id: int, application):  # returns moving avg of the last 5 columns
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        moving_avg_query = """
        SELECT
        AVG(app.ram) OVER (ORDER BY app.measurement_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_ram,
        AVG(app.cpu) OVER (ORDER BY app.measurement_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_cpu
        FROM
        applicationdata AS app
        WHERE
        app.pc_id = %s AND app.name = %s
        ORDER BY
        app.measurement_time;
        """

        cursor.execute(moving_avg_query, (pc_id, application))
        result = cursor.fetchone()

        if result:
            return result[0], result[1]
        else:
            return 0, 0
    except psycopg2.DatabaseError as e:
        raise DataBaseException()
    except KeyError as e:
        raise InvalidParametersException()
    finally:
        conn_pool.putconn(conn)


def insert_inital_pcdata(df_dict):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        state_id = get_pc_state_df(df_dict['client'], conn)

        success = update_disk_df(state_id, df_dict['disk'], df_dict['partition'], conn)

        if success:
            conn.commit()
            return state_id
        conn.rollback()
        return None
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise DataBaseException()
    finally:
        conn_pool.putconn(conn)


def insert_anomalies(pcdata_id, anomaly_list):
    conn = conn_pool.getconn()
    cursor = conn.cursor()
    try:
        insert_anomaly_query = """
        INSERT INTO applicationdata_anomaly (anomaly_id, applicationdata_id, user_id, pc_id, change_in_percentage, data_type, subsequent_anomaly) 
        VALUES 
        (%s, (SELECT id FROM applicationdata where name=%s and pcdata_id=%s),(SELECT user_id FROM pc WHERE id = (SELECT pc_id FROM applicationdata where name=%s and pcdata_id=%s)), (SELECT pc_id FROM applicationdata where name=%s and pcdata_id=%s), %s ,%s, FALSE)"""
        for anomaly in anomaly_list:
            anomaly_data = (
                anomaly.anomaly_type,
                anomaly.application,
                pcdata_id,
                anomaly.application,
                pcdata_id,
                anomaly.application,
                pcdata_id,
                anomaly.change,
                anomaly.column
            )
            cursor.execute(insert_anomaly_query, anomaly_data)
        conn.commit()
    except psycopg2.DatabaseError as e:
        conn.rollback()
        if e.pgerror == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
            raise DataBaseInsertException(detail=f"Issue inserting into Table {str(e.diag.table_name)}")
        raise DataBaseException()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn_pool.putconn(conn)
