import {Component, OnInit} from '@angular/core';
import {PC} from "../model/PC";
import {PcService} from "../services/pc.service";
import {SelectedPcService} from "../services/selected-pc.service";
import {UserPC} from "../model/UserPC";

@Component({
    selector: 'app-pc-selection',
    templateUrl: './pc-selection.component.html',
    styleUrls: ['./pc-selection.component.scss']
})
export class PcSelectionComponent implements OnInit {
    pcs: PC[] = [];
    newHardwareUUID: string = "";
    newClientName: string = "";

    constructor(private pcService: PcService, private selectedPcService: SelectedPcService) {
    }

    ngOnInit(): void {
        this.loadPCs();
    }

    loadPCs() {
        this.pcService.getPCsOfUser(1 /* TODO: exchange with id of the user that is logged in */).subscribe((pcList) => {
            this.pcs = pcList.pcs;
            console.log(this.pcs);
        });
    }

    selectPC(selectedPc: PC) {
        this.pcs.forEach(pc => {
            if (pc != selectedPc) {
                pc.selectedForDisplay = false;
            }
        });
        selectedPc.selectedForDisplay = true;
        this.setSelectedPcId(selectedPc.id);
    }

    addPC() {
        let userPC: UserPC = {
            user_id: 1 + "" /* TODO: exchange with id of the user that is logged in */,
            hardware_uuid: this.newHardwareUUID,
            client_name: this.newClientName,
            manufacturer: "",
            model: ""
        };

        this.pcService.addPCToUser(userPC).subscribe(() => {
            this.loadPCs();
        });
    }

    removePc(pcId: number) {
        this.pcService.removePc(pcId).subscribe(() => {
            this.loadPCs();
        });
    }

    setSelectedPcId(selectedPcId: number) {
        this.selectedPcService.setSelectedPcId(selectedPcId);
    }
}
