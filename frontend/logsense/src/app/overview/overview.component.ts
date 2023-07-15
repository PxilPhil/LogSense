import { Component, OnInit } from '@angular/core';
import {Chart, Plugin, registerables} from 'chart.js';
Chart.register(...registerables);

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {

  client: String = "Acer Nitro 5";
  runtime: String = "2h 30min";


  constructor() { }

  ngOnInit(): void {
    this.resourceMetricsCharts();
  }

  xValues: Number[] = [50,60,70,80,90,100,110,120,130,140,150];
  yValues: Number[] = [7,8,8,9,9,9,10,11,14,14,15];


  resourceMetricsCharts(): void {
    var resMetrics = new Chart("resMetrics", {
      type: 'line',
      data: {
        labels: [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050],
        datasets: [{
          data: [86,114,106,106,107,111,133,221,783,2478],
          label: "Africa",
          borderColor: "#3e95cd",
          fill: false
        }, {
          data: [282,350,411,502,635,809,947,1402,3700,5267],
          label: "Asia",
          borderColor: "#8e5ea2",
          fill: false
        }, {
          data: [168,170,178,190,203,276,408,547,675,734],
          label: "Europe",
          borderColor: "#3cba9f",
          fill: false
        }, {
          data: [40,20,10,16,24,38,74,167,508,784],
          label: "Latin America",
          borderColor: "#e8c3b9",
          fill: false
        }, {
          data: [6,3,2,2,7,26,82,172,312,433],
          label: "North America",
          borderColor: "#c45850",
          fill: false
        }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: {
            position: 'right',
            align: 'center',
            labels: {
              usePointStyle: true,
              padding: 24,
              font: {
                family: "'Arial'",
                size: 16,
              }
            },
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
}
