import {Component, OnInit} from '@angular/core';
import {Chart} from "chart.js";
import {ApplicationService} from "../services/application.service";
import {ApplicationNames} from "../model/ApplicationNames";
import {DatePipe} from "@angular/common";
import {Application, ApplicationTimeSeriesData} from "../model/Application";
import {AlertService} from "../services/alert.service";
import {Alert} from "../model/Alert";

@Component({
  selector: 'app-single-processes',
  templateUrl: './single-processes.component.html',
  styleUrls: ['./single-processes.component.scss']
})
export class SingleProcessesComponent implements OnInit {
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
  latestApplicationMeasurement: ApplicationTimeSeriesData = new ApplicationTimeSeriesData();
  statistics: string[] = ["CPU Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Rise of RAM usage of 90% detected"];
  alerts: Alert[] = ["Abnormal RAM-Spikes detected", "Memory leak possible"];
  isApplicationSelected = false;

  constructor(private applicationService: ApplicationService, private alertService: AlertService, private datePipe: DatePipe) {
  }

  ngOnInit() {
    this.loadApplicationNameList();
    //this.loadAlerts();  //TODO: insert again when endpoint is implemented
    this.cpuUsageChart();
    this.ramUsageChart()
  }

  loadApplicationNameList(): void {
    let dateNow = Date.now();
    this.applicationService.getApplicationNameList(1, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds == 0 ? dateNow : this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: ApplicationNames) => {
      this.applicationNameList = data;
    });
  }

  loadAlerts(): void {
    this.alertService.getAlerts().subscribe((data: Alert[]) => {
      this.alerts = data;
    })
  }

  loadApplicationDataOnApplicationNameClick(applicationName: string): void {
    this.isApplicationSelected = true;
    let dateNow = Date.now();
    this.applicationService.getApplicationByApplicationName(1, applicationName, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds == 0 ? dateNow : this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: Application) => {
      this.selectedApplication = data;
      this.latestApplicationMeasurement = this.getLatestApplicationMeasurementOfSelectedApplication();
    });
  }

  getLatestApplicationMeasurementOfSelectedApplication(): ApplicationTimeSeriesData {
    if (this.selectedApplication.time_series_data.length > 0) {
      return this.selectedApplication.time_series_data.reduce((previous, current) => {
        return (current.measurement_time > previous.measurement_time) ? current : previous;
      });
    }
    return new ApplicationTimeSeriesData();
  }

  cpuUsageChart(): void {
    const data = this.getData();
    const usage = new Chart("usageCPU", {
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

  ramUsageChart(): void {
    const data = this.getData();
    const usage = new Chart("usageRAM", {
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
    return {labels, values};
  }

  formatUpTime(upTime: number): string {
    const date = new Date(upTime);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    const seconds = date.getSeconds().toString().padStart(2, '0');
    return `${hours} hours, ${minutes} minutes and ${seconds} seconds`;
  }
}

