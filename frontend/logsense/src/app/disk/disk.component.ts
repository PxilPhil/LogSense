import {Component, OnDestroy, OnInit} from '@angular/core';
import {Chart} from "chart.js";
import {MatDialog} from "@angular/material/dialog";
import {PartDialogComponent} from "../part-dialog/part-dialog.component";
import {DiskDataService} from "../services/disk.service";
import {DiskData} from "../model/DiskData";
import {Alert} from "../model/Alert";
import {AlertService} from "../services/alert.service";
import {PCDataService} from "../services/pc-data.service";
import {PCData, PCTimeSeriesData, TimeSeriesData} from "../model/PCData";
import {DatePipe} from "@angular/common";
import {ChartData} from "../ram/ram.component";
import {SelectedPcService} from "../services/selected-pc.service";

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
  diskChartData: ChartData = new ChartData();
  diskTotal: string = "platzhalter"; // TODO
  diskFree: string = "platzhalter";


  statistics: String[] = ["Disk usage dropped 4%", "21 anomalies detected", "5 Events registered", "Recent Rise of 15% detected"];
  alerts: Alert[] = [];

  isShowEventsChecked: boolean = true;
  isShowAnomaliesChecked: boolean = true;
  isShowPredictionsChecked: boolean = false;

  pcId: number = 0;
  showPcIdAlert: boolean = true;

  constructor(public dialog: MatDialog, private diskDataService: DiskDataService, private pcDataService: PCDataService, private alertService: AlertService, private selectedPcService: SelectedPcService, private datePipe: DatePipe) {
    this.loadDiskData();  //only load diskStores and partitions on startup or on refresh
  }

  ngOnInit() {
    this.getSelectedPcId();
    this.loadPCData();
    this.loadAlerts();
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
    this.diskDataService.getDiskData(this.pcId).subscribe((data: DiskData) => {
      this.diskData = data;
    });
  }

  loadPCData() {
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds == 0) {
      this.diskDataService.getDiskTimeseriesData(this.pcId, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: TimeSeriesData[]) => {
        this.diskData.time_series_data = data;
        this.transformData();
        //this.latestPCDataMeasurement = this.getLatestPCDataMeasurement();
        this.diskUsageChart();
      });
    } else {
      this.diskDataService.getDiskTimeseriesData(this.pcId, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds == 0 ? dateNow : dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: TimeSeriesData[]) => {
        this.diskData.time_series_data = data;
        this.transformData();
        //this.latestPCDataMeasurement = this.getLatestPCDataMeasurement();
        this.diskUsageChart();
      });
    }
  }
  transformData() {
    this.diskChartData.time = [];
    this.diskChartData.value = [];
    for (let dataPoint of this.diskData.time_series_data) {;
      this.diskChartData.time.push(this.datePipe.transform(dataPoint.measurement_time, 'MM-dd HH:mm:ss')??"");
      this.diskChartData.value.push(this.convertBytesToGigaBytes(dataPoint.value));
    }
  }
  /*getLatestPCDataMeasurement(): PCTimeSeriesData {
    if (this.pcData.time_series_list.length > 0) {
      return this.pcData.time_series_list.reduce((previous, current) => {
        return (current.measurement_time > previous.measurement_time) ? current : previous;
      });
    }
    return new PCTimeSeriesData();
  }
*/
  /*
  loadAlerts(): void {
    this.alertService.getAlerts().subscribe((data: Alert[]) => {
      //this.alerts = data;
    });
  }
  */

  diskUsageChart(): void {
    console.log(this.pcData);
    if (this.diskChart) {
      this.diskChart.destroy();
    }
    this.diskChart = new Chart("disk", {
      type: "line",
      data: {
        labels: this.diskChartData.time,
        datasets: [{
          data: this.diskChartData.value,
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

  loadAlerts() {
    //is it fine to just get data like this?
    this.alerts = this.alertService.getStoredAlerts(undefined, ['free_disk_space', 'read_bytes_disk', 'reads_disks', 'write_bytes_disks', 'writes_disks']);
  }

  getSelectedPcId() {
    if (this.selectedPcService.getSelectedPcId() != null) {
      this.pcId = this.selectedPcService.getSelectedPcId()!;
      this.showPcIdAlert = false;
    } else {
      this.showPcIdAlert = true;
    }
  }
}
