export class CpuData {
  disks: DiskStore[] = [];
}

export class DiskStore {
  id: number = 0;
  cpuName: String = "AMD Ryzen 7 5800H";
  identifier: String = "Intel64 Family 6 Model 165 Stepping 2";
  processorID: String = "BFEBFBFF000A0652";
  vendor: String = "GenuineIntel";
  bitness: String = "64 Bit";
  physicalPackages: Number = 1;
  physicalProcessors: Number = 6;
  logicalProcessors: Number = 12;
  contextSwitches: String = "230431317";
  interrupts: String = "185631654";
  current: Number = 21; //%
  average: Number = 48; //%
  stability: String = "Low";
}

