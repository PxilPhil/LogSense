import {EventData, EventList, Process, ProcessList, StatisticData, TimeSeriesData, TimeSeriesList} from "./PCData";

export class RamStats {
    cur: number = 0;
    avg: number = 0;
    stability: string = "";
    total: number = 0;
    free: number = 0;
    page: number = 0;
}

export class RAMModel {
  pc_id: number = 0;
  start: string = "";
  end: string = "";
  time_series_list: TimeSeriesData[] = [];
  allocation_list: Process[] = [];
  events_and_anomalies: EventData[] = [];
  statistic_data: StatisticData = new StatisticData();
}
