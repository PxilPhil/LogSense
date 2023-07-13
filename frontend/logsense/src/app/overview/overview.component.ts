import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {

  client: String = "Acer Nitro 5";
  runtime: String = "2h 30min";
  constructor() { }

  ngOnInit(): void {
  }

}
