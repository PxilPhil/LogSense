import {Component, Input} from '@angular/core';
import {Alert} from "../model/Alert";

@Component({
  selector: 'app-alerts',
  templateUrl: './alerts.component.html',
  styleUrls: ['./alerts.component.scss']
})
export class AlertsComponent {
  @Input() alerts: Alert[] = [];
    //["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];

}
