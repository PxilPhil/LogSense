import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ResourceMetricsModel} from "../model/ResourceMetrics";
import {CPUGeneral} from "../model/Cpu";


@Injectable({
  providedIn: 'root'
})
export class CpuService {

  constructor(private httpClient: HttpClient) { }

  getGeneral(pc_id: number): Observable<CPUGeneral> {
    const url: string = `http://127.0.0.1:8000/pc/general_specs/${pc_id}`;
    return this.httpClient.get<CPUGeneral>(url);
  }
}
