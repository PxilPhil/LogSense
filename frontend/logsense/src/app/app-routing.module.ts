import {NgModule} from '@angular/core';
import {PreloadAllModules, RouterModule, Routes} from '@angular/router';
import {OverviewComponent} from "./overview/overview.component";
import {LoginComponent} from "./login/login.component";
import {CpuComponent} from "./cpu/cpu.component";
import {SingleProcessesComponent} from "./single-processes/single-processes.component";
import {RamComponent} from "./ram/ram.component";
import {DiskComponent} from "./disk/disk.component";
import {NetworkComponent} from "./network/network.component";
import {CustomAlertsComponent} from "./custom-alerts/custom-alerts.component";

const routes: Routes = [
  {path: '', component: OverviewComponent},
  {path: 'overview', component: OverviewComponent},
  {path: 'login', component: LoginComponent},
  {path: 'cpu', component: CpuComponent},
  {path: 'processes', component: SingleProcessesComponent},
  {path: 'ram', component: RamComponent},
  {path: 'disk', component: DiskComponent},
  {path: 'network', component: NetworkComponent},
  {path: 'alerts', component: CustomAlertsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {preloadingStrategy: PreloadAllModules})],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
