import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";


@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})
export class ToolbarComponent implements OnInit {
  showBar: boolean = true

  constructor(private router: Router) {
  }

  ngOnInit(): void {
    this.router.events.subscribe((val) => {
      if (this.router.url === '/login') {
        this.showBar = false;
      } else {
        this.showBar = true;
      }
    });
  }
}
