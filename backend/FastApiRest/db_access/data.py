from datetime import datetime

import psycopg2

from db_access import cursor, conn
from psycopg2 import extras

from db_access.helper import get_pcid_by_stateid


def insert_pcdata(state_id, df_dict, pc_total_df,
                  anomalies):  # TODO: Optionally save moving averages into database if its too slow to calculate it every time
    try:
        first_row_pc_total = pc_total_df.iloc[0]
        first_row_pc = df_dict['resources'].iloc[0]
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
        for index, row in df_dict["application"].iterrows():
            # print(index)
            # print(row[index])
            # print(row['residentSetSize'])
            application_data = (
                pcdata_id,
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
            (PcData_ID, measurement_time, name, path, cpu, ram, state, "user", context_switches, major_faults, bitness, commandline, "current_Working_Directory", open_Files, parent_Process_ID, thread_count, uptime, process_count_difference)
            VALUES %s
        """
        psycopg2.extras.execute_values(cursor, application_data_query, applications)

        connections = []
        for index, row in df_dict["connection"].iterrows():
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
            VALUES %s
        """
        psycopg2.extras.execute_values(cursor, connection_data_query, connections)

        # Assuming you have imported the required libraries and established a connection to the database

        network_interfaces = []
        for index, row in df_dict["network"].iterrows():
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
            VALUES %s
        """
        psycopg2.extras.execute_values(cursor, network_interface_data_query, network_interfaces)

        conn.commit()
        return pcdata_id
    except Exception as e:
        conn.rollback()
        raise e


def get_moving_avg_of_total_ram(pc_id: int, application): # returns moving avg of the last 5 columns
    moving_avg_query = """
    SELECT
    AVG(app.ram) OVER (ORDER BY app.measurement_time ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_ram
    FROM
    applicationdata AS app
    JOIN
    pcdata AS pc ON app.pcdata_id = pc.id
    WHERE
    pc.pc_id = %s AND app.name = %s
    ORDER BY
    app.measurement_time;
    """

    cursor.execute(moving_avg_query, (pc_id, application))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return 0
