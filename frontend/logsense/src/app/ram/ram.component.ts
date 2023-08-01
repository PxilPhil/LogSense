import { Component, OnInit } from '@angular/core';
import {Process} from "../single-processes/single-processes.component";
import {ProcessModel} from "../cpu/cpu.component";
import {Chart} from "chart.js";

export class RAMModel {
  totalMemory: Number = 17.02; //GB
  freeMemory: Number = 12.02; //GB
  pageSize: Number = 4.096; //KB
  current: Number = 21; //%
  average: Number = 48; //%
  stability: String = "Low";
  stats: String[] = ["RAM Usage dropped 4%", "21 anomalies detected", "5 Events registered",  "Recent Rise of 15% detected"];
  processes: ProcessModel[] = [{name: "Chrome", allocation: 15}, {name: "Explorer", allocation: 10},{name: "Intellij", allocation: 48}];
  alerts: String[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];
}
@Component({
  selector: 'app-ram',
  templateUrl: './ram.component.html',
  styleUrls: ['./ram.component.scss']
})
export class RamComponent implements OnInit {
  ram: RAMModel = new RAMModel();
  selectedTime: String = "Last 24h";
  times = [
    {id: 1, time: "Last 24h"},
    {id: 2, time: "Last Week"},
    {id: 3, time: "Last Month"},
    {id: 4, time: "Last 6 Months"},
    {id: 5, time: "Last 12 Months"},
    {id: 6, time: "All Time"}
  ];

  ngOnInit() {
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

  getData(): { labels: string[], values: number[] } {
    const labels = ['Zeitpunkt 1', 'Zeitpunkt 2', 'Zeitpunkt 3']; // Beispiellabels
    const values = [75, 90, 60]; // Beispielauslastung
    return { labels, values };
  }
}
