import { Component } from '@angular/core';

export class NetworkInterfaceModel {
  displayName: String;
  name: String;
  ip4: String;
  ip6: String;
  mac: String;
  subnetMask: Number;
  bytesReceived: Number;
  bytesSent: Number;
  packetsReceived: Number;
  packetsSent: Number;
}
@Component({
  selector: 'app-network',
  templateUrl: './network.component.html',
  styleUrls: ['./network.component.scss']
})
export class NetworkComponent {

}
