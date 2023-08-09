export class DiskForecastData {
  pc: number = 0;
  days: number = 0;
  final_timestamp: Date = new Date();
  data_list: DiskForecastDataPoint[] = [];
}

export class DiskForecastDataPoint {
  LinearRegression: number = 0;
  datetime: Date = new Date();
}
