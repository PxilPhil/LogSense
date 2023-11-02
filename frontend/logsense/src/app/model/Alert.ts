export interface Alert {
  type: string;
  message: string;
  severity_level: number;
  column: string;
  application?: string | null;
  detected_alert_list: Date[];
}
