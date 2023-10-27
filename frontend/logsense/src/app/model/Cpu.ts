import {EventData, PCTimeSeriesData, Process, StatisticData, TimeSeriesData} from "./PCData";

export class CPUGeneral {
  processor_name: string = "";
  processor_identifier: string = "";
  processor_id: string = "";
  processor_vendor: string = "";
  processor_bitness: number = 0;
  physical_package_count: number = 0;
  physical_processor_count: number = 0;
  logical_processor_count: number = 0;
  context_switches: number = 0;
  interrupts: number = 0;
}

export class CPUStats {
  mean_cpu: number = 0;
  stability_cpu: string = "";
  cur_cpu: number = 0;
}

export class CPUModel {
  pc_id: number = 0;
  start: string = "";
  end: string = "";
  time_series_list: TimeSeriesData[] = [];
  allocation_list: Process[] = [];
  events_and_anomalies: EventData[] = [];
  statistic_data: StatisticData = new StatisticData();
}
