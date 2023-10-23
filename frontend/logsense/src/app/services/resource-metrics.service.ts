import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ResourceMetricsModel} from "../model/ResourceMetrics";

@Injectable({
  providedIn: 'root'
})
export class ResourceMetricsService {

  constructor(private httpClient: HttpClient) { }

  getResourceMetrics(pc_id: number): Observable<ResourceMetricsModel> {
    const url: string = `http://127.0.0.1:8000/pc/resource_metrics/${pc_id}`;
    return this.httpClient.get<ResourceMetricsModel>(url);
  }
}
