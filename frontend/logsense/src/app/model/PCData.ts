import { TimeSeriesData } from "./TimeSeriesData";

  export interface PCDataResponse {
    pc_id: number;
    type: string;
    start: string;
    end: string;
    standard_deviation: number;
    mean: number;
    time_series_list: TimeSeriesData[];
    allocation_map: {
      name: string;
      allocation: number;
    }[];
  }