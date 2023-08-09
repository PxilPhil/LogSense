import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {NetworkData} from "../model/NetworkData";

@Injectable({
  providedIn: 'root'
})

export class NetworkDataService {
  constructor(private httpClient: HttpClient) {
  }

  getNetworkData(pc_id: number): Observable<NetworkData> {
    const url: string = `http://localhost:8000/pc/${pc_id}/network`;
    return this.httpClient.get<NetworkData>(url);
  }
}
