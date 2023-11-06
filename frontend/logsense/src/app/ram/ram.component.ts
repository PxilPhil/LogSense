import {Component, OnInit} from '@angular/core';
import {ProcessModel} from "../cpu/cpu.component";
import {Chart, ChartTypeRegistry, TooltipItem} from "chart.js";
import {TimeModel} from "../disk/disk.component";
import {PCData, Process, TimeSeriesList} from "../model/PCData";
import {PCDataService} from "../services/pc-data.service";
import {DatePipe} from "@angular/common";
import {RAMModel, RamStats} from "../model/Ram";
import {ResourceMetricsService} from "../services/resource-metrics.service";
import _default from "chart.js/dist/core/core.interaction";
import index = _default.modes.index;
import {ResourceMetricsModel} from "../model/ResourceMetrics";
import {Alert} from "../model/Alert";
import {AlertService} from "../services/alert.service";

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

export class ChartDataset {
  type: string = "";
  label?: string; // Die Beschriftung des Datensatzes
  data: number[] = []; // Ein Array von Y-Werten
  borderColor?: string; // Die Farbe der Linie
  backgroundColor?: string; // Die Farbe des Bereichs unter der Linie
  borderWidth?: number; // Die Linienbreite
  fill?: boolean; // Ob der Bereich unter der Linie gefüllt werden soll
  order?: number;
  // Weitere Eigenschaften können hinzugefügt werden, je nach Bedarf
}

@Component({
  selector: 'app-ram',
  templateUrl: './ram.component.html',
  styleUrls: ['./ram.component.scss']
})
export class RamComponent implements OnInit {
  ram: RAMModel = new RAMModel();
  ramStats: RamStats = new RamStats();
  ramData: ChartData = new ChartData();
  displayedProcesses: Process[] = [];
  ramChart: Chart | undefined;

  //timeSeriesData: TimeSeriesList = new TimeSeriesList();
  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];
  selectedTime: TimeModel = this.times[0];

  checked: String = "";
  radioOptions: String[] = ["Show None", "Show Anomalies", "Show Events and Anomalies"];

  alerts: Alert[] = []
  showAllProcesses: boolean = true;

  constructor(private alertService: AlertService, private statsService: ResourceMetricsService, private pcDataService: PCDataService, private  datePipe: DatePipe) {
  }

  ngOnInit() {
    this.loadStats();
    this.loadData();
    this.loadAlerts();
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
  reloadChart() {
    switch (this.checked) {
      case this.radioOptions[1]: {
        this.showAnomalyChart();
        break;
      }
      case this.radioOptions[2]: {
        this.showAllChart();
        break;
      }
      default: {
        this.usageChart();
        break;
      }
    }
  }

  destroyChart() {
    if(this.ramChart) {
      this.ramChart.destroy();
    }
  }

  showAnomalyChart() {
    this.destroyChart();
    this.ramChart = new Chart("ram", {
      data: {
        datasets: [{
          type: 'line',
          label: 'Line Dataset',
          data: this.ramData.value,
          backgroundColor: 'rgba(62, 149, 205, 0.5)',
          borderColor: '#3e95cd',
          order: 2
        },{
          type: 'scatter',
          label: 'Scatter Dataset',
          data: this.getAnomalies(),
          backgroundColor: '#e82546',
          borderColor: '#e82546'
        }],
        labels: this.ramData.time
      },
      options: {
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
              label: (context) => this.getEventMsg(context)
            }
          }
        }
      }
    })
  }

  showAllChart() {
    this.destroyChart();
    this.ramChart = new Chart("ram", {
      data: {
        datasets: this.getEventDataSet(),
        labels: this.ramData.time
      },
      options: {
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
              label: (context) => this.getEventMsg(context)
            }
          }
        }
      }
    })
  }

  usageChart(): void {
    this.destroyChart();
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
  getEventDataSet() {
    console.log(this.ramData);
    let dataset: any[] = [{
      type: 'line',
      label: 'Line Dataset',
      data: this.ramData.value,
      backgroundColor: 'rgba(62, 149, 205, 0.5)',
      borderColor: '#3e95cd',
      order: 3
    },{
      type: 'scatter',
      label: 'Scatter Dataset',
      data: this.getAnomalies(),
      backgroundColor: '#e82546',
      borderColor: '#e82546'
    }];
    this.getEvents().forEach((data, index) => {
      dataset.push({type: 'line', data: data, fill: true, backgroundColor: 'rgba(179, 0, 255, 1)', borderColor: 'rgb(179, 0, 255)', order: 2});
    });
    return dataset;
  }
  getEvents(){
    let events: any[] = [];
    var inEvent: boolean = false;
    this.ram.events_and_anomalies.forEach((event, eventIndex) => {
      if(!event.is_anomaly) {
        let tmpEvent: any[] = [];
        this.ram.time_series_list.forEach((data, dataIndex) => {
          if(data.measurement_time == event.till_timestamp) {
            //console.log(data.measurement_time + "\n" + event.till_timestamp + "->" + event.timestamp);
            inEvent = true;
            tmpEvent.push(this.roundDecimal(this.convertBytesToGigaBytes(data.value), 2));
          } else if(data.measurement_time == event.timestamp) {
            tmpEvent.push(this.roundDecimal(this.convertBytesToGigaBytes(data.value), 2));
            inEvent = false;
          } else if(inEvent) {
            tmpEvent.push(this.roundDecimal(this.convertBytesToGigaBytes(data.value), 2));
          } else {
            tmpEvent.push(null);
          }
        })
        events.push(tmpEvent);
      }
    })
    return events;
  }

  getAnomalies(){
    let anomalyPositions: any[] = [];
    var success: boolean = false;

    this.ram.time_series_list.forEach((data, index) => {
      for (let anomaly of this.ram.events_and_anomalies) {
        if (data.measurement_time == anomaly.timestamp && anomaly.is_anomaly) {
          anomalyPositions.push(this.ramData.value[index]);
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
  getEventMsg(context: TooltipItem<keyof ChartTypeRegistry>): string[] {
    let msg: string = "";
    if(context.dataset.borderColor != "#3e95cd") {
      this.ram.events_and_anomalies.forEach((data, index) => {
        //console.log(context.label + ":" + data.timestamp);
        if(this.datePipe.transform(data.till_timestamp, 'MM-dd HH:mm:ss') == context.label || this.datePipe.transform(data.timestamp, 'MM-dd HH:mm:ss') == context.label) {
          msg = data.justification_message;
        }
      });
    } else {
      msg += context.parsed.y + "%";
    }
    return msg.split("\n");
  }
  loadStats() {
    this.statsService.getResourceMetrics(1).subscribe((data: ResourceMetricsModel) => {
      this.ramStats.avg = this.roundDecimal(data.avg_ram_usage_percentage_last_day, 2);
      this.ramStats.cur = this.roundDecimal(data.ram_percentage_in_use, 2);
      this.ramStats.stability = data.ram_stability;
      this.ramStats.free = this.roundDecimal(this.convertBytesToGigaBytes(data.free_memory), 2);
      this.ramStats.page = data.page_size;
      this.ramStats.total = this.roundDecimal(this.convertBytesToGigaBytes(data.total_memory), 2);
    });
  }
  loadData() {
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds!=0) {
      this.pcDataService.getRAMData(1, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: RAMModel) => {
        this.ram = data;
        this.transformData();
        this.showAll();
        this.reloadChart();
      });
    } else {
      this.pcDataService.getRAMData(1, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: RAMModel) => {
        this.ram = data;
        this.transformData();
        this.showAll();
        this.reloadChart();
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

  loadAlerts() {
    this.alerts = this.alertService.getStoredAlerts(undefined, ['ram']);
    console.log(this.alerts)

  }

}
