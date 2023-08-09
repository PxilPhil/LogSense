import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {PCData} from "../model/PCData";

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
}
