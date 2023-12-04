import {Component, OnInit} from '@angular/core';
import {AlertService} from "../services/alert.service";
import {UserAlert} from "../model/Alert";
import {switchMap} from "rxjs";
import { catchError } from 'rxjs/operators';
import {ApplicationService} from "../services/application.service";
import {DatePipe} from "@angular/common";
import {SelectedPcService} from "../services/selected-pc.service";

@Component({
  selector: 'app-custom-alerts',
  templateUrl: './custom-alerts.component.html',
  styleUrls: ['./custom-alerts.component.scss']
})
export class CustomAlertsComponent implements OnInit{
  searchCriteria: string = "";

  operator: string[] = ["<", "=", ">"];
  detection: string[] = ["Data Point", "Moving Averages"];
  applications: string [] = []
  columns: string[] = ["cpu", "ram", "free_disk_space", "partition_major_faults", "partition_minor_faults", "available_memory", "open_files"]
  detection_selected: string = "Moving Averages" //todo: maybe do this in a different way
  selected_from_database = false
  error_occured = false

  displayedAlerts: UserAlert[] = [];
  userAlerts: UserAlert[] = []
  selectedUserAlert: UserAlert = {
    id: 1,
    user_id: 1,
    type: "Example User Alert",
    message: "This is an example user alert.",
    severity_level: 1,
    conditions: [
      {
        percentage_trigger_value: 0.05,
        absolute_trigger_value: 1000,
        operator: ">",
        column: "",
        application: "",
        detect_via_moving_averages: true,
      }
    ],
  };

  pcId: number = 0;
  showPcIdAlert: boolean = true;

  constructor(private alertService: AlertService, private applicationService: ApplicationService, private selectedPcService: SelectedPcService, private datePipe: DatePipe) {}

  ngOnInit() {
    this.getSelectedPcId();
    this.loadUserAlerts();
    this.loadApplicationNames();
  }

  loadUserAlerts() {
    this.alertService.getAllUserAlerts(1).subscribe(data => {
      this.userAlerts = data.custom_alert_list;
      this.displayedAlerts = this.userAlerts;
    })
  }

  filterAlerts() {
    this.displayedAlerts = this.userAlerts;
    var tmp: UserAlert[] = [];
    for(let alert of this.displayedAlerts) {
      if(alert.type.toLowerCase().includes(this.searchCriteria.toLowerCase())) {
        tmp.push(alert);
      }
    }
    this.displayedAlerts = tmp;
  }
  selectUserAlert(userAlert: UserAlert) {
    this.error_occured = false;
    this.selectedUserAlert = { ...userAlert };
    this.selected_from_database = true;
    if (this.selectedUserAlert.conditions[0].detect_via_moving_averages) {
      this.detection_selected="Moving Averages"
    } else {
      this.detection_selected="Data Point"
    }
  }

  postUserAlert() {
    this.error_occured = false;

    //convert % value into floating points


    if (this.selected_from_database) {
      this.alertService
        .deleteUserAlert(this.selectedUserAlert.id)
        .pipe(
          switchMap(() => this.alertService.postUserAlert(this.selectedUserAlert)),
          catchError((error) => {
            console.error("Error in postUserAlert:", error);
            this.error_occured = true; // Set the error flag
            return [];
          })
        )
        .subscribe(() => {
          this.discardSelection();
          this.loadUserAlerts();
        });
    } else {
      this.alertService.postUserAlert(this.selectedUserAlert)
        .pipe(
          catchError((error) => {
            console.error("Error in postUserAlert:", error);
            this.error_occured = true; // Set the error flag
            return [];
          })
        )
        .subscribe(() => {
          this.discardSelection();
          this.loadUserAlerts();
        });
    }
  }

  deleteUserAlert() {
    this.error_occured = false;
    if (this.selected_from_database) {
      this.alertService.deleteUserAlert(this.selectedUserAlert.id).subscribe(() => {
        this.discardSelection();
        this.loadUserAlerts();
      });
    }
  }

  discardSelection() {
    this.error_occured = false;
    this.selected_from_database = false;
    this.selectedUserAlert = {
      id: 1,
      user_id: 1,
      type: "Example User Alert",
      message: "This is an example user alert.",
      severity_level: 1,
      conditions: [
        {
          percentage_trigger_value: 0.05,
          absolute_trigger_value: 1000,
          operator: ">",
          column: "",
          application: "",
          detect_via_moving_averages: true,
        }
      ],
    };
  }

  private loadApplicationNames() {
    this.applicationService.getApplicationNameList(this.pcId, this.datePipe.transform(Date.now() - Date.now(), 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "", this.datePipe.transform(Date.now(), 'yyyy-MM-ddTHH:mm:ss.SSS') ?? "").subscribe(data => {
      this.applications=data.application_list;
      //console.log(this.applications)
    })
  }

  convertPercentageToDecimal(percentageValue: string): number | null {
    percentageValue = percentageValue.trim();

    if (percentageValue.endsWith('%')) {
      const percentage = parseFloat(percentageValue.slice(0, -1));

      if (!isNaN(percentage)) {
        // Convert the percentage to a decimal by dividing by 100
        return percentage / 100;
      }
    }

    return null;
  }

  getSelectedPcId() {
    if (this.selectedPcService.getSelectedPcId() != null) {
      this.pcId = this.selectedPcService.getSelectedPcId()!;
      this.showPcIdAlert = false;
    } else {
      this.showPcIdAlert = true;
    }
  }
}
