import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {PCList} from "../model/PCList";
import {UserPC} from "../model/UserPC";

@Injectable({
    providedIn: 'root'
})

export class PcService {
    private url: string = "http://localhost:8000/pc";

    constructor(private httpClient: HttpClient) {
    }

    getPCsOfUser(userId: number): Observable<PCList> {
        return this.httpClient.get<PCList>(`${this.url}/user/${userId}`);
    }

    addPCToUser(userPC: UserPC): Observable<void> {
        return this.httpClient.post<void>(`${this.url}/add_pc`, userPC);
    }

    removePc(pcId: number): Observable<void> {
      return this.httpClient.delete<void>(`${this.url}/${pcId}`);
    }
}
