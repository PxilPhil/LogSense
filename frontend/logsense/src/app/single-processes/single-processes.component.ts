import {Component, OnDestroy, OnInit} from '@angular/core';
import {Chart} from "chart.js";
import {ApplicationService} from "../services/application.service";
import {ApplicationNames} from "../model/ApplicationNames";
import {DatePipe} from "@angular/common";
import {Application, ApplicationTimeSeriesData} from "../model/Application";
import {AlertService} from "../services/alert.service";
import {Alert} from "../model/Alert";
import {SelectedPcService} from "../services/selected-pc.service";

export class ChartData {
  measurementTime: string[] = [];
  usage: number[] = [];
}
@Component({
  selector: 'app-single-processes',
  templateUrl: './single-processes.component.html',
  styleUrls: ['./single-processes.component.scss']
})
export class SingleProcessesComponent implements OnInit, OnDestroy {
  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];
  selectedTime = this.times[0];

  applicationNameList: ApplicationNames = new ApplicationNames();
  selectedApplication: Application = new Application();

  //latestApplicationMeasurement: ApplicationTimeSeriesData = new ApplicationTimeSeriesData();
  statistics: string[] = ["CPU Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Rise of RAM usage of 90% detected"];
  alerts: Alert[] = [];
  isApplicationSelected = false;
  cpuChart: Chart | undefined;
  ramChart: Chart | undefined;
  displayedApps: string[] = [];
  runningApps: string[] = [];
  searchCriteria: string = "";
  cpuData: ChartData = {measurementTime: [], usage: []};
  ramData: ChartData = {measurementTime: [], usage: []};

  checkedCPU: String = "";
  checkedRAM: String = "";
  radioOptions: String[] = ["Show None", "Show Anomalies", "Show Events and Anomalies"];


  pcId: number = 0;
  showPcIdAlert: boolean = true;

  constructor(private applicationService: ApplicationService, private alertService: AlertService, private selectedPcService: SelectedPcService, private datePipe: DatePipe) {
  }

  ngOnInit() {
    this.getSelectedPcId();
    this.loadApplicationNameList();
    this.loadAlerts();
  }

  ngOnDestroy() {
    if (this.cpuChart) {
      this.cpuChart.destroy();
    }

    if (this.ramChart) {
      this.ramChart.destroy();
    }
  }

  setData(): void {
    this.cpuData = this.getCpuData();
    this.ramData = this.getRamData();
  }

  loadApplicationNameList(): void {
    this.runningApps = [];
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds!=0) {
      this.applicationService.getApplicationNameList(this.pcId, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds == 0 ? dateNow : dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: ApplicationNames) => {
        this.applicationNameList = data;
        for (let app of this.applicationNameList.application_list) {
          this.runningApps.push(app);
        }
        this.displayedApps = this.applicationNameList.application_list;
        this.loadApplicationData(this.displayedApps[0]);
      });
    } else {
      this.applicationService.getApplicationNameList(this.pcId, this.datePipe.transform(dateNow-dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: ApplicationNames) => {
        this.applicationNameList = data;
        for (let app of this.applicationNameList.application_list) {
          this.runningApps.push(app);
        }
        this.displayedApps = this.applicationNameList.application_list;
        this.loadApplicationData(this.displayedApps[0]);
      });
    }
  }

  filterApplicationNameList(): void {
    console.log("d\n" + this.displayedApps);
    console.log("r\n" + this.runningApps);
    this.displayedApps = this.runningApps;
    console.log("d\n" + this.displayedApps);
    let tmp: string[] = [];
    for (let app of this.displayedApps) {
      if(app.toLowerCase().includes(this.searchCriteria.toLowerCase())) {
        tmp.push(app);
      }
    }
    console.log("t\n" + tmp);
    this.displayedApps = tmp;
  }


  /*
  loadAlerts(): void {
    this.alertService.getAlerts().subscribe((data: Alert[]) => {
      //this.alerts = data;
    });
  }
  */

  loadApplicationData(applicationName: string): void {
    this.isApplicationSelected = true;
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds != 0) {
      this.applicationService.getApplicationByApplicationName(1, applicationName, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds == 0 ? dateNow : dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", 5).subscribe((data: Application) => {
        this.selectedApplication = data;
        console.log(data);
        //this.latestApplicationMeasurement = this.getLatestApplicationMeasurementOfSelectedApplication();
        this.setData();
        this.cpuUsageChart();
        this.ramUsageChart();
        this.loadAlerts();

      });
    } else {
      this.applicationService.getApplicationByApplicationName(1, applicationName, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", 5).subscribe((data: Application) => {
        this.selectedApplication = data;
        console.log(data);
        //this.latestApplicationMeasurement = this.getLatestApplicationMeasurementOfSelectedApplication();
        this.setData();
        this.cpuUsageChart();
        this.ramUsageChart();
        this.loadAlerts();

      });
    }

  }

  reloadApplicationDataOnTimesSelectionChange() {
    this.loadApplicationNameList();
    this.loadApplicationData(this.selectedApplication.application_name);
  }

  getLatestApplicationMeasurementOfSelectedApplication(): ApplicationTimeSeriesData {
    if (this.selectedApplication.time_series_data.length > 0) {
      return this.selectedApplication.time_series_data.reduce((previous, current) => {
        return (current.measurement_time > previous.measurement_time) ? current : previous;
      });
    }
    return new ApplicationTimeSeriesData();
  }

  reloadCPUChart() {
    switch (this.checkedCPU) {
      case this.radioOptions[1]: {
        this.showAnomalyCPUChart();
        break;
      }
      case this.radioOptions[2]: {
        this.showAllCPUChart();
        break;
      }
      default: {
        this.cpuUsageChart();
        break;
      }
    }
  }
  reloadRAMChart() {
    switch (this.checkedRAM) {
      case this.radioOptions[1]: {
        this.showAnomalyRAMChart();
        break;
      }
      case this.radioOptions[2]: {
        this.showAllRAMChart();
        break;
      }
      default: {
        this.ramUsageChart();
        break;
      }
    }
  }

  showAllCPUChart(): void {

  }

  showAllRAMChart(): void {

  }
  showAnomalyCPUChart(): void {

  }
  showAnomalyRAMChart(): void {

  }


  cpuUsageChart(): void {
    if (this.cpuChart) {
      this.cpuChart.destroy();
    }

    this.cpuChart = new Chart("usageCPU", {
      type: "line",
      data: {
        labels: this.cpuData.measurementTime,
        datasets: [{
          data: this.cpuData.usage,
          borderColor: "#3e95cd",
          fill: false
        }]
      }, options: {
        maintainAspectRatio: false,
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            display: false
          }, tooltip: {
            callbacks: {
              label: function (context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ' ';
                }
                label += context.parsed.y + '%';
                return label;
              }
            }
          }
        }
      },
    });
  }

  ramUsageChart(): void {
    if (this.ramChart) {
      this.ramChart.destroy();
    }

    this.ramChart = new Chart("usageRAM", {
      type: "line",
      data: {
        labels: this.ramData.measurementTime,
        datasets: [{
          data: this.ramData.usage,
          borderColor: "#3e95cd",
          fill: false
        }]
      }, options: {
        maintainAspectRatio: false,
        responsive: true,
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
                label += context.parsed.y + ' MB';
                return label;
              }
            }
          }
        }
      },
    });
  }

  getCpuData(): ChartData {
    let data: ChartData = {measurementTime: [], usage: []};
    this.selectedApplication.time_series_data.forEach(cpuUsageMeasurement => {
      data.measurementTime.push(this.datePipe.transform(cpuUsageMeasurement.measurement_time, 'MM-dd HH:mm') ?? "");
      //console.log(cpuUsageMeasurement.cpu);
      data.usage.push(this.roundDecimalNumber(cpuUsageMeasurement.cpu*100, 3));
    });
    //console.log(data);
    return data;
  }

  getRamData(): ChartData {
    let data: ChartData = {measurementTime: [], usage: []};
    this.selectedApplication.time_series_data.forEach(ramUsageMeasurement => {
      data.measurementTime.push(this.datePipe.transform(ramUsageMeasurement.measurement_time, 'MM-dd HH:mm') ?? "");
      data.usage.push(this.roundDecimalNumber(this.convertBytesToMegaBytes(ramUsageMeasurement.ram), 2));
    });
    return data;
  }

  formatUpTime(upTime: number): string {
    const date = new Date(upTime);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    return `${hours} hours, ${minutes} minutes and ${seconds} seconds`;
  }

  convertBytesToMegaBytes(valueInBytes: number): number {
    return (valueInBytes / 1000 / 1000);
  }

  roundDecimalNumber(decimalNumber: number, places: number): number {
    return Math.round((decimalNumber + Number.EPSILON) * Math.pow(10, places)) / Math.pow(10, places);
  }

  loadAlerts() {
    //is it fine to just get data like this?
    console.log(this.selectedApplication.application_name)
    this.alerts = this.alertService.getStoredAlerts(this.selectedApplication.application_name, undefined);
  }

  protected readonly onchange = onchange;

  getSelectedPcId() {
    if (this.selectedPcService.getSelectedPcId() != null) {
      this.pcId = this.selectedPcService.getSelectedPcId()!;
      this.showPcIdAlert = false;
    } else {
      this.showPcIdAlert = true;
    }
  }
}

