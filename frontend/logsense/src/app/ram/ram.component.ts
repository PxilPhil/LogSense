import {Component, OnInit} from '@angular/core';
import {ProcessModel} from "../cpu/cpu.component";
import {Chart} from "chart.js";
import {TimeModel} from "../disk/disk.component";
import {PCData, Process, TimeSeriesList} from "../model/PCData";
import {PCDataService} from "../services/pc-data.service";
import {DatePipe} from "@angular/common";
import {RAMModel, RamStats} from "../model/Ram";
import {ResourceMetricsService} from "../services/resource-metrics.service";
import _default from "chart.js/dist/core/core.interaction";
import index = _default.modes.index;

/*export class RAMModel {
  totalMemory: Number = 17.02; //GB
  freeMemory: Number = 12.02; //GB
  pageSize: Number = 4.096; //KB
  current: Number = 21; //%
  average: Number = 48; //%
  stability: String = "TODO";
  stats: String[] = ["RAM Usage dropped 4%", "21 anomalies detected", "5 Events registered", "Recent Rise of 15% detected"];
  processes: ProcessModel[] = [{name: "Chrome", allocation: 15}, {name: "Explorer", allocation: 10}, {
    name: "Intellij",
    allocation: 48
  }];
  alerts: String[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];
}*/

export class ChartData {
  time: string[] = [];
  value: number[] = [];
}

@Component({
  selector: 'app-ram',
  templateUrl: './ram.component.html',
  styleUrls: ['./ram.component.scss']
})
export class RamComponent implements OnInit {
  ram: RAMModel = new RAMModel();
  displayedProcesses: Process[] = [];

  timeSeriesData: TimeSeriesList = new TimeSeriesList();
  ramData: ChartData =  new ChartData();

  ramChart: Chart | undefined;

  ramStats: RamStats = new RamStats();
  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];
  selectedTime: TimeModel = this.times[0];

  showAllProcesses: boolean = true;

  constructor(private pcDataService: PCDataService, private  datePipe: DatePipe, private resourceService: ResourceMetricsService) {
  }

  showAll() {
    this.displayedProcesses = [];
    if(!this.showAllProcesses) {
      this.displayedProcesses = this.ram.allocation_list;
    } else {
      var i = 1;
      for (let process of this.ram.allocation_list) {
        if(i<9) {
          this.displayedProcesses.push(process);
          i++;
        } else {
          break;
        }
      }
    }
    this.showAllProcesses = !this.showAllProcesses;
  }
  ngOnInit() {
    //this.loadStats() // TODO: soboids den API Call gibt Stats lodn
    this.loadData();
  }

  usageChart(): void {
    if(this.ramChart) {
      this.ramChart.destroy();
    }
    this.ramChart = new Chart("ram", {
      type: "line",
      data: {
        labels: this.ramData.time,
        datasets: [{
          data: this.ramData.value,
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

  loadStats() {
    /*let pcData: PCData = new PCData();
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds != 0) {
      this.pcDataService.getPcData(1, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: PCData) => {
        pcData = data;
        this.ramStats.stability = pcData.stability_ram;
      });
      //this.resourceService.getResourceMetrics(1)
    }*/
  }
  loadData() {
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds!=0) {
      this.pcDataService.getRAMData(1, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: RAMModel) => {
        this.ram = data;
        this.transformData();
        this.showAll();
        this.usageChart();
      });
    } else {
      this.pcDataService.getRAMData(1, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: RAMModel) => {
        this.ram = data;
        this.transformData();
        this.showAll();
        this.usageChart();
      });
    }
  }

  transformData() {
    this.ramData.time = [];
    this.ramData.value = [];
    for (let dataPoint of this.ram.time_series_list) {
      this.ramData.time.push(this.datePipe.transform(dataPoint.measurement_time, 'MM-dd HH:mm:ss')??"");
      this.ramData.value.push(this.roundDecimal(this.convertBytesToGigaBytes(dataPoint.value), 2));
    }
    this.ram.allocation_list.forEach((value, index) => {
      this.ram.allocation_list[index].allocation = this.roundDecimal(this.ram.allocation_list[index].allocation*100, 2);
    })
  }

  convertBytesToGigaBytes(valueInBytes: number): number {
    return (valueInBytes / 1000 / 1000 / 1000);
  }

  roundDecimal(num: number, places: number): number{
    return Math.round((num + Number.EPSILON) * Math.pow(10, places)) / Math.pow(10, places);
  }

}
