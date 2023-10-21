import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-alerts',
  templateUrl: './alerts.component.html',
  styleUrls: ['./alerts.component.scss']
})
export class AlertsComponent {
  @Input() alerts: String[] = [];
    //["Some devices are at their workload limit", "Abnormal CPU-Spikes detected (21 Anomalies in the last 24 hours)"];

}
