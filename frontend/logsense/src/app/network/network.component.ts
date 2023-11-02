import {Component, OnInit} from '@angular/core';
import {NetworkDataService} from "../services/network.service";
import {NetworkData} from "../model/NetworkData";
import {Alert} from "../model/Alert";
import {AlertService} from "../services/alert.service";

@Component({
  selector: 'app-network',
  templateUrl: './network.component.html',
  styleUrls: ['./network.component.scss']
})
export class NetworkComponent implements OnInit {
  networkData: NetworkData = new NetworkData();

  constructor(private networkDataService: NetworkDataService, private alertService: AlertService) {
  }

  ngOnInit() {
    this.loadNetworkData();
    //this.loadAlerts();    //TODO: insert again when endpoint is implemented
  }

  loadNetworkData() {
    this.networkDataService.getNetworkData(1 /* TODO get dynamic pc id */).subscribe((data: NetworkData) => {
      this.networkData = data;
    });
  }

  /*
  loadAlerts(): void {
    this.alertService.getAlerts().subscribe((data: Alert[]) => {
      //this.alerts = data;
    });
  }
  */
}
