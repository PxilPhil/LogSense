import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, tap} from 'rxjs';
import {Alert, UserAlert, UserAlertRoot} from "../model/Alert";

@Injectable({
  providedIn: 'root'
})

export class AlertService { // service used to get alerts from the api and then save them in this service
  private alerts: Alert[] = [];

  constructor(private httpClient: HttpClient) { }

  getAlerts(pc_id: number, start: string, end: string): Observable<Alert[]> {
    const url: string = `http://localhost:8000/alerts/${pc_id}?start=${start}&end=${end}`;
    return this.httpClient.get<Alert[]>(url).pipe(
      tap((fetchedAlerts) => {
        this.alerts = fetchedAlerts;
      })
    );
  }

  getAllUserAlerts(user_id: number): Observable<UserAlertRoot> {
    const url: string = `http://localhost:8000/alerts/all/${user_id}`;
    return this.httpClient.get<UserAlertRoot>(url);
  }

  postUserAlert(userAlert: UserAlert): Observable<any> {
    const url: string = `http://localhost:8000/alerts/`;
    return this.httpClient.post(url, userAlert); //todo: api requires array, remove later if it's fixed in the api
  }

  deleteUserAlert(id: number): Observable<any> {
    const url: string = `http://localhost:8000/alerts/${id}`
    return this.httpClient.delete(url);
  }

  getStoredAlerts(application_name?: string, columns?: string[]): Alert[] {
    return this.alerts.filter((alert) => {
      if (application_name && columns && columns.length > 0) {
        return alert.application === application_name && columns.includes(alert.column);
      } else if (application_name && columns && columns.length === 0) {
        return alert.application === application_name;
      } else if (!application_name && columns && columns.length > 0) {
        return columns.includes(alert.column);
      } else {
        return true;
      }
    });
  }
}
