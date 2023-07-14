import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {MainPageComponent} from "./main-page/main-page.component";
import {OverviewComponent} from "./overview/overview.component";
import {LoginComponent} from "./login/login.component";

const routes: Routes = [
  //{ path: '', component: MainPageComponent},
  //{ path: 'main', component: MainPageComponent},
  //{ path: 'overview', component: OverviewComponent},
  //{ path: 'login', component: LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
