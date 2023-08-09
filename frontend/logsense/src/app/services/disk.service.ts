import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {DiskData} from "../model/DiskData";
import {DiskForecastData} from "../model/DiskForecastData";

@Injectable({
  providedIn: 'root'
})

export class DiskDataService {
  constructor(private httpClient: HttpClient) {
  }

  getDiskData(pc_id: number): Observable<DiskData> {
    const url: string = `http://localhost:8000/pc/${pc_id}/disk`;
    return this.httpClient.get<DiskData>(url);
  }

  getForecastedFreeDiskSpace(pc_id: number, days: number): Observable<DiskForecastData> {
    const url: string = `http://localhost:8000/pc/${pc_id}/data/forecast/${days}`;
    return this.httpClient.get<DiskForecastData>(url);
  }
}
