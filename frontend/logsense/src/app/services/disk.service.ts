import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {DiskData, DiskStore} from "../model/DiskData";
import {DiskForecastData} from "../model/DiskForecastData";
import {TimeSeriesData} from "../model/PCData";

@Injectable({
  providedIn: 'root'
})

export class DiskDataService {
  constructor(private httpClient: HttpClient) {
  }

  getDiskStores(pc_id: number): Observable<DiskData> {
    const url: string = `http://localhost:8000/pc/${pc_id}/disks-partitions`;
    return this.httpClient.get<DiskData>(url);
  }

  getDiskTimeseriesData(pc_id: number, start: string, end: string): Observable<TimeSeriesData[]> {
    const url: string = `http://localhost:8000/pc/${pc_id}/disk?start=${start}&end=${end}`;
    return this.httpClient.get<TimeSeriesData[]>(url);
  }

  getForecastedFreeDiskSpace(pc_id: number, days: number): Observable<DiskForecastData> {
    const url: string = `http://localhost:8000/pc/${pc_id}/data/forecast/${days}`;
    return this.httpClient.get<DiskForecastData>(url);
  }
}
