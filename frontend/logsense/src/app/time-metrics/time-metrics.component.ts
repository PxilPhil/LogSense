import { Component, OnDestroy, OnInit } from '@angular/core';
import {Chart} from "chart.js";
import {TimeModel} from "../disk/disk.component";
import {TimeMetrics, TimeMetricsModel} from "../model/TimeMetrics";
import {TimeMetricsService} from "../services/time-metrics.service";
import {DatePipe} from "@angular/common";

@Component({
  selector: 'app-time-metrics',
  templateUrl: './time-metrics.component.html',
  styleUrls: ['./time-metrics.component.scss']
})
export class TimeMetricsComponent implements OnInit, OnDestroy {

  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];
  selectedTime: TimeModel = this.times[0];

  timeMetricsChart: Chart | undefined;
  timeMetrics: TimeMetrics = new TimeMetrics();
  showAll: boolean = false;

  constructor(private timeService: TimeMetricsService, private datePipe: DatePipe) {
  }

  ngOnInit() {
    this.loadTimeMetrics();
    console.log(this.timeMetrics);
  }
  ngOnDestroy() {
    if (this.timeMetricsChart) {
      this.timeMetricsChart.destroy();
    }
  }
  timeChart() {
    if(this.timeMetricsChart) {
      this.timeMetricsChart.destroy();
    }

    this.timeMetricsChart = new Chart("timeChart", {
      type: 'bar',
      data: {
        labels: this.timeMetrics.name,
        datasets: [{
          data: (this.timeMetrics.total_running_time_minutes),
          borderColor: "#2b26a8",
          backgroundColor: "#7BE1DF",
        }]
      },
      options: {
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
                label += context.parsed.y + ' hrs';
                return label;
              }
            }
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

  loadTimeMetrics() {
    let dateNow = Date.now();
    this.timeMetrics.name = [];
    this.timeMetrics.total_running_time_minutes = [];
    var i = 0;
    if(this.selectedTime.valueInMilliseconds!=0) {
      this.timeService.getTimeMetrics(1,this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: TimeMetricsModel) => {
        for (let entry of data.data) {
          this.timeMetrics.name.push(entry.name);
          this.timeMetrics.total_running_time_minutes.push(Math.round((entry.total_running_time_seconds/60/60 + Number.EPSILON) * 100) / 100); //seconds to hrs
          i++;
          if(!this.showAll && i >= 10) {
            break;
          }
        }
        this.timeChart();
      });
    } else {
      this.timeService.getTimeMetrics(1,this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe((data: TimeMetricsModel) => {
        for (let entry of data.data) {
          this.timeMetrics.name.push(entry.name);
          this.timeMetrics.total_running_time_minutes.push(Math.round((entry.total_running_time_seconds/60/60 + Number.EPSILON) * 100) / 100); //seconds to hours
          i++;
          if(!this.showAll && i >= 10) {
            break;
          }
        }
        this.timeChart();
      });
    }
  }
}
