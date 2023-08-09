import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Alert} from "../model/Alert";

@Injectable({
  providedIn: 'root'
})

export class AlertService {
  constructor(private httpClient: HttpClient) {
  }

  getAlerts(): Observable<Alert[]> {
    const url: string = `http://localhost:8000/alerts`;
    return this.httpClient.get<Alert[]>(url);
  }
}
