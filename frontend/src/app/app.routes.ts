import { Routes } from '@angular/router';
import { LoginPageComponent } from '../pages/login-page/login-page.component';
import { TopicsPageComponent } from '../pages/topics-page/topics-page.component';
import { PersonalPageComponent } from '../pages/personal-page/personal-page.component';
import { TopicFullViewComponent } from '../widgets/topic-full-view/topic-full-view.component';
import { authGuard } from '../guard/auth.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: LoginPageComponent,

  },
  {
    path: 'topics',
    component: TopicsPageComponent,
    canActivate: [authGuard],
    children: [
        {
          path: 'details',
          component: TopicFullViewComponent,
        },
      ],
  },
  {
    path: 'me',
    canActivate: [authGuard],
    component: PersonalPageComponent,
  },
];
