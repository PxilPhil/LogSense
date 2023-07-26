from datetime import datetime

import psycopg2

from data_analytics import anomaly
from db_access import cursor, conn
from psycopg2 import extras

from model.data import runningPCData


def insert_pcdata(pc_total_df, application_df, anomalies):
    try:
        first_row_pc_total = pc_total_df.iloc[0]
        #first_row_pc = pc_df.iloc[0]
        pcdata_id = 0

        """
        pcdata_values = (
                            row[measurement_time],
                            pcdata.free_disk_space,
                            pcdata.partition_major_faults,
                            pcdata.partition_minor_faults,
                            pcdata.available_memory,
                            pcdata.names_power_source,
                            pcdata.discharging_power_sources,
                            pcdata.power_online_power_sources,
                            pcdata.remaining_capacity_percent_power_sources,
                            pcdata.context_switches_processor,
                            pcdata.interrupts_processor)

        pcdata_query = ""
            INSERT INTO pcdata (
                state_id,
                pc_id,
                measurement_time,
                free_disk_space,
                partition_major_faults,
                partition_minor_faults,
                available_memory,
                names_power_source,
                discharging_power_sources,
                power_online_power_sources,
                remaining_capacity_percent_power_sources,
                context_switches_processor,
                interrupts_processor,
                total_cpu,
                total_ram,
                total_context_switches,
                total_major_faults,
                total_minor_faults,
                total_open_files,
                total_thread_count
            ) VALUES %s RETURNING id;
        ""

        cursor.execute(pcdata_query, (pcdata_values,))
        pcdata_id = cursor.fetchone()[0]
        """

        applications =  []
        for index, row in application_df.iterrows():
            #print(index)
            #print(row[index])
            #print(row['residentSetSize'])
            timestamp = datetime.fromtimestamp(index/1000)
            application_data = (
                pcdata_id,
                timestamp,
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

        # Insert ApplicationData into 'applicationdata' table

        """        
        application_data = [(pcdata_id, app.measurement_time, app.name, app.path, app.cpu, app.ram, app.State, app.user,
                             app.context_Switches, app.major_Faults, app.bitness, app.commandline,
                             app.current_Working_Directory, app.open_Files, app.parent_ProcessID,
                             app.thread_Count, app.uptime, app.process_Count_Difference) for app in
                            pcdata.applicationdata]

        extras.execute_values(cursor, ""
        INSERT INTO applicationdata (pcdata_id, measurement_time, name, path, cpu, ram, State, "user", context_Switches,
                                    major_Faults, bitness, commandline, "current_Working_Directory", open_Files,
                                    parent_ProcessID, thread_Count, uptime, process_Count_Difference) VALUES %s;
        "", application_data)

        # Insert applicationdata_anomaly into 'applicationdata_anomaly' table
        applicationdata_anomaly_data = [(anomaly.anomaly_id, app_id) for app_id in
                                        range(pcdata_id, pcdata_id + len(pcdata.applicationdata))]

        extras.execute_values(cursor, ""
        INSERT INTO applicationdata_anomaly (anomaly_id, applicationdata_id) VALUES %s;
        "", applicationdata_anomaly_data)

        # Insert NetworkInterface into 'networkInterface' table
        network_interface_data = [(pcdata_id, net.name, net.display_name, net.ipv4_address, net.ipv6_address, net.art,
                                   net.subnet_mask, net.mac_address, net.bytes_received, net.bytes_sent,
                                   net.packets_received, net.packets_sent) for net in pcdata.networkInterface]

        extras.execute_values(cursor, ""
        INSERT INTO networkInterface (pcdata_id, name, display_name, ipv4_address, ipv6_address, art, subnet_mask, mac_address,
                                      bytes_received, bytes_sent, packets_received, packets_sent) VALUES %s;
        "", network_interface_data)
        """

        conn.commit()
        return pcdata_id
    except Exception as e:
        conn.rollback()
        raise e
