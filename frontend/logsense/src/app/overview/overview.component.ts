import {Component, OnInit} from '@angular/core';
import {Chart, registerables} from 'chart.js';
import {ResourceMetricsModel} from "../model/ResourceMetrics";
import {ResourceMetricsService} from "../services/resource-metrics.service";
import {AlertService} from "../services/alert.service";
import {DatePipe} from "@angular/common";
import {Alert} from "../model/Alert";
import {SelectedPcService} from "../services/selected-pc.service";
import {PcSelectionComponent} from "../pc-selection/pc-selection.component";

Chart.register(...registerables);

export class PowerSourceModel {
    systemBattery: String = "PowerSourceName";
    remainingCapacity: Number = 75; //%
    charging: Boolean = true;
    discharging: Boolean = false;
    powerOnLine: Boolean = true;
}

export class Client {
    manufacturer: String = "Acer";
    model: String = "Nitro AN517-52";
    uuid: String = "E4A2D298-F59B-EA11-80D6-089798A075FA";
    powerSources: PowerSourceModel = new PowerSourceModel();
}

@Component({
    selector: 'app-overview',
    templateUrl: './overview.component.html',
    styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {

    client: Client = new Client();
    runtime: String = "2h 30min";
    resourceMetrics: ResourceMetricsModel = new ResourceMetricsModel();
    /*cpu: CPUModel = new CPUModel();
    ram: RAMModel = new RAMModel();
    disk: DiskData = new DiskData();*/
    alerts: Alert[] = []
    //selectedTime: TimeModel = {id: 1, time: "Last 24h", valueInMilliseconds: 86400000};
    pcId: number = 0;
    showPcIdAlert: boolean = true;

    /*times = [
      {id: 1, time: "Last 24h"},
      {id: 2, time: "Last Week"},
      {id: 3, time: "Last Month"},
      {id: 4, time: "Last 6 Months"},
      {id: 5, time: "Last 12 Months"},
      {id: 6, time: "All Time"}
    ];*/

    constructor(private resourceService: ResourceMetricsService, private alertService: AlertService, private selectedPcService: SelectedPcService, private datePipe: DatePipe) {
    }

    ngOnInit(): void {
        this.getSelectedPcId();
        this.loadResourceMetrics();
        this.loadAlerts();
    }

    loadResourceMetrics() {
        this.resourceService.getResourceMetrics(this.pcId).subscribe((data: ResourceMetricsModel) => {
            this.resourceMetrics = data;
            this.resourceMetrics.cpu_percentage_use = this.roundDecimal(this.resourceMetrics.cpu_percentage_use, 2);
            this.resourceMetrics.ram_percentage_in_use = this.roundDecimal(this.resourceMetrics.ram_percentage_in_use, 2);
            this.resourceMetrics.disk_percentage_in_use = this.roundDecimal(this.resourceMetrics.disk_percentage_in_use, 2);
            this.resourceMetrics.total_memory = this.roundDecimal(this.convertBytesToGigaBytes(this.resourceMetrics.total_memory), 2);
            this.resourceMetrics.free_memory = this.roundDecimal(this.convertBytesToGigaBytes(this.resourceMetrics.free_memory), 2);
            this.resourceMetrics.total_disk_space = this.roundDecimal(this.convertBytesToGigaBytes(this.resourceMetrics.total_disk_space), 2);
            this.resourceMetrics.free_disk_space = this.roundDecimal(this.convertBytesToGigaBytes(this.resourceMetrics.free_disk_space), 2);
        })
    }

    convertBytesToGigaBytes(valueInBytes: number): number {
        return (valueInBytes / 1000 / 1000 / 1000);
    }

    roundDecimal(num: number, places: number): number {
        return Math.round((num + Number.EPSILON) * Math.pow(10, places)) / Math.pow(10, places);
    }

    loadAlerts() {
        // TODO: add data pipe here
        this.alertService.getAlerts(this.pcId, this.datePipe.transform(Date.now() - Date.now(), 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(Date.now(), 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe(data => {
            this.alerts = data;
        })
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
