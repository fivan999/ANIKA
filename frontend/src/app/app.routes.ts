import { Routes } from '@angular/router';
import { LoginPageComponent } from '../pages/login-page/login-page.component';
import { TopicsPageComponent } from '../pages/topics-page/topics-page.component';
import { PersonalPageComponent } from '../pages/personal-page/personal-page.component';

export const routes: Routes = [
    {
        path: 'login',
        component: LoginPageComponent
    },
    {
        path: 'topics',
        component: TopicsPageComponent
    },
    {
        path: 'me',
        component: PersonalPageComponent
    }
];
