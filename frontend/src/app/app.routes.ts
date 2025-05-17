import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/login/login.component').then(
        (c) => c.LoginComponent
      ),
  },
  {
    path: 'playground',
    canActivate: [AuthGuard],
    loadComponent: () =>
      import('./features/playground/playground.component').then(
        (c) => c.PlaygroundComponent
      ),
    children: [
      {
        path: 'local',
        loadComponent: () =>
          import('./features/playground/pages/local/local.component').then(
            (c) => c.LocalComponent
          ),
      },
      {
        path: 'online',
        loadComponent: () =>
          import('./features/playground/pages/online/online.component').then(
            (c) => c.OnlineComponent
          ),
      },
      {
        path: 'ai',
        loadComponent: () =>
          import('./features/playground/pages/ai/ai.component').then(
            (c) => c.AiComponent
          ),
      },
    ],
  },
  { path: '**', redirectTo: '/playground', pathMatch: 'full' },
];
