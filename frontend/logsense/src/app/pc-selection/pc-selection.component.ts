import { Component } from '@angular/core';
import {PC} from "../model/PC";

@Component({
  selector: 'app-pc-selection',
  templateUrl: './pc-selection.component.html',
  styleUrls: ['./pc-selection.component.scss']
})
export class PcSelectionComponent {
  userPcs: PC[] = [{id: 1, hardware_uuid: "E4A2D298-F59B-EA11-80D6-089798A075FA", client_name: "TestClient 2", manufacturer: null, model: null},
    {id: 2, hardware_uuid: "E4A2D298-F59B-EA11-80D6-089798A075FA", client_name: "Test Client Numero Dos", manufacturer: null, model: null},
    {id: 3, hardware_uuid: "E4A2D298-F59B-EA11-80D6-089798A075FA", client_name: "Test Client Numero 3", manufacturer: null, model: null},
    {id: 4, hardware_uuid: "E4A2D298-F59B-EA11-80D6-089798A075FA", client_name: "Test Client Numero 4", manufacturer: null, model: null},
    {id: 5, hardware_uuid: "E4A2D298-F59B-EA11-80D6-089798A075FA", client_name: "Test Client Numero 5", manufacturer: null, model: null},
    {id: 6, hardware_uuid: "E4A2D298-F59B-EA11-80D6-089798A075FA", client_name: "Test Client Numero 6", manufacturer: null, model: null},
    {id: 7, hardware_uuid: "E4A2D298-F59B-EA11-80D6-089798A075FA", client_name: "Test Client Numero 7", manufacturer: null, model: null}];
}
