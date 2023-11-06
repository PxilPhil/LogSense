import {EventData, Process, StatisticData} from "./PCData";
import {TimeMetrics} from "./TimeMetrics";

export class Application {
  pc: number = 0;
  application_name: string = "";
  time_series_data: ApplicationTimeSeriesData[] = [];
  cpu_events_and_anomalies: EventData[] = [];
  ram_events_and_anomalies: EventData[] = [];
  cpu_statistic_data: StatisticData = new StatisticData();
  ram_statistic_data: StatisticData = new StatisticData();
  run_time_in_seconds: AppTime = new AppTime();
  info: ApplicationInfo = new ApplicationInfo();
}

export class AppTime {
  name: string = "";
  total_running_time_seconds: number = 0;
}
export class ApplicationTimeSeriesData {
  measurement_time: string = "";
  cpu: number = 0;
  ram: number = 0;
}

export class ApplicationInfo {
  process_id: number = 0;
  path: string = "";
  working_directory: string = "";
  command_line: string = "";
  windows_user_name: string = "";
  bitness: number = 0;
  state: string = "";
  major_faults: number = 0;
  context_switches: number = 0;
  threads: number = 0;
  open_files: number = 0;
}
