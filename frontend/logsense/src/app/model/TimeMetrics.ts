export class TimeMetrics {
  name: string[] = [];
  total_running_time_minutes: number[] = [];
}

export class TimeMetricsModel {
  data: {name: string, total_running_time_seconds: number}[] = [];
}
