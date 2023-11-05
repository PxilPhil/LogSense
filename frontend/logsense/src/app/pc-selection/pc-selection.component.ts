import {Component, OnInit} from '@angular/core';
import {PC} from "../model/PC";
import {PcService} from "../services/pc.service";

@Component({
    selector: 'app-pc-selection',
    templateUrl: './pc-selection.component.html',
    styleUrls: ['./pc-selection.component.scss']
})
export class PcSelectionComponent implements OnInit {
    userPcs: PC[] = [];
    newHardwareUUID: string = "";
    newClientName: string = "";

    constructor(private pcService: PcService) {
    }

    ngOnInit(): void {
        this.pcService.getPCsOfUser(1 /* TODO: exchange with id of the user that is logged in */).subscribe((userPCs) => {
            this.userPcs = userPCs.pcs;
            this.userPcs.at(0)!.selectedForDisplay = true;
        });
    }

    selectPC(selectedPc: PC) {
        this.userPcs.forEach(pc => {
            if (pc != selectedPc) {
                pc.selectedForDisplay = false;
            }
        });
        selectedPc.selectedForDisplay = true;
    }

    addPC() {
        let userPC = {
            user_id: 1 + "", /* TODO: exchange with id of the user that is logged in */
            hardware_uuid: this.newHardwareUUID,
            client_name: this.newClientName
        };

        this.pcService.addPCToUser(userPC).subscribe((response) => {
            console.log(response.pc_id);
        });
    }
}
