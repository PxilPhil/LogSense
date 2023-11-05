import {Component, OnInit} from '@angular/core';
import {Chart, registerables} from 'chart.js';
import {CPUModel} from "../model/Cpu";
import {RAMModel} from "../model/Ram";
import {TimeModel} from "../disk/disk.component";
import {ApiService} from '../services/api-service.service';
import {ClientDetails, PCData} from '../model/PCData';
import {DiskData} from "../model/DiskData";
import {ResourceMetricsModel} from "../model/ResourceMetrics";
import {ResourceMetricsService} from "../services/resource-metrics.service";
import {AlertService} from "../services/alert.service";
import {DatePipe} from "@angular/common";
import {Alert} from "../model/Alert";
import {PCDataService} from "../services/pc-data.service";

Chart.register(...registerables);

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {

  client: ClientDetails = new ClientDetails();
  runtime: String = "2h 30min";
  resourceMetrics: ResourceMetricsModel = new ResourceMetricsModel();
  /*cpu: CPUModel = new CPUModel();
  ram: RAMModel = new RAMModel();
  disk: DiskData = new DiskData();*/
  alerts: Alert[] = []
  //selectedTime: TimeModel = {id: 1, time: "Last 24h", valueInMilliseconds: 86400000};

  /*times = [
    {id: 1, time: "Last 24h"},
    {id: 2, time: "Last Week"},
    {id: 3, time: "Last Month"},
    {id: 4, time: "Last 6 Months"},
    {id: 5, time: "Last 12 Months"},
    {id: 6, time: "All Time"}
  ];*/

  constructor(private pcDataService: PCDataService, private resourceService: ResourceMetricsService, private alertService: AlertService, private datePipe: DatePipe) {
  }

  ngOnInit(): void {
    this.loadResourceMetrics();
    this.loadClientDetails();
    this.loadAlerts();
  }

  loadClientDetails() {
    this.pcDataService.getClientDetails(1).subscribe((data: ClientDetails)=> {
      this.client = data;
      this.client.remaining_capacity=this.roundDecimal(this.client.remaining_capacity*100, 2);
    })
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

  loadAlerts() {
    // TODO: add data pipe here
    this.alertService.getAlerts(1, this.datePipe.transform(Date.now() - Date.now(), 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(Date.now(), 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe(data => {
      this.alerts=data;
    })

    console.log('alertServicee')
    console.log(this.alerts)

  }


}
