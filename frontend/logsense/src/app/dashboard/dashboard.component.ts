import { Component, OnInit } from '@angular/core';

export interface Tile {
  color: string;
  cols: number;
  rows: number;
  text: string;
}
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  rowHeight: number = 64;
  gutterSize: number = 16;
  constructor() { }
  tiles: Tile[] = [
    {text: 'Host-Information', cols: 4, rows: 3, color: 'lightblue'},
    {text: 'Two', cols: 2, rows: 2, color: 'lightgreen'},
    {text: 'Three', cols: 2, rows: 2, color: 'lightpink'},
    {text: 'Four', cols: 2, rows: 5, color: '#DDBDF1'},
    {text: 'Five', cols: 2, rows: 5, color: 'lightpink'},
    {text: 'Six', cols: 4, rows: 3, color: '#DDBDF1'},
    {text: 'Seven', cols: 2, rows: 2, color: 'lightpink'},
    {text: 'Eight', cols: 2, rows: 2, color: '#DDBDF1'},
    {text: 'Nine', cols: 8, rows: 2, color: 'lightpink'},
    {text: 'Ten', cols: 4, rows: 2, color: '#DDBDF1'},

  ];
  ngOnInit(): void {
  }

}
