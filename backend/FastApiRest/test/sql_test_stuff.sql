
INSERT INTO pcdata (state_id, pc_id, measurement_time, free_disk_space, read_bytes_disks, reads_disks, write_bytes_disks, writes_disks, partition_major_faults, partition_minor_faults, available_memory, names_power_source, charging_power_sources, discharging_power_sources, power_online_power_sources, remaining_capacity_percent_power_sources, context_switches_processor, interrupts_processor, cpu, ram, context_switches, major_faults, open_files, thread_count) VALUES (1, 1, '2023-09-29 17:29:20.280000', 832019019776, 12638135808, 293445, 8617013248, 240684, 0, 1, 15849578496, 'System Battery', false, false, true, 1, 81441349, 52147359, 0.8, 12599134196, 0, 0, 134832, 7000);

select * from pcdata;
select measurement_time, ram, cpu from applicationdata where name='java';

select * from applicationdata where measurement_time <= '2023-09-29T17:29:20.280000' and name='chrome';

INSERT INTO applicationdata (pcdata_id, pc_id, measurement_time, name, path, cpu, ram, state, "user", process_count_difference) VALUES (61, 1, '2023-09-29 17:29:20.280000', 'chrome', 'iwos', 0.1, 10000000, 'RUNNING', 'sarah', 0)


select * from pcstate where measurement_time=(select MAX(measurement_time) from pcstate);

select * from anomaly;

select * from applicationdata;

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
            pc_id = 1 AND
            name = 'chrome'
        ORDER BY
            measurement_time;

SELECT * from anomaly;

DELETE FROM anomaly where user_id=1;

INSERT INTO anomaly (user_id, type, severity_level, message, condition) VALUES (
    1,
    'RAM Threshold',
    5,
    'PC is using more than 90% RAM',
    '[
            {
                "combined_conditions": null,
                "percentage_trigger_value": 0.9,
                "absolute_trigger_value": null,
                "operator": ">",
                "column": "ram",
                "application": null,
                "detect_via_moving_averages": true
            }
        ]'
);

INSERT INTO anomaly (user_id, type, severity_level, message, condition) VALUES (
    1,
    'RAM Threshold done stupid',
    5,
    'PC is using more than 5% RAM',
    '[
            {
                "combined_conditions": null,
                "percentage_trigger_value": 0.05,
                "absolute_trigger_value": null,
                "operator": ">",
                "column": "ram",
                "application": null,
                "detect_via_moving_averages": false
            }
        ]'
);

INSERT INTO anomaly (user_id, type, severity_level, message, condition) VALUES (
    1,
    'RAM Threshold fixed',
    5,
    'PC is using more 5GB RAM',
    '[
            {
                "combined_conditions": null,
                "percentage_trigger_value": null,
                "absolute_trigger_value": 5368709120,
                "operator": ">",
                "column": "ram",
                "application": null,
                "detect_via_moving_averages": true
            }
        ]'
);

INSERT INTO anomaly (user_id, type, severity_level, message, condition) VALUES (
    1,
    'CPU Threshold for Chrome',
    5,
    'Chrome is using more than 5% CPU',
    '[
            {
                "combined_conditions": null,
                "percentage_trigger_value": 0.05,
                "absolute_trigger_value": 0.05,
                "operator": ">",
                "column": "cpu",
                "application": "chrome",
                "detect_via_moving_averages": true
            }
        ]'
);

INSERT INTO anomaly (user_id, type, severity_level, message, condition) VALUES (
    1,
    'CPU Threshold done stupid',
    5,
    'PC is using more than 5% CPU',
    '[
            {
                "combined_conditions": null,
                "percentage_trigger_value": 0.05,
                "absolute_trigger_value": null,
                "operator": ">",
                "column": "cpu",
                "application": null,
                "detect_via_moving_averages": false
            }
        ]'
);

INSERT INTO anomaly (user_id, type, severity_level, message, condition) VALUES (
    1,
    'CPU Threshold done stupid',
    5,
    'PC is using less than 99% CPU',
    '[
            {
                "combined_conditions": null,
                "percentage_trigger_value": 0.99,
                "absolute_trigger_value": null,
                "operator": "<",
                "column": "cpu",
                "application": null,
                "detect_via_moving_averages": false
            }
        ]'
);