import {Injectable} from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class SelectedPcService {
    selectedPcId: number | null = null;

    getSelectedPcId(): number | null {
        return this.selectedPcId;
    }

    setSelectedPcId(selectedPcId: number) {
        this.selectedPcId = selectedPcId;
    }
}
