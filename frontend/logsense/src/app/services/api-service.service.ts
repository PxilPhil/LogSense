import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {PCData} from '../model/PCData';

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  constructor(private http: HttpClient) {
    console.log('ApiService constructor called');
  }

  // Gets TimeSeries data for pc, filterd by type (RAM/CPU), including analyzed things
  getPCData(pc_id: number, type: string, start: string, end: string): Observable<PCData> {
    const url = `http://localhost:8000/pc/${pc_id}/data/${type}?start=${start}&end=${end}`;
    return this.http.get<PCData>(url);
  }
}
