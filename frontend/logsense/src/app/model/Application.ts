export class Application {
  pc: number = 0;
  application_name: string = "";
  standard_deviation_ram: number = 0;
  standard_deviation_cpu: number = 0;
  mean_ram: number = 0;
  mean_cpu: number = 0;
  time_series_data: ApplicationTimeSeriesData[] = [];
  event_list: [
    {
      timestamp: Date;
      anomaly_type: number;
      change: number;
      application: string;
      column: string;
    }
  ] = [
    {
      timestamp: new Date(), anomaly_type: 0, change: 0, application: "", column: ""
    }
  ];
  anomaly_list: [
    {
      timestamp: Date;
      severity: number;
      application: string;
      column: string
    }
  ] = [
    {
      timestamp: new Date(), severity: 0, application: "", column: ""
    }
  ];
}

export class ApplicationTimeSeriesData {
  id: number = 0;
  pcdata_id: number = 0;
  measurement_time: Date = new Date();
  name: string = "";
  path: string = "";
  cpu: number = 0;
  ram: number = 0;
  state: string = "";
  user: string = "";
  context_switches: number = 0;
  major_faults: number = 0;
  bitness: number = 0;
  commandLine: string = "";
  current_Working_Directory: string = "";
  open_files: number = 0;
  parent_process_id: number = 0;
  thread_count: number = 0;
  uptime: number = 0;
  process_count_difference: number = 0;
  rolling_avg_ram: number = 0;
  rolling_avg_cpu: number = 0;
}
