export interface TimeSeriesData {
    id: number;
    state_id: number;
    pc_id: number;
    measurement_time: string;
    free_disk_space: number;
    read_bytes_disks: number;
    reads_disks: number;
    write_bytes_disks: number;
    writes_disks: number;
    partition_major_faults: number;
    partition_minor_faults: number;
    available_memory: number;
    names_power_source: string;
    charging_power_sources: boolean;
    discharging_power_sources: boolean;
    power_online_power_sources: boolean;
    remaining_capacity_percent_power_sources: number;
    context_switches_processor: number;
    interrupts_processor: number;
    ram: number;
    context_switches: number;
    major_faults: number;
    open_files: number;
    thread_count: number;
  }