import {Component, OnInit} from '@angular/core';
import {Chart} from "chart.js";
import {CPUGeneral, CPUStats} from "../model/Cpu";
import {CpuService} from "../services/cpu.service";
import {PCDataService} from "../services/pc-data.service";
import {DatePipe} from "@angular/common";
import {PCData} from "../model/PCData";

export class CPUModel {
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

export class ProcessModel {
  name: String = "chrome";
  allocation: Number = 15;
}

@Component({
  selector: 'app-cpu',
  templateUrl: './cpu.component.html',
  styleUrls: ['./cpu.component.scss']
})
export class CpuComponent implements OnInit {
  //cpu: CPUModel = new CPUModel();
  cpuGeneral: CPUGeneral = new CPUGeneral();
  cpuStats: CPUStats = new CPUStats();
  notes: String[] = ["CPU Usage dropped 4%", "21 Anomalies detected", "5 Events registered"];
  processes: ProcessModel[] = [{name: "Chrome", allocation: 15}, {name: "Explorer", allocation: 10}, {
    name: "Intellij",
    allocation: 48
  }];
  alerts: String[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];
  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];
  selectedTime = this.times[0];

  constructor(private cpuService: CpuService, private pcDataService: PCDataService, private datePipe: DatePipe) {}

  ngOnInit() {
    this.loadStats();
    console.log(this.cpuStats);
    this.loadGeneralInfo();
    this.usageChart();
  }

  usageChart(): void {
    const data = this.getData();
    const usage = new Chart("usage", {
      type: "line",
      data: {
        labels: data.labels,
        datasets: [{
          data: data.values,
          borderColor: "#3e95cd",
          fill: false
        }]
      }, options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            display: false
          }
        }
      },
    });
  }

  loadGeneralInfo() {
    this.cpuService.getGeneral(1).subscribe((data: CPUGeneral) => {
      this.cpuGeneral = data;
    })
  }

  loadStats() {
    let pcData: PCData = new PCData();
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds != 0) {
      this.pcDataService.getPcData(1, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: PCData) => {
        pcData = data;
        this.cpuStats.mean_cpu = this.roundDecimal(pcData.mean_cpu, 2);
        this.cpuStats.stability_cpu = pcData.stability_cpu;
        this.cpuStats.cur_cpu = this.roundDecimal(pcData.time_series_list[0].cpu, 2);
      });
    } else {
      this.pcDataService.getPcData(1, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: PCData) => {
        pcData = data;
        this.cpuStats.mean_cpu = this.roundDecimal(pcData.mean_cpu, 2);
        this.cpuStats.stability_cpu = pcData.stability_cpu;
        this.cpuStats.cur_cpu = this.roundDecimal(pcData.time_series_list[0].cpu, 2);
      });
    }

  }

  roundDecimal(num: number, places: number): number{
    return Math.round((num + Number.EPSILON) * Math.pow(10, places)) / Math.pow(10, places);
  }
  getData(): { labels: string[], values: number[] } {
    const labels = ['Zeitpunkt 1', 'Zeitpunkt 2', 'Zeitpunkt 3']; // Beispiellabels
    const values = [75, 90, 60]; // Beispielauslastung
    return {labels, values};
  }
}
