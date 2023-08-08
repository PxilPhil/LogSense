export class NetworkData {
  network_list: NetworkInterface[] = [];
  connection_list: IPConnection[] = [];
}

export class NetworkInterface {
  id: number = 0;
  pcdata_id: number = 0;
  name: string = "";
  display_name: string = "";
  ipv4_address: string = "";
  ipv6_address: string = "";
  subnet_mask: string = "";
  mac_address: string = "";
  bytes_received: number = 0;
  bytes_sent: number = 0;
  packets_received: number = 0;
  packets_sent: number = 0;
}

export class IPConnection {
  id: number = 0;
  pcdata_id: number = 0;
  localaddress: string = "";
  localport: number = 0;
  foreignaddress: string = "";
  foreignport: number = 0;
  state: string = "";
  type: string = "";
  owningprocessid: number = 0;
}
