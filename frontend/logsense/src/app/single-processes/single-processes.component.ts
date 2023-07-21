import { Component } from '@angular/core';

export class Process {
  name:String = "Chrome";
  processID: String = "5136";
  path: String = "C:\\Windows\\System\\chrome.exe";
  workingDirectory: String = "C:\\WINDOWS\\sytem32\\";
  cmdLn: String = "C:\\etc...";
  parentProcessID: String = "1148";
  user: String = "sarah";
  bitness: Number = 64; //Bit
  cpuAverage: Number = 24;//%
  ramAverage: Number = 45;//%
  runtime: Number = 69; //min?
  majorFaults: Number = 0;
  minorFaults: Number = 28177;
  contextSwitches: Number = 0;
  threads: Number = 4;
  openFiles: Number = 489;
  statistics: String[] = ["CPU Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Rise of RAM usage of 90% detected"];
  alerts: String[] = ["Abnormal RAM-Spikes detected", "Memory leak possible"];
}

@Component({
  selector: 'app-single-processes',
  templateUrl: './single-processes.component.html',
  styleUrls: ['./single-processes.component.scss']
})
export class SingleProcessesComponent {
    tmpPro: Process = new Process();
    tmpProcesses: Process[] = [
      {name: "Chrome", processID: "5136", path: "C:\\Windows\\System\\chrome.exe", workingDirectory: "C:\\WINDOWS\\sytem32\\", cmdLn: "C:\\etc...", parentProcessID: "1148", user: "sarah", bitness: 64, cpuAverage: 24, ramAverage: 45, runtime: 69, majorFaults: 0, minorFaults: 28177, contextSwitches: 0, threads: 4, openFiles: 489, statistics: ["CPU Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Rise of RAM usage of 90% detected"], alerts: ["Abnormal RAM-Spikes detected", "Memory leak possible"]},
      {name: "Vmmem", processID: "1456", path: "C:\\Windows\\System\\svchost.exe", workingDirectory: "C:\\WINDOWS\\sytem32\\", cmdLn: "C:\\etc...", parentProcessID: "1148", user: "sarah", bitness: 64, cpuAverage: 24, ramAverage: 45, runtime: 69, majorFaults: 0, minorFaults: 28177, contextSwitches: 0, threads: 4, openFiles: 489, statistics: ["CPU Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Rise of RAM usage of 90% detected"], alerts: ["Abnormal RAM-Spikes detected", "Memory leak possible"]},
      {name: "Chrome", processID: "5136", path: "C:\\Windows\\System\\chrome.exe", workingDirectory: "C:\\WINDOWS\\sytem32\\", cmdLn: "C:\\etc...", parentProcessID: "1148", user: "sarah", bitness: 64, cpuAverage: 24, ramAverage: 45, runtime: 69, majorFaults: 0, minorFaults: 28177, contextSwitches: 0, threads: 4, openFiles: 489, statistics: ["CPU Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Rise of RAM usage of 90% detected"], alerts: ["Abnormal RAM-Spikes detected", "Memory leak possible"]},
      {name: "Vmmem", processID: "1456", path: "C:\\Windows\\System\\svchost.exe", workingDirectory: "C:\\WINDOWS\\sytem32\\", cmdLn: "C:\\etc...", parentProcessID: "1148", user: "sarah", bitness: 64, cpuAverage: 24, ramAverage: 45, runtime: 69, majorFaults: 0, minorFaults: 28177, contextSwitches: 0, threads: 4, openFiles: 489, statistics: ["CPU Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Rise of RAM usage of 90% detected"], alerts: ["Abnormal RAM-Spikes detected", "Memory leak possible"]}
    ];
    selectedProcess: Process = new Process();
}
