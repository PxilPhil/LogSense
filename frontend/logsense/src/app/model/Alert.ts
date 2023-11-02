export interface Alert {
  type: string;
  message: string;
  severity_level: number;
  column: string;
  application?: string | null;
  detected_alert_list: Date[];
}

export interface UserAlertRoot {
  custom_alert_list: UserAlert[]
}

export interface UserAlert {
  id: number;
  user_id: number;
  type: string;
  message: string;
  severity_level: number;
  conditions: Condition[];
}

export interface Condition {
  percentage_trigger_value: number | null;
  absolute_trigger_value: number | null;
  operator: string;
  column: string;
  application: string | null;
  detect_via_moving_averages: boolean;
}
