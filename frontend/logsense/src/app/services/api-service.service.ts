import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { PCDataResponse } from '../models/PCData';




@Injectable({
  providedIn: 'root'
})


export class ApiService {
  constructor(private http: HttpClient) { 
    console.log('ApiService constructor called');
  }

    // Gets TimeSeries data for pc, filterd by type (RAM/CPU), including analyzed things
    getPCData(pc_id: number, type: string, start: string, end: string): Observable<PCDataResponse> {
      const url = `http://localhost:8000/pc/${pc_id}/data/${type}?start=${start}&end=${end}`;
      return this.http.get<PCDataResponse>(url);
    }

}