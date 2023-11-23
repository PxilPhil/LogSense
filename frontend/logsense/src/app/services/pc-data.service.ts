import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ClientDetails, PCData, TimeSeriesList} from "../model/PCData";
import {RAMModel} from "../model/Ram";
import {CPUModel} from "../model/Cpu";

@Injectable({
  providedIn: 'root'
})

export class PCDataService {
  constructor(private httpClient: HttpClient) {
  }

  getPcData(pc_id: number, start: string, end: string): Observable<PCData> {
    const url: string = `http://localhost:8000/pc/${pc_id}/data?start=${start}&end=${end}`;
    return this.httpClient.get<PCData>(url);
  }

  getTimeSeriesData(pc_id: number, start: string, end: string): Observable<TimeSeriesList> {
    const url: string = `http://localhost:8000/pc/${pc_id}/data?start=${start}&end=${end}`;
    return this.httpClient.get<TimeSeriesList>(url);
  }

  getClientDetails(pc_id: number): Observable<ClientDetails> {
    const url: string = `http://127.0.0.1:8000/pc/details/${pc_id}`;
    return this.httpClient.get<ClientDetails>(url);
  }
  getRAMData(pc_id: number, start: string, end: string):Observable<RAMModel> {
    const url: string = `http://localhost:8000/pc/${pc_id}/ram?start=${start}&end=${end}`;
    return this.httpClient.get<RAMModel>(url);
  }

  getCPUData(pc_id: number, start: string, end: string, bucketValue: string):Observable<CPUModel> {
    const url: string = `http://localhost:8000/pc/${pc_id}/cpu?start=${start}&end=${end}&bucket_value=${bucketValue}`;
    return this.httpClient.get<CPUModel>(url);
  }
}
