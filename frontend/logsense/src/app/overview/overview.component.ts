import {Component, OnInit} from '@angular/core';
import {Chart, registerables} from 'chart.js';
import {CPUModel} from "../model/Cpu";
import {RAMModel} from "../model/Ram";
import {TimeModel} from "../disk/disk.component";
import {ApiService} from '../services/api-service.service';
import {PCData} from '../model/PCData';
import {DiskData} from "../model/DiskData";
import {ResourceMetricsModel} from "../model/ResourceMetrics";
import {ResourceMetricsService} from "../services/resource-metrics.service";

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
  alerts: String[] = ["Abnormal RAM-Spikes detected", "Memory leak possible"];
  //selectedTime: TimeModel = {id: 1, time: "Last 24h", valueInMilliseconds: 86400000};

  /*times = [
    {id: 1, time: "Last 24h"},
    {id: 2, time: "Last Week"},
    {id: 3, time: "Last Month"},
    {id: 4, time: "Last 6 Months"},
    {id: 5, time: "Last 12 Months"},
    {id: 6, time: "All Time"}
  ];*/

  constructor(private resourceService: ResourceMetricsService) {
  }

  ngOnInit(): void {
    this.loadResourceMetrics();
  }

  loadResourceMetrics() {
    this.resourceService.getResourceMetrics(1).subscribe((data: ResourceMetricsModel) => {
      this.resourceMetrics = data;
      this.resourceMetrics.cpu_percentage_use = this.roundDecimal(this.resourceMetrics.cpu_percentage_use, 2);
      this.resourceMetrics.ram_percentage_in_use = this.roundDecimal(this.resourceMetrics.ram_percentage_in_use, 2);
      this.resourceMetrics.disk_percentage_in_use = this.roundDecimal(this.resourceMetrics.disk_percentage_in_use, 2);
      this.resourceMetrics.total_memory = this.roundDecimal(this.convertBytesToGigaBytes(this.resourceMetrics.total_memory),2);
      this.resourceMetrics.free_memory = this.roundDecimal(this.convertBytesToGigaBytes(this.resourceMetrics.free_memory),2);
      this.resourceMetrics.total_disk_space = this.roundDecimal(this.convertBytesToGigaBytes(this.resourceMetrics.total_disk_space),2);
      this.resourceMetrics.free_disk_space = this.roundDecimal(this.convertBytesToGigaBytes(this.resourceMetrics.free_disk_space),2);
    })
  }

  convertBytesToGigaBytes(valueInBytes: number): number {
    return (valueInBytes / 1000 / 1000 / 1000);
  }

  roundDecimal(num: number, places: number): number{
    return Math.round((num + Number.EPSILON) * Math.pow(10, places)) / Math.pow(10, places);
  }


}
