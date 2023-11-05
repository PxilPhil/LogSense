import {Component, OnInit} from '@angular/core';
import {NetworkDataService} from "../services/network.service";
import {NetworkData} from "../model/NetworkData";
import {Alert} from "../model/Alert";
import {AlertService} from "../services/alert.service";
import {SelectedPcService} from "../services/selected-pc.service";

@Component({
  selector: 'app-network',
  templateUrl: './network.component.html',
  styleUrls: ['./network.component.scss']
})
export class NetworkComponent implements OnInit {
  networkData: NetworkData = new NetworkData();

  pcId: number = 0;
  showPcIdAlert: boolean = true;

  constructor(private networkDataService: NetworkDataService, private alertService: AlertService, private selectedPcService: SelectedPcService) {
  }

  ngOnInit() {
    this.getSelectedPcId();
    this.loadNetworkData();
  }

  loadNetworkData() {
    this.networkDataService.getNetworkData(this.pcId).subscribe((data: NetworkData) => {
      this.networkData = data;
    });
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
