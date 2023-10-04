import {Component, OnDestroy, OnInit} from '@angular/core';
import {Chart} from "chart.js";
import {MatDialog} from "@angular/material/dialog";
import {PartDialogComponent} from "../part-dialog/part-dialog.component";
import {DiskDataService} from "../services/disk.service";
import {DiskData} from "../model/DiskData";
import {Alert} from "../model/Alert";
import {AlertService} from "../services/alert.service";
import {PCDataService} from "../services/pc-data.service";
import {PCData, PCTimeSeriesData} from "../model/PCData";
import {DatePipe} from "@angular/common";

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
export class DiskComponent implements OnInit, OnDestroy {
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
  pcData: PCData = new PCData();
  latestPCDataMeasurement: PCTimeSeriesData = new PCTimeSeriesData();

  diskChart: Chart | undefined;
  diskTotal: string = "platzhalter"; // TODO
  diskFree: string = "platzhalter";


  statistics: String[] = ["Disk usage dropped 4%", "21 anomalies detected", "5 Events registered", "Recent Rise of 15% detected"];
  alerts: Alert[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];

  isShowEventsChecked: boolean = true;
  isShowAnomaliesChecked: boolean = true;
  isShowPredictionsChecked: boolean = false;

  constructor(public dialog: MatDialog, private diskDataService: DiskDataService, private pcDataService: PCDataService, private alertService: AlertService, private datePipe: DatePipe) {
    this.loadDiskData();  //only load diskStores and partitions on startup or on refresh
  }

  ngOnInit() {
    this.loadPCData();
    //this.loadAlerts()   //TODO: insert again when endpoint is implemented
  }

  ngOnDestroy() {
    if (this.diskChart) {
      this.diskChart.destroy();
    }
  }

  onResize(event: Event) {
    console.log(event);
  }

  loadDiskData() {
    this.diskDataService.getDiskData(1 /* TODO: get dynamic pc id */).subscribe((data: DiskData) => {
      this.diskData = data;
    });
  }

  loadPCData() {
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds == 0) {
      this.pcDataService.getPcData(1 /* TODO: get dynamic pc id */, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: PCData) => {
        this.pcData = data;
        this.latestPCDataMeasurement = this.getLatestPCDataMeasurement();
        this.diskUsageChart();
      });
    } else {
      this.pcDataService.getPcData(1 /* TODO: get dynamic pc id */, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds == 0 ? dateNow : dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: PCData) => {
        this.pcData = data;
        this.latestPCDataMeasurement = this.getLatestPCDataMeasurement();
        this.diskUsageChart();
      });
    }

  }

  getLatestPCDataMeasurement(): PCTimeSeriesData {
    if (this.pcData.time_series_list.length > 0) {
      return this.pcData.time_series_list.reduce((previous, current) => {
        return (current.measurement_time > previous.measurement_time) ? current : previous;
      });
    }
    return new PCTimeSeriesData();
  }

  loadAlerts(): void {
    this.alertService.getAlerts().subscribe((data: Alert[]) => {
      this.alerts = data;
    });
  }

  diskUsageChart(): void {
    if (this.diskChart) {
      this.diskChart.destroy();
    }
    const data = this.getDiskData();
    this.diskChart = new Chart("disk", {
      type: "line",
      data: {
        labels: data.measurementTimes,
        datasets: [{
          data: data.diskUsages,
          borderColor: "#3e95cd",
          fill: false
        }]
      }, options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ' ';
                }
                label += context.parsed.y + ' GB';
                return label;
              }
            }
          }
        }
      },
    });
  }

  getDiskData(): { measurementTimes: string[], diskUsages: number[] } {
    let measurementTimes: string[] = [];
    let diskUsages: number[] = [];
    this.pcData.time_series_list.forEach(pcDataMeasurement => {
      measurementTimes.push(this.datePipe.transform(pcDataMeasurement.measurement_time, 'MM-dd HH:mm') ?? "");
      diskUsages.push(this.roundDecimalNumber(this.convertBytesToGigaBytes(pcDataMeasurement.free_disk_space), 2));
    });
    return {measurementTimes: measurementTimes, diskUsages: diskUsages};
  }

  openDialog(diskListIndex: number) {
    this.dialog.open(PartDialogComponent, {
      data: this.diskData.disks.at(diskListIndex)!.partitions
    });
  }

  reloadChart() {
    this.diskUsageChart();
  }

  convertBytesToGigaBytes(valueInBytes: number): number {
    return (valueInBytes / 1000 / 1000 / 1000);
  }

  roundDecimalNumber(decimalNumber: number, places: number): number {
    return Math.round((decimalNumber + Number.EPSILON) * Math.pow(10, places)) / Math.pow(10, places);
  }
}
