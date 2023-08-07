import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ApplicationNames} from "../model/ApplicationNames";
import {Application} from "../model/Application";

@Injectable({
  providedIn: 'root'
})

export class ApplicationService {
  constructor(private httpClient: HttpClient) {
  }

  getApplicationNameList(pc_id: number, start: string, end: string): Observable<ApplicationNames> {
    const url: string = `http://localhost:8000/pc/${pc_id}/application?start=${start}&end=${end}`;
    return this.httpClient.get<ApplicationNames>(url);
  }

  getApplicationByApplicationName(pc_id: number, application_name: string, start: string, end: string): Observable<Application> {
    const url: string = `http://localhost:8000/pc/${pc_id}/application/${application_name}?start=${start}&end=${end}`;
    return this.httpClient.get<Application>(url);
  }
}
