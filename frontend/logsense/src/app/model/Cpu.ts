import {PCTimeSeriesData} from "./PCData";

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
