import {Component, OnInit} from '@angular/core';
import {ProcessModel} from "../cpu/cpu.component";
import {Chart} from "chart.js";
import {TimeModel} from "../disk/disk.component";
import {PCData} from "../model/PCData";
import {PCDataService} from "../services/pc-data.service";
import {DatePipe} from "@angular/common";
import {RamStats} from "../model/Ram";
import {ResourceMetricsService} from "../services/resource-metrics.service";

export class RAMModel {
  totalMemory: Number = 17.02; //GB
  freeMemory: Number = 12.02; //GB
  pageSize: Number = 4.096; //KB
  current: Number = 21; //%
  average: Number = 48; //%
  stability: String = "Low";
  stats: String[] = ["RAM Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Recent Rise of 15% detected"];
  processes: ProcessModel[] = [{name: "Chrome", allocation: 15}, {name: "Explorer", allocation: 10}, {
    name: "Intellij",
    allocation: 48
  }];
  alerts: String[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];
}

@Component({
  selector: 'app-ram',
  templateUrl: './ram.component.html',
  styleUrls: ['./ram.component.scss']
})
export class RamComponent implements OnInit {
  ram: RAMModel = new RAMModel();

  ramStats: RamStats = new RamStats();
  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];
  selectedTime: TimeModel = this.times[0];

  constructor(private pcDataService: PCDataService, private  datePipe: DatePipe, private resourceService: ResourceMetricsService) {
  }

  ngOnInit() {
    this.loadStats() // TODO: soboids den API Call gibt Stats lodn
    this.usageChart();
  }

  usageChart(): void {
    const data = this.getData();
    const usage = new Chart("ram", {
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

  loadStats() {
    /*let pcData: PCData = new PCData();
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds != 0) {
      this.pcDataService.getPcData(1, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: PCData) => {
        pcData = data;
        this.ramStats.stability = pcData.stability_ram;
      });
      //this.resourceService.getResourceMetrics(1)
    }*/
  }
  getData(): { labels: string[], values: number[] } {
    const labels = ['Zeitpunkt 1', 'Zeitpunkt 2', 'Zeitpunkt 3']; // Beispiellabels
    const values = [75, 90, 60]; // Beispielauslastung
    return {labels, values};
  }
}
