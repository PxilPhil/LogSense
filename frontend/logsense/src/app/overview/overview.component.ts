import { Component, OnInit } from '@angular/core';
import {Chart, Plugin, registerables} from 'chart.js';
import {CPUModel} from "../cpu/cpu.component";
import {RAMModel} from "../ram/ram.component";
import {DiskModel} from "../disk/disk.component";
import { ApiService } from '../services/api-service.service';
import { PCDataResponse } from '../models/PCData';
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
  disk: DiskModel = new DiskModel();
  alerts: String[] = ["Abnormal RAM-Spikes detected", "Memory leak possible"];
  selectedTime: String = "Last 24h";

<<<<<<< HEAD
  constructor(private apiService: ApiService) { }

=======
  times = [
    {id: 1, time: "Last 24h"},
    {id: 2, time: "Last Week"},
    {id: 3, time: "Last Month"},
    {id: 4, time: "Last 6 Months"},
    {id: 5, time: "Last 12 Months"},
    {id: 6, time: "All Time"}
  ];
  constructor() { }
>>>>>>> 5cfeaf0bca500e5e1d58d289872df5edcdbe7095

  ngOnInit(): void {
    this.timeChart();
    console.log('init')

    this.apiService.getPCData(1, 'RAM', '2023-07-25 10:20:16', '2023-08-25 10:20:16').subscribe(
      (response: PCDataResponse) => {
        console.log('Data:', response);
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }

  timeChart() {
    const data = this.getData();
    const config = new Chart("timeChart",  {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [{
          data: data.values,
          borderColor: "#2b26a8",
          backgroundColor: "#7BE1DF",
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  getData(): { labels: string[], values: number[] } {
      const labels = ['Zeitpunkt 1', 'Zeitpunkt 2', 'Zeitpunkt 3']; // Beispiellabels
      const values = [75, 90, 60]; // Beispielauslastung
      return { labels, values };
  }

}
