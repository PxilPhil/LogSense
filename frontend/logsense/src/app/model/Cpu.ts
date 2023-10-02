export class CpuData {
  cpuData: Cpu[] = [];
}

export class Cpu {
  id: number = 0;
  cpuName: String = "";
  identifier: String = "";
  processorID: String = "";
  vendor: String = "";
  bitness: String = "";
  physicalPackages: Number = 0;
  physicalProcessors: Number = 0;
  logicalProcessors: Number = 0;
  contextSwitches: String = "";
  interrupts: String = "";
  current: Number = 0; //%
  average: Number = 0; //%
  stability: String = "";
}

