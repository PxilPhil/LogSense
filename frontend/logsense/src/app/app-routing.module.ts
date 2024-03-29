import {NgModule} from '@angular/core';
import {PreloadAllModules, RouterModule, Routes} from '@angular/router';
import {OverviewComponent} from "./overview/overview.component";
import {CpuComponent} from "./cpu/cpu.component";
import {SingleProcessesComponent} from "./single-processes/single-processes.component";
import {RamComponent} from "./ram/ram.component";
import {DiskComponent} from "./disk/disk.component";
import {NetworkComponent} from "./network/network.component";
import {CustomAlertsComponent} from "./custom-alerts/custom-alerts.component";
import {PcSelectionComponent} from "./pc-selection/pc-selection.component";

const routes: Routes = [
  {path: '', component: OverviewComponent},
  {path: 'overview', component: OverviewComponent},
  {path: 'cpu', component: CpuComponent},
  {path: 'processes', component: SingleProcessesComponent},
  {path: 'ram', component: RamComponent},
  {path: 'disk', component: DiskComponent},
  {path: 'network', component: NetworkComponent},
  {path: 'alerts', component: CustomAlertsComponent},
  {path: 'pc_selection', component: PcSelectionComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {preloadingStrategy: PreloadAllModules})],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
