import {TimeSeriesData} from "./PCData";

export class DiskData {
  time_series_data: TimeSeriesData[] = [];
  disks: DiskStore[] = [];
}

export class DiskStore {
  id: number = 0;
  state_id: number = 0;
  measurement_time: Date = new Date();
  serialnumber: string = "";
  model: string = "";
  name: string = "";
  size: number = 0;
  partitions: Partition[] = [];
}

export class Partition {
  id: number = 0;
  disk_id: number = 0;
  disk_store_name: string = "";
  identification: string = "";
  name: string = "";
  type: string = "";
  mount_point = "";
  size: number = 0;
  major_faults: number = 0;
  minor_faults: number = 0;
}
