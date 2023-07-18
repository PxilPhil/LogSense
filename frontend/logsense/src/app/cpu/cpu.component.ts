import { Component, OnInit } from '@angular/core';
import {Chart} from "chart.js";
import _default from "chart.js/dist/plugins/plugin.legend";
import labels = _default.defaults.labels;

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
@Component({
  selector: 'app-cpu',
  templateUrl: './cpu.component.html',
  styleUrls: ['./cpu.component.scss']
})
export class CpuComponent implements OnInit{

  cpu: CPUModel = new CPUModel();
  average: number = 21;
  current: number = 48;
  stability: String = "Low";
  selectedTime: String = "Last 24h";
  notes: String[] = ["CPU Usage dropped 4%", "21 Anomalies detected", "5 Events registered"]
  constructor() {
  }
  ngOnInit() {
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

  getData(): { labels: string[], values: number[] } {
    const labels = ['Zeitpunkt 1', 'Zeitpunkt 2', 'Zeitpunkt 3']; // Beispiellabels
    const values = [75, 90, 60]; // Beispielauslastung
    return { labels, values };
  }
}
