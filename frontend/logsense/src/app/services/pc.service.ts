import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {PCs} from "../model/PCs";
import {UserPC} from "../model/UserPC";

@Injectable({
    providedIn: 'root'
})

export class PcService {
    private url: string = "http://localhost:8000/pc";

    constructor(private httpClient: HttpClient) {
    }

    getPCsOfUser(user_id: number): Observable<PCs> {
        return this.httpClient.get<PCs>(this.url + `/user/${user_id}`);
    }

    addPCToUser(userPC: UserPC): Observable<any> {
        return this.httpClient.post<any>(this.url + "/add_pc", userPC);
    }

    removePC(pcId: number): Observable<void> {
      return this.httpClient.delete<void>(`${this.url}/${pcId}`);
    }
}
