import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {MainPageComponent} from "./main-page/main-page.component";
import {OverviewComponent} from "./overview/overview.component";
import {SingleProcessComponent} from "./single-process/single-process.component";
import {RamComponent} from "./ram/ram.component";
import {CpuComponent} from "./cpu/cpu.component";
import {DiskComponent} from "./disk/disk.component";
import {NetworkComponent} from "./network/network.component";
import {LoginComponent} from "./login/login.component";

const routes: Routes = [
  { path: '', component: MainPageComponent},
  { path: 'main', component: MainPageComponent},
  { path: 'overview', component: OverviewComponent},
  { path: 'processes', component: SingleProcessComponent},
  { path: 'ram', component: RamComponent},
  { path: 'cpu', component: CpuComponent},
  { path: 'disk', component: DiskComponent},
  { path: 'network', component: NetworkComponent},
  { path: 'login', component: LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
