import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from "rxjs";
import {TimeMetrics} from "../model/TimeMetrics";

@Injectable({
  providedIn: 'root'
})
export class TimeMetricsService {

  constructor(private httpClient: HttpClient) { }

  getTimeMetrics(pc_id: number, start: string, end: string): Observable<TimeMetrics> {
    const url: string = `http://localhost:8000/pc/${pc_id}/time-metrics/?start=${start}&end=${end}`;
    return this.httpClient.get<TimeMetrics>(url);
  }

  getTimeMetricsByApplicationName(pc_id: number, app_name: string, start: string, end: string): Observable<TimeMetrics> {
    const url: string = `http://localhost:8000/pc/${pc_id}/application/${app_name}/time-metrics/?start=${start}&end=${end}`;
    return this.httpClient.get<TimeMetrics>(url);
  }

}
