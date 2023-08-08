import { Component, OnInit } from '@angular/core';
import {Chart} from "chart.js";
import {MatDialog} from "@angular/material/dialog";
import {PartDialogComponent} from "../part-dialog/part-dialog.component";
import {DiskDataService} from "../services/disk.service";
import {DiskData} from "../model/DiskData";
import {Alert} from "../model/Alert";
import {AlertService} from "../services/alert.service";

export interface TimeModel {
  id: Number;
  time: String;
  valueInMilliseconds: number;
}

@Component({
  selector: 'app-disk',
  templateUrl: './disk.component.html',
  styleUrls: ['./disk.component.scss']
})
export class DiskComponent implements OnInit{
  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];
  selectedTime = this.times[0];
  diskData: DiskData = new DiskData();
  statistics: String[] = ["Disk usage dropped 4%", "21 anomalies detected", "5 Events registered",  "Recent Rise of 15% detected"];
  alerts: Alert[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];

  constructor(public dialog: MatDialog, private diskDataService: DiskDataService, private alertService: AlertService) {
  }

  ngOnInit() {
    this.loadDiskData();
    //this.loadAlerts()   //TODO: insert again when endpoint is implemented
    this.usageChart();
  }

  loadDiskData() {
    this.diskDataService.getDiskData(1 /* TODO get dynamic pc id */).subscribe((data: DiskData) => {
      this.diskData = data;
      console.log(JSON.stringify(this.diskData));
    });
  }

  loadAlerts(): void {
    this.alertService.getAlerts().subscribe((data: Alert[]) => {
      this.alerts = data;
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

  openDialog(diskListIndex: number) {
    this.dialog.open(PartDialogComponent, {
      data: this.diskData.disks.at(diskListIndex)!.partitions
    });
  }
}
