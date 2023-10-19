import {Component, OnInit} from '@angular/core';
import {Chart, registerables} from 'chart.js';
import {CPUModel} from "../cpu/cpu.component";
import {RAMModel} from "../ram/ram.component";
import {TimeModel} from "../disk/disk.component";
import {ApiService} from '../services/api-service.service';
import {PCData} from '../model/PCData';
import {DiskData} from "../model/DiskData";

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
  cpu: CPUModel = new CPUModel();
  ram: RAMModel = new RAMModel();
  disk: DiskData = new DiskData();
  alerts: String[] = ["Abnormal RAM-Spikes detected", "Memory leak possible"];
  selectedTime: TimeModel = {id: 1, time: "Last 24h", valueInMilliseconds: 86400000};

  times = [
    {id: 1, time: "Last 24h"},
    {id: 2, time: "Last Week"},
    {id: 3, time: "Last Month"},
    {id: 4, time: "Last 6 Months"},
    {id: 5, time: "Last 12 Months"},
    {id: 6, time: "All Time"}
  ];

  constructor(private apiService: ApiService) {
  }

  ngOnInit(): void {
    console.log('init')

    this.apiService.getPCData(1, 'RAM', '2023-07-25 10:20:16', '2023-08-25 10:20:16').subscribe(
      (response: PCData) => {
        console.log('Data:', response);
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }

}
