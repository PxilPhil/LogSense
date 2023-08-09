import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA} from "@angular/material/dialog";
import {Partition} from "../model/DiskData";

@Component({
  selector: 'app-part-dialog',
  templateUrl: './part-dialog.component.html',
  styleUrls: ['./part-dialog.component.scss']
})
export class PartDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: Partition[]) {
  }
}
