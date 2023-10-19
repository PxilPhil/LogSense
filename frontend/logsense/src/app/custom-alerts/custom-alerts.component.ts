import { Component } from '@angular/core';

@Component({
  selector: 'app-custom-alerts',
  templateUrl: './custom-alerts.component.html',
  styleUrls: ['./custom-alerts.component.scss']
})
export class CustomAlertsComponent {
  searchCriteria: string = "";

  severity: string[] = ["Very Low", "Low", "Medium", "High", "Very High"];
  operator: string[] = ["<=", "=", ">="];
  detection: string[] = ["Data Point", "Moving Averages"];




}
