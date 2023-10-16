import { Component, OnDestroy, OnInit } from '@angular/core';
import {Chart} from "chart.js";
import {TimeModel} from "../disk/disk.component";
import {TimeMetrics} from "../model/TimeMetrics";
import {TimeMetricsService} from "../services/time-metrics.service";
import {DatePipe} from "@angular/common";

@Component({
  selector: 'app-time-metrics',
  templateUrl: './time-metrics.component.html',
  styleUrls: ['./time-metrics.component.scss']
})
export class TimeMetricsComponent {

  selectedTime: TimeModel = {id: 1, time: "Last 24h", valueInMilliseconds: 86400000};
  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];

  timeMetricsChart: Chart | undefined;
  timeMetrics: TimeMetrics = new TimeMetrics();

  constructor(private timeService: TimeMetricsService, private datePipe: DatePipe) {
  }

  ngOnInit() {
    this.timeChart();
  }
  ngOnDestroy() {
    if (this.timeMetricsChart) {
      this.timeMetricsChart.destroy();
    }
  }
  timeChart() {
    const data = this.getData();
    this.timeMetricsChart = new Chart("timeChart", {
      type: 'bar',
      data: {
        labels: data.name,
        datasets: [{
          data: data.total_running_time_seconds,
          borderColor: "#2b26a8",
          backgroundColor: "#7BE1DF",
        }]
      },
      options: {
        plugins: {
          legend: {
            display: true,
            position: "right"
          }
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  getData(): TimeMetrics {
    let dateNow = Date.now();
    this.timeService.getTimeMetrics(1,this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: TimeMetrics) => {
      this.timeMetrics = data;
    });
    return this.timeMetrics;
  }
}
