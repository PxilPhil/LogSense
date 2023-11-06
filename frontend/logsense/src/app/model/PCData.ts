export class TimeSeriesData {
  measurement_time: string = "";
  value: number = 0;
}

export class TimeSeriesList {
  time_series_list: TimeSeriesData[] = [];
}

export class Process {
  name: string = "";
  allocation: number = 0;
}

export class ProcessList {
  allocation_list: Process[] = [];
}

export class EventList {
  events_and_anomalies: EventData[] = [];
}
export class EventChartData {
  time: string = "";
  value: number = 0;
  msg: string = "";
}

export class EventData {
  timestamp: string = "";
  till_timestamp: string = "";
  is_anomaly: boolean = false;
  justification_message: string = "";
  statistics: StatisticData = new StatisticData();
}

export class StatisticData {
  average: number = 0;
  current: number = 0;
  stability: string = "";
  message: string = "";
}

export class PCData {
  pc_id: number = 0;
  start: string = "";
  end: string = "";
  standard_deviation_ram: number = 0;
  mean_ram: number = 0;
  standard_deviation_cpu: number = 0;
  stability_cpu: string = "";
  stability_ram: string = "";
  mean_cpu: number = 0;
  time_series_list: PCTimeSeriesData[] = [];
  allocation_list_ram: {
    name: string;
    allocation: number;
  }[] = [];
  allocation_list_cpu: {
    name: string;
    allocation: number;
  }[] = [];
  anomaly_list: {
    timestamp: Date;
    severity: number;
    application: string;
    column: string;
  }[] = [];
}

export class PCTimeSeriesData {
  id: number = 0;
  state_id: number = 0;
  pc_id: number = 0;
  measurement_time: string = "";
  free_disk_space: number = 0;
  read_bytes_disks: number = 0;
  reads_disks: number = 0;
  write_bytes_disks: number = 0;
  writes_disks: number = 0;
  partition_major_faults: number = 0;
  partition_minor_faults: number = 0;
  available_memory: number = 0;
  names_power_source: string = "";
  charging_power_sources: boolean = false;
  discharging_power_sources: boolean = false;
  power_online_power_sources: boolean = false;
  remaining_capacity_percent_power_sources: number = 0;
  context_switches_processor: number = 0;
  interrupts_processor: number = 0;
  ram: number = 0;
  cpu: number = 0;
  context_switches: number = 0;
  major_faults: number = 0;
  open_files: number = 0;
  thread_count: number = 0;
}

export class ClientDetails {
  manufacturer: string = "";
  model: string = "";
  hardware_uuid: string = "";
  system_battery: string = "";
  remaining_capacity: number = 0; //%
  charging: boolean = false;
  discharging: boolean = false;
  power_on_line: boolean = false;
}
