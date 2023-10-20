import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ResourceMetricsModel} from "../model/ResourceMetrics";
import {CPUGeneral, CPUStats} from "../model/Cpu";
import {PCData} from "../model/PCData";


@Injectable({
  providedIn: 'root'
})
export class CpuService {

  constructor(private httpClient: HttpClient) { }

  getGeneral(pc_id: number): Observable<CPUGeneral> {
    const url: string = `http://127.0.0.1:8000/pc/general_specs/${pc_id}`;
    return this.httpClient.get<CPUGeneral>(url);
  }

  getStats(pc_id: number, start: string, end: string): Observable<CPUStats> {
    const url: string = `http://localhost:8000/pc/${pc_id}/data?start=${start}&end=${end}`;
    return this.httpClient.get<CPUStats>(url);
  }
}
