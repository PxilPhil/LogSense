import {Component, OnDestroy, OnInit} from '@angular/core';
import {Chart, ChartTypeRegistry, TooltipItem} from "chart.js";
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

  bucketingTimes = [
    {id: 1, value: "1 minute"},
    {id: 2, value: "5 minutes"},
    {id: 3, value: "10 minutes"},
    {id: 4, value: "30 minutes"},
    {id: 5, value: "45 minutes"},
    {id: 6, value: "60 minutes"}
  ];
  selectedBucketingTime = this.bucketingTimes[0];

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
    this.destroyCPUChart();
    this.destroyRAMChart();
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
        if(this.isApplicationSelected) {
          this.loadApplicationData(this.selectedApplication.application_name);
        } else {
          this.loadApplicationData(this.displayedApps[0]);
        }
      });
    } else {
      this.applicationService.getApplicationNameList(this.pcId, this.datePipe.transform(dateNow-dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: ApplicationNames) => {
        this.applicationNameList = data;
        for (let app of this.applicationNameList.application_list) {
          this.runningApps.push(app);
        }
        this.displayedApps = this.applicationNameList.application_list;
        if(this.isApplicationSelected) {
          this.loadApplicationData(this.selectedApplication.application_name);
        } else {
          this.loadApplicationData(this.displayedApps[0]);
        }
      });
    }
  }

  filterApplicationNameList(): void {
    //console.log("d\n" + this.displayedApps);
    //console.log("r\n" + this.runningApps);
    this.displayedApps = this.runningApps;
    //console.log("d\n" + this.displayedApps);
    let tmp: string[] = [];
    for (let app of this.displayedApps) {
      if(app.toLowerCase().includes(this.searchCriteria.toLowerCase())) {
        tmp.push(app);
      }
    }
    //console.log("t\n" + tmp);
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
      this.applicationService.getApplicationByApplicationName(1, applicationName, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds == 0 ? dateNow : dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.selectedBucketingTime.value).subscribe((data: Application) => {
        this.selectedApplication = data;
        //console.log(data);
        //this.latestApplicationMeasurement = this.getLatestApplicationMeasurementOfSelectedApplication();
        this.setData();
        this.reloadCPUChart();
        this.reloadRAMChart();
        this.loadAlerts();

      });
    } else {
      this.applicationService.getApplicationByApplicationName(1, applicationName, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.selectedBucketingTime.value).subscribe((data: Application) => {
        this.selectedApplication = data;
        //console.log(data);
        //this.latestApplicationMeasurement = this.getLatestApplicationMeasurementOfSelectedApplication();
        this.setData();
        this.reloadCPUChart();
        this.reloadRAMChart();
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

  destroyCPUChart() {
    if(this.cpuChart) {
      this.cpuChart.destroy();
    }
  }

  destroyRAMChart() {
    if(this.ramChart) {
      this.ramChart.destroy();
    }
  }

  showAllCPUChart(): void {
    this.destroyCPUChart();
    this.cpuChart = new Chart("usageCPU", {
      data: {
        datasets: this.getCPUEventDataSet(),
        labels: this.cpuData.measurementTime
      },
      options: {
        responsive: true,
        //maintainAspectRatio: true,
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
              label: (context) => this.getCPUEventMsg(context)
            }
          }
        }
      }
    })
  }

  showAllRAMChart(): void {
    this.destroyRAMChart();
    this.ramChart = new Chart("usageRAM", {
      data: {
        datasets: this.getRAMEventDataSet(),
        labels: this.ramData.measurementTime
      },
      options: {
        responsive: true,
        //maintainAspectRatio: true,
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
              label: (context) => this.getRAMEventMsg(context)
            }
          }
        }
      }
    })
  }
  showAnomalyCPUChart(): void {
    this.destroyCPUChart();
    this.cpuChart = new Chart("usageCPU", {
      data: {
        datasets: [{
          type: 'line',
          label: 'Line Dataset',
          data: this.getCpuData().usage,
          backgroundColor: 'rgba(62, 149, 205, 0.5)',
          borderColor: '#3e95cd',
          order: 2
        }, {
          type: 'scatter',
          label: 'Scatter Dataset',
          data: this.getCPUAnomalies(),
          backgroundColor: '#e82546',
          borderColor: '#e82546'
        }],
        labels: this.cpuData.measurementTime
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
          },
          tooltip: {
            callbacks: {
              label: (context) => this.getCPUEventMsg(context)
            }
          }
        }
      }
    })
  }
  showAnomalyRAMChart(): void {
    this.destroyRAMChart();
    this.ramChart = new Chart("usageRAM", {
      data: {
        datasets: [{
          type: 'line',
          label: 'Line Dataset',
          data: this.ramData.usage,
          backgroundColor: 'rgba(62, 149, 205, 0.5)',
          borderColor: '#3e95cd',
          order: 2
        }, {
          type: 'scatter',
          label: 'Scatter Dataset',
          data: this.getRAMAnomalies(),
          backgroundColor: '#e82546',
          borderColor: '#e82546'
        }],
        labels: this.ramData.measurementTime
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
          },
          tooltip: {
            callbacks: {
              label: (context) => this.getRAMEventMsg(context)
            }
          }
        }
      }
    })
  }

  getRAMEventDataSet(): any[] {
    let dataset: any[] = [{
      type: 'line',
      label: 'Line Dataset',
      data: this.getRamData().usage,
      backgroundColor: 'rgba(62, 149, 205, 0.5)',
      borderColor: '#3e95cd',
      order: 3
    },{
      type: 'scatter',
      label: 'Scatter Dataset',
      data: this.getRAMAnomalies(),
      backgroundColor: '#e82546',
      borderColor: '#e82546',
      order: 1
    }];
    this.getRAMEvents().forEach((data) => {
      dataset.push({type: 'line', data: data, fill: true, backgroundColor: 'rgba(179, 0, 255, 0.25)', borderColor: 'rgb(179, 0, 255, 0.5)', order: 2});
    });
    return dataset;
  }

  getCPUEventDataSet(): any[] {
    let dataset: any[] = [{
      type: 'line',
      label: 'Line Dataset',
      data: this.getCpuData().usage,
      backgroundColor: 'rgba(62, 149, 205, 0.5)',
      borderColor: '#3e95cd',
      order: 3
    },{
    type: 'scatter',
      label: 'Scatter Dataset',
      data: this.getCPUAnomalies(),
      backgroundColor: '#e82546',
      borderColor: '#e82546',
      order: 1
  }];
    this.getCPUEvents().forEach((data) => {
      dataset.push({type: 'line', data: data, fill: true, backgroundColor: 'rgba(179, 0, 255, 0.25)', borderColor: 'rgb(179, 0, 255, 0.5)', order: 2});
    });
    return dataset;
  }
  getRAMEvents() {
    let events: any[] = [];
    var inEvent: boolean = false;
    this.selectedApplication.ram_events_and_anomalies.forEach((event) => {
      if(!event.is_anomaly) {
        let tmpEvent: any[] = [];
        this.selectedApplication.time_series_data.forEach((data) => {
          //console.log(data.measurement_time + "\n" + this.datePipe.transform(event.till_timestamp, 'yyyy-MM-ddTHH:mm' ?? "") + "->" + event.timestamp);
          if(this.datePipe.transform(data.measurement_time, 'yyyy-MM-ddTHH:mm' ?? "") == this.datePipe.transform(event.till_timestamp, 'yyyy-MM-ddTHH:mm' ?? "")) {
            //console.log(data.measurement_time + "\n" + this.datePipe.transform(event.till_timestamp, 'yyyy-MM-ddTHH:mm' ?? "") + "->" + event.timestamp);
            inEvent = true;
            tmpEvent.push(this.roundDecimalNumber(this.convertBytesToMegaBytes(data.ram), 2));
          } else if(data.measurement_time == event.timestamp) {
            tmpEvent.push(this.roundDecimalNumber(this.convertBytesToMegaBytes(data.ram), 2));
            inEvent = false;
          } else if(inEvent) {
            tmpEvent.push(this.roundDecimalNumber(this.convertBytesToMegaBytes(data.ram), 2));
          } else {
            tmpEvent.push(null);
          }
        })
        //console.log(tmpEvent);
        events.push(tmpEvent);
      }
    })
    return events;
  }

  getCPUEvents() {
    let events: any[] = [];
    var inEvent: boolean = false;
    this.selectedApplication.cpu_events_and_anomalies.forEach((event) => {
      if(!event.is_anomaly) {
        let tmpEvent: any[] = [];
        this.selectedApplication.time_series_data.forEach((data) => {
          //console.log(data.measurement_time + "\n" + this.datePipe.transform(event.till_timestamp, 'yyyy-MM-ddTHH:mm' ?? "") + "->" + event.timestamp);
          if(this.datePipe.transform(data.measurement_time, 'yyyy-MM-ddTHH:mm' ?? "") == this.datePipe.transform(event.till_timestamp, 'yyyy-MM-ddTHH:mm' ?? "")) {
            //console.log(data.measurement_time + "\n" + this.datePipe.transform(event.till_timestamp, 'yyyy-MM-ddTHH:mm' ?? "") + "->" + event.timestamp);
            inEvent = true;
            tmpEvent.push(this.roundDecimalNumber(data.cpu*100, 2));
          } else if(data.measurement_time == event.timestamp) {
            tmpEvent.push(this.roundDecimalNumber(data.cpu*100, 2));
            inEvent = false;
          } else if(inEvent) {
            tmpEvent.push(this.roundDecimalNumber(data.cpu*100, 2));
          } else {
            tmpEvent.push(null);
          }
        })
        //console.log(tmpEvent);
        events.push(tmpEvent);
      }
    })
    return events;
  }
  getRAMAnomalies() {
    let anomalyPositions: any[] = [];
    var success: boolean = false;

    this.selectedApplication.time_series_data.forEach((data, index) => {
      for (let anomaly of this.selectedApplication.ram_events_and_anomalies) {
        if (data.measurement_time == anomaly.timestamp && anomaly.is_anomaly) {
          anomalyPositions.push(this.ramData.usage[index]);
          success = true;
        }
      }
      if(!success) {
        anomalyPositions.push(null);
      }
      success=false;
    })
    return anomalyPositions;
  }
  getCPUAnomalies() {
    let anomalyPositions: any[] = [];
    var success: boolean = false;

    this.selectedApplication.time_series_data.forEach((data, index) => {
      for (let anomaly of this.selectedApplication.cpu_events_and_anomalies) {
        if (data.measurement_time == anomaly.timestamp && anomaly.is_anomaly) {
          anomalyPositions.push(this.cpuData.usage[index]);
          success = true;
        }
      }
      if(!success) {
        anomalyPositions.push(null);
      }
      success=false;
    })
    return anomalyPositions;
  }
  getRAMEventMsg(context: TooltipItem<keyof ChartTypeRegistry>): string[] {
    let msg: string = "";
    if(context.dataset.borderColor != "#3e95cd") {
      this.selectedApplication.ram_events_and_anomalies.forEach((data) => {
        if(this.datePipe.transform(data.till_timestamp, 'MM-dd HH:mm') == context.label || this.datePipe.transform(data.timestamp, 'MM-dd HH:mm') == context.label) {
          msg = data.justification_message;
        }
      });
    } else {
      msg += context.parsed.y + "%";
    }
    return msg.split("\n");
  }

  getCPUEventMsg(context: TooltipItem<keyof ChartTypeRegistry>): string[] {
    let msg: string = "";
    if(context.dataset.borderColor != "#3e95cd") {
      this.selectedApplication.cpu_events_and_anomalies.forEach((data) => {
        if(this.datePipe.transform(data.till_timestamp, 'MM-dd HH:mm') == context.label || this.datePipe.transform(data.timestamp, 'MM-dd HH:mm') == context.label) {
          msg = data.justification_message;
        }
      });
    } else {
      msg += context.parsed.y + "%";
    }
    return msg.split("\n");
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
        //maintainAspectRatio: false,
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
        //maintainAspectRatio: false,
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
      data.usage.push(this.roundDecimalNumber(cpuUsageMeasurement.cpu*100, 2));
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
    //console.log(this.selectedApplication.application_name)
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

