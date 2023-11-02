import {Component, OnInit} from '@angular/core';
import {AlertService} from "../services/alert.service";
import {UserAlert} from "../model/Alert";
import {switchMap} from "rxjs";

@Component({
  selector: 'app-custom-alerts',
  templateUrl: './custom-alerts.component.html',
  styleUrls: ['./custom-alerts.component.scss']
})
export class CustomAlertsComponent implements OnInit{
  searchCriteria: string = "";

  operator: string[] = ["<", "=", ">"];
  detection: string[] = ["Data Point", "Moving Averages"];
  detection_selected: string = "Moving Averages" //todo: maybe do this in a different way
  selected_from_database = false

  userAlerts: UserAlert[] = []
  selectedUserAlert: UserAlert = {
    id: 1,
    user_id: 1,
    type: "Example User Alert",
    message: "This is an example user alert.",
    severity_level: 1,
    conditions: [
      {
        percentage_trigger_value: null,
        absolute_trigger_value: 1000,
        operator: ">",
        column: "ram",
        application: "exampleApp",
        detect_via_moving_averages: true,
      }
    ],
  };

  constructor(private alertService: AlertService) {}

  ngOnInit() {
    this.loadUserAlerts();
  }

  loadUserAlerts() {
    this.alertService.getAllUserAlerts(1).subscribe(data => {
      this.userAlerts = data.custom_alert_list;
    })
  }

  selectUserAlert(userAlert: UserAlert) {
    this.selectedUserAlert = { ...userAlert };
    this.selected_from_database = true;
    if (this.selectedUserAlert.conditions[0].detect_via_moving_averages) {
      this.detection_selected="Moving Averages"
    } else {
      this.detection_selected="Data Point"
    }
  }

  postUserAlert() {
    if (this.selected_from_database) {
      this.alertService
        .deleteUserAlert(this.selectedUserAlert.id)
        .pipe(
          switchMap(() => this.alertService.postUserAlert(this.selectedUserAlert))
        )
        .subscribe(() => {
          this.discardSelection()
          this.loadUserAlerts();
        });
    } else {
      this.alertService.postUserAlert(this.selectedUserAlert).subscribe(() => {
        this.discardSelection()
        this.loadUserAlerts();
      });
    }
  }

  deleteUserAlert() {
    if (this.selected_from_database) {
      this.alertService.deleteUserAlert(this.selectedUserAlert.id).subscribe(() => {
        this.discardSelection();
        this.loadUserAlerts();
      });
    }
  }

  discardSelection() {
    this.selected_from_database = false;
    this.selectedUserAlert = {
      id: 1,
      user_id: 1,
      type: "Example User Alert",
      message: "This is an example user alert.",
      severity_level: 1,
      conditions: [
        {
          percentage_trigger_value: null,
          absolute_trigger_value: 1000,
          operator: ">",
          column: "ram",
          application: "exampleApp",
          detect_via_moving_averages: true,
        }
      ],
    };
  }
}
