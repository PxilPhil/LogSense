import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {DiskData} from "../model/DiskData";

@Injectable({
  providedIn: 'root'
})

export class DiskDataService {
  constructor(private httpClient: HttpClient) {
  }

  getDiskData(pc_id: number): Observable<DiskData> {
    const url: string = `http://localhost:8000/pc/${pc_id}/disk`;
    return this.httpClient.get<DiskData>(url);
  }
}
