import { Component, OnInit } from '@angular/core';
import {Chart} from "chart.js";
import {MatDialog} from "@angular/material/dialog";
import {PartDialogComponent} from "../part-dialog/part-dialog.component";

export class DiskModel {
  name: String = "\\\\\\\\.\\\\PHYSICALDRIVE0";
  totalMemory: Number = 1024.204; //GB
  free: Number = 825.02; //GB
  model: String = "WDC PC SN530 SDBPNPZ-1T00-10...";
  size: Number = 1024.203; //GB
  readBytes: Number = 33780874240;
  read: Number = 2082811;
  writeBytes: Number = 27120091648;
  writes: Number = 467354;
  current: Number = 21; //%
  average: Number = 48; //%
  stability: String = "Low";
  partitions: PartitionModel[] = [
    {diskNr: 0, partNr: 1, name: "GPT: Standarddaten", type: "GPT: Standarddaten", mount: "C:\\", size: 1023.013, majorFaults: 0,minorFaults: 1},
    {diskNr: 0, partNr: 2, name: "GPT: Standarddaten", type: "GPT: Standarddaten", mount: "E:\\", size: 1023.013, majorFaults: 0, minorFaults: 2},
  ];
  stats: String[] = ["Disk usage dropped 4%", "21 anomalies detected", "5 Events registered",  "Recent Rise of 15% detected"];
  alerts: String[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];

}

export class PartitionModel {
  diskNr: Number = 0;
  partNr: Number = 1;
  name: String = "GPT: Basicdata";
  type: String = "GPT: Standarddaten"
  mount: String = "C:\\";
  size: Number = 1023.013; //GB
  majorFaults: Number = 0;
  minorFaults: Number = 1;
}
export interface TimeModel {
  id: Number;
  time: String;
}
@Component({
  selector: 'app-disk',
  templateUrl: './disk.component.html',
  styleUrls: ['./disk.component.scss']
})
export class DiskComponent implements OnInit{
  selectedTime: TimeModel = {id: 1, time: "Last 24h"};
  disk: DiskModel = new DiskModel();
  times = [
    {id: 1, time: "Last 24h"},
    {id: 2, time: "Last Week"},
    {id: 3, time: "Last Month"},
    {id: 4, time: "Last 6 Months"},
    {id: 5, time: "Last 12 Months"},
    {id: 6, time: "All Time"}
  ];

  constructor(public dialog: MatDialog) {}
  ngOnInit() {
    this.usageChart();
  }

  openDialog() {
    this.dialog.open(PartDialogComponent, {
      data: {
        partitions: this.disk.partitions
      }
    });
  }
  usageChart(): void {
    const data = this.getData();
    const usage = new Chart("disk", {
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
