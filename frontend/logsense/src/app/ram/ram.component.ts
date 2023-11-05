import {Component, OnInit} from '@angular/core';
import {Chart} from "chart.js";
import {TimeModel} from "../disk/disk.component";
import {Process, TimeSeriesList} from "../model/PCData";
import {PCDataService} from "../services/pc-data.service";
import {DatePipe} from "@angular/common";
import {RAMModel, RamStats} from "../model/Ram";
import {ResourceMetricsService} from "../services/resource-metrics.service";
import {ResourceMetricsModel} from "../model/ResourceMetrics";
import {Alert} from "../model/Alert";
import {AlertService} from "../services/alert.service";
import {SelectedPcService} from "../services/selected-pc.service";

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
    displayedProcesses: Process[] = [];

    timeSeriesData: TimeSeriesList = new TimeSeriesList();
    ramData: ChartData = new ChartData();

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
    alerts: Alert[] = []
    showAllProcesses: boolean = true;

    pcId: number = 0;
    showPcIdAlert: boolean = true;

    constructor(private alertService: AlertService, private statsService: ResourceMetricsService, private pcDataService: PCDataService, private selectedPcService: SelectedPcService, private datePipe: DatePipe, private resourceService: ResourceMetricsService) {
    }

    showAll() {
        this.displayedProcesses = [];
        if (!this.showAllProcesses) {
            this.displayedProcesses = this.ram.allocation_list;
        } else {
            var i = 1;
            for (let process of this.ram.allocation_list) {
                if (i < 9) {
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
        this.getSelectedPcId();
        this.loadStats();
        this.loadData();
        this.loadAlerts();
    }

    usageChart(): void {
        if (this.ramChart) {
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
        this.statsService.getResourceMetrics(this.pcId).subscribe((data: ResourceMetricsModel) => {
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
        if (this.selectedTime.valueInMilliseconds != 0) {
            this.pcDataService.getRAMData(this.pcId, this.datePipe.transform(dateNow - this.selectedTime.valueInMilliseconds, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: RAMModel) => {
                this.ram = data;
                this.transformData();
                this.showAll();
                this.usageChart();
            });
        } else {
            this.pcDataService.getRAMData(this.pcId, this.datePipe.transform(dateNow - dateNow, 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(dateNow, "yyyy-MM-ddTHH:mm:ss.SSS") ?? "").subscribe((data: RAMModel) => {
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
            this.ramData.time.push(this.datePipe.transform(dataPoint.measurement_time, 'MM-dd HH:mm:ss') ?? "");
            this.ramData.value.push(this.roundDecimal(this.convertBytesToGigaBytes(dataPoint.value), 2));
        }
        this.ram.allocation_list.forEach((value, index) => {
            this.ram.allocation_list[index].allocation = this.roundDecimal(this.ram.allocation_list[index].allocation * 100, 2);
        })
    }

    convertBytesToGigaBytes(valueInBytes: number): number {
        return (valueInBytes / 1000 / 1000 / 1000);
    }

    roundDecimal(num: number, places: number): number {
        return Math.round((num + Number.EPSILON) * Math.pow(10, places)) / Math.pow(10, places);
    }

    loadAlerts() {
        this.alerts = this.alertService.getStoredAlerts(undefined, ['ram']);
        console.log(this.alerts)

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
