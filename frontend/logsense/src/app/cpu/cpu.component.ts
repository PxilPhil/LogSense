import {Component, Inject, LOCALE_ID, OnInit} from '@angular/core';
import {Chart} from "chart.js";
import {CPUGeneral, CPUModel, CPUStats} from "../model/Cpu";
import {CpuService} from "../services/cpu.service";
import {PCDataService} from "../services/pc-data.service";
import {DatePipe, formatDate} from "@angular/common";
import {PCData, Process, TimeSeriesList} from "../model/PCData";
import {ChartData, ChartDataset} from "../ram/ram.component";
import _default from "chart.js/dist/core/core.interaction";
import index = _default.modes.index;

/*export class CPUModel {
  cpuName: String = "AMD Ryzen 7 5800H";
  identifier: String = "Intel64 Family 6 Model 165 Stepping 2";
  processorID: String = "BFEBFBFF000A0652";
  vendor: String = "GenuineIntel";
  bitness: String = "64 Bit";
  physicalPackages: Number = 1;
  physicalProcessors: Number = 6;
  logicalProcessors: Number = 12;
  contextSwitches: String = "230431317";
  interrupts: String = "185631654";
  current: Number = 21; //%
  average: Number = 48; //%
  stability: String = "Low";
}
*/
export class ProcessModel {
  name: String = "chrome";
  allocation: Number = 15;
}


@Component({
  selector: 'app-cpu',
  templateUrl: './cpu.component.html',
  styleUrls: ['./cpu.component.scss']
})
export class CpuComponent implements OnInit {
  cpu: CPUModel = new CPUModel();
  cpuGeneral: CPUGeneral = new CPUGeneral();
  cpuStats: CPUStats = new CPUStats();
  cpuData: ChartData = new ChartData();
  displayedProcesses: Process[] = [];
  cpuChart: Chart | undefined;

  notes: String[] = ["CPU Usage dropped 4%", "21 Anomalies detected", "5 Events registered"];
  processes: ProcessModel[] = [{name: "Chrome", allocation: 15}, {name: "Explorer", allocation: 10}, {
    name: "Intellij",
    allocation: 48
  }];
  alerts: String[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];
  times = [
    {id: 1, time: "Last 24h", valueInMilliseconds: 86400000},
    {id: 2, time: "Last Week", valueInMilliseconds: 604800000},
    {id: 3, time: "Last Month", valueInMilliseconds: 2629746000},
    {id: 4, time: "Last 6 Months", valueInMilliseconds: 15778476000},
    {id: 5, time: "Last 12 Months", valueInMilliseconds: 31556952000},
    {id: 6, time: "All Time", valueInMilliseconds: 0}
  ];
  selectedTime = this.times[0];
  showAllProcesses: boolean = true;

  checked: String = "";
  radioOptions: String[] = ["Show None", "Show Anomalies", "Show Events and Anomalies"];

  constructor(private cpuService: CpuService, private pcDataService: PCDataService, private datePipe: DatePipe, @Inject(LOCALE_ID) public locale: string) {}

  ngOnInit() {
    this.loadData();
    this.loadStats();
    this.loadGeneralInfo();
  }

  showAll() {
    this.displayedProcesses = [];
    if(!this.showAllProcesses) {
      this.displayedProcesses = this.cpu.allocation_list;
    } else {
      var i = 1;
      for (let process of this.cpu.allocation_list) {
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
  destroyCharts() {
    if(this.cpuChart) {
      this.cpuChart.destroy();
    }
  }

  showAnomalyChart() {
    this.destroyCharts();
    this.cpuChart = new Chart("usage", {
      data: {
        datasets: [{
          type: 'line',
          label: 'Line Dataset',
          data: this.cpuData.value,
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
        labels: this.cpuData.time
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
              label: function (context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ' ';
                }
                label += context.parsed.y + ' %';
                return label;
              }
            }
          }
        }
      }
    })
  }
  showAllChart() {
    this.destroyCharts();
    this.cpuChart = new Chart("usage", {
      data: {
        datasets: this.getEventDataSet(),
        labels: this.cpuData.time
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
              label: function (context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ' ';
                }
                label += context.parsed.y + ' %';
                return label;
              }
            }
          }
        }
      }
    })
  }

  getEventDataSet() {
    let dataset: any[] = [{
      type: 'line',
      label: 'Line Dataset',
      data: this.cpuData.value,
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
      dataset.push({type: 'line', data: data, fill: true, backgroundColor: 'rgba(179, 0, 255, 0.25)', borderColor: 'rgb(179, 0, 255)', order: 2});
    });
    return dataset;
  }

  getEvents(){
    let events: any[] = [];
    var success: boolean = false;
    var inEvent: boolean = false;

    this.cpu.events_and_anomalies.forEach((event, eventIndex) => {
      if(!event.is_anomaly) {
        let tmpEvent: any[] = [];
        this.cpu.time_series_list.forEach((data, dataIndex) => {
          if(data.measurement_time == event.timestamp) {
            inEvent = true;
            tmpEvent.push(data.value * 100);
          } else if(data.measurement_time == event.till_timestamp) {
            tmpEvent.push(data.value * 100);
            inEvent = false;
          } else if(inEvent) {
            tmpEvent.push(data.value * 100);
          } else {
            tmpEvent.push(null);
          }
        })
        events.push(tmpEvent);
      }
    })
    /*this.cpu.time_series_list.forEach((data, index) => {
      for (let anomaly of this.cpu.events_and_anomalies) {
        if (data.measurement_time == anomaly.timestamp && !anomaly.is_anomaly) {
          events.push(this.cpuData.value[index]);
          success = true;
        }
        if(data.measurement_time == anomaly.till_timestamp) {

        }
      }
      if(!success) {
        events.push(null);
      }
      success=false;
    })*/
    console.log(events);
    return events;
  }


  getAnomalies(){
    let anomalyPositions: any[] = [];
    var success: boolean = false;

    this.cpu.time_series_list.forEach((data, index) => {
      for (let anomaly of this.cpu.events_and_anomalies) {
        if (data.measurement_time == anomaly.timestamp && anomaly.is_anomaly) {
          anomalyPositions.push(this.cpuData.value[index]);
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

  usageChart(): void {
    this.destroyCharts();
    this.cpuChart = new Chart("usage", {
      type: "line",
      data: {
        labels: this.cpuData.time,
        datasets: [{
          data: this.cpuData.value,
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
                label += context.parsed.y + ' %';
                return label;
              }
            }
          }
        }
      },
    });
  }

  loadGeneralInfo() {
    this.cpuService.getGeneral(1).subscribe((data: CPUGeneral) => {
      this.cpuGeneral = data;
    })
  }

  loadStats() {
    let pcData: PCData = new PCData();
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds != 0) {
      this.pcDataService.getPcData(1, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: PCData) => {
        pcData = data;
        this.cpuStats.mean_cpu = this.roundDecimal(pcData.mean_cpu, 2);
        this.cpuStats.stability_cpu = pcData.stability_cpu;
        this.cpuStats.cur_cpu = this.roundDecimal(pcData.time_series_list[0].cpu, 2);
      });
    } else {
      this.pcDataService.getPcData(1, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: PCData) => {
        pcData = data;
        this.cpuStats.mean_cpu = this.roundDecimal(pcData.mean_cpu, 2);
        this.cpuStats.stability_cpu = pcData.stability_cpu;
        this.cpuStats.cur_cpu = this.roundDecimal(pcData.time_series_list[0].cpu, 2);
      });
    }

  }

  loadData() {
    let dateNow = Date.now();
    if(this.selectedTime.valueInMilliseconds!=0) {
      this.pcDataService.getCPUData(1, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: CPUModel) => {
        this.cpu = data;
        this.transformData();
        this.showAll();

          this.getEvents();
        this.reloadChart();
      });
    } else {
      this.pcDataService.getCPUData(1, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: CPUModel) => {
        this.cpu = data;
        this.transformData();
        this.showAll();

        this.reloadChart();
      });
    }
  }

  transformData() {
    this.cpuData.time = [];
    this.cpuData.value = [];
    for (let dataPoint of this.cpu.time_series_list) {;
      this.cpuData.time.push(this.datePipe.transform(dataPoint.measurement_time, 'MM-dd HH:mm:ss')??"");
      this.cpuData.value.push(this.roundDecimal(dataPoint.value*100, 2));
    }
    this.cpu.allocation_list.forEach((value, i) => {
      this.cpu.allocation_list[i].allocation = this.roundDecimal(this.cpu.allocation_list[i].allocation * 100, 2);
    });
  }

  convertBytesToGigaBytes(valueInBytes: number): number {
    return (valueInBytes / 1000 / 1000 / 1000);
  }

  roundDecimal(num: number, places: number): number{
    return Math.round((num + Number.EPSILON) * Math.pow(10, places)) / Math.pow(10, places);
  }

}
