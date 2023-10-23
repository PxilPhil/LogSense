export class ResourceMetricsModel {
  cpu_percentage_use: number = 0; //%
  processor_name: string = "";
  physical_package_count: number = 0;
  physical_processor_count: number = 0;
  logical_processor_count: number = 0;
  ram_percentage_in_use: number = 0; //%
  total_memory: number = 0; //Byte
  free_memory: number = 0; //Byte
  page_size: number = 0;
  disk_percentage_in_use: number = 0; //%
  total_disk_space: number = 0; //Byte
  free_disk_space: number = 0; //Byte
}
