import { Component, OnInit } from '@angular/core';

export class NetworkInterfaceModel {
  displayName: String = "Killer E2600 Gigabit";
  name: String = "eth8";
  ip4: String = "192.168.98.1";
  ip6: String = "fe80:0:0:0:b1dd:b439:f225:996f";
  mac: String = "00:50:56:c0:00:03";
  subnetMask: Number = 24;
  bytesReceived: Number = 0;
  bytesSent: Number = 6210;
  packetsReceived: Number = 0;
  packetsSent: Number = 0;
}

export class ConnectionModel {
  timestamp: String = "1688714155432";
  localPort: String = "49410";
  foreignAddress: String = "20.199.120.151";
  foreignPort: String = "443";
  state: String = "ESTABLISHED";
  type: String = "tcp4";
}

export class NetworkModel {
  networkInterfaces: NetworkInterfaceModel[] = [];
  connections: ConnectionModel[] = [];
  alerts: String[] = ["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];
}
@Component({
  selector: 'app-network',
  templateUrl: './network.component.html',
  styleUrls: ['./network.component.scss']
})
export class NetworkComponent implements OnInit {

  network: NetworkModel = new NetworkModel();

  ngOnInit() {
    this.init();
  }

  init() {
    this.network.networkInterfaces.push(new NetworkInterfaceModel());
    this.network.networkInterfaces.push(new NetworkInterfaceModel())
    this.network.connections.push(new ConnectionModel());
    this.network.connections.push(new ConnectionModel());
  }

}
