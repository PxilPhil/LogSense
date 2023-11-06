import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {CommonModule, DatePipe, NgOptimizedImage} from "@angular/common";

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {MainPageComponent} from './main-page/main-page.component';
import {ToolbarComponent} from './toolbar/toolbar.component';
import {HeaderComponent} from './header/header.component';
import {OverviewComponent} from './overview/overview.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatIconModule} from "@angular/material/icon";
import {LoginComponent} from './login/login.component';
import {CpuComponent} from './cpu/cpu.component';
import {SingleProcessesComponent} from './single-processes/single-processes.component';
import {MatFormFieldModule} from "@angular/material/form-field";
import {FormsModule} from '@angular/forms';
import {MatInputModule} from "@angular/material/input";
import {RamComponent} from './ram/ram.component';
import {DiskComponent} from './disk/disk.component';
import {NetworkComponent} from './network/network.component';
import {MatDialogModule} from "@angular/material/dialog";
import {PartDialogComponent} from './part-dialog/part-dialog.component';
import {HttpClientModule} from '@angular/common/http';
import {MatDividerModule} from "@angular/material/divider";
import {CustomAlertsComponent} from './custom-alerts/custom-alerts.component';
import {TimeMetricsComponent} from './time-metrics/time-metrics.component';
import {AlertsComponent} from './alerts/alerts.component';
import {MatRadioModule} from "@angular/material/radio";
import {PcSelectionComponent} from './pc-selection/pc-selection.component';
import {AlertModule} from "@coreui/angular"; // Import HttpClientModule

@NgModule({
    declarations: [
        AppComponent,
        MainPageComponent,
        ToolbarComponent,
        HeaderComponent,
        OverviewComponent,
        DashboardComponent,
        LoginComponent,
        CpuComponent,
        SingleProcessesComponent,
        RamComponent,
        DiskComponent,
        NetworkComponent,
        PartDialogComponent,
        CustomAlertsComponent,
        TimeMetricsComponent,
        AlertsComponent,
        PcSelectionComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        CommonModule,
        BrowserAnimationsModule,
        MatIconModule,
        MatFormFieldModule,
        FormsModule,
        MatInputModule,
        MatDialogModule,
        HttpClientModule,
        MatDividerModule,
        MatRadioModule,
        NgOptimizedImage,
        AlertModule
    ],
    providers: [DatePipe],
    bootstrap: [AppComponent]
})
export class AppModule {
}
