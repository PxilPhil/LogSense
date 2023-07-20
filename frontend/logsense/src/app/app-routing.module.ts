import { NgModule } from '@angular/core';
import {PreloadAllModules, RouterModule, Routes} from '@angular/router';
import {MainPageComponent} from "./main-page/main-page.component";
import {OverviewComponent} from "./overview/overview.component";
import {LoginComponent} from "./login/login.component";
import {CpuComponent} from "./cpu/cpu.component";
import {SingleProcessesComponent} from "./single-processes/single-processes.component";

const routes: Routes = [
  { path: '', component: OverviewComponent},
  { path: 'overview', component: OverviewComponent},
  { path: 'login', component: LoginComponent},
  { path: 'cpu', component: CpuComponent},
  { path: 'processes', component: SingleProcessesComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {preloadingStrategy: PreloadAllModules})],
  exports: [RouterModule]
})
export class AppRoutingModule { }
