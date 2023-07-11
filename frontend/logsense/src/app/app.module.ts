import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MainPageComponent } from './main-page/main-page.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { HeaderComponent } from './header/header.component';
import { OverviewComponent } from './overview/overview.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatGridListModule} from "@angular/material/grid-list";
import { AlertsComponent } from './alerts/alerts.component';
import { ResourceMetricsComponent } from './resource-metrics/resource-metrics.component';
import { TimeMetricsComponent } from './time-metrics/time-metrics.component';
import { SingleProcessComponent } from './single-process/single-process.component';
import { CpuComponent } from './cpu/cpu.component';
import { RamComponent } from './ram/ram.component';
import { DiskComponent } from './disk/disk.component';
import { DashboardComponent } from './dashboard/dashboard.component';



@NgModule({
  declarations: [
    AppComponent,
    MainPageComponent,
    ToolbarComponent,
    HeaderComponent,
    OverviewComponent,
    AlertsComponent,
    ResourceMetricsComponent,
    TimeMetricsComponent,
    SingleProcessComponent,
    CpuComponent,
    RamComponent,
    DiskComponent,
    DashboardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatGridListModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
