import { Routes } from '@angular/router';

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
    loadComponent: () =>
      import('./features/playground/playground.component').then(
        (c) => c.PlaygroundComponent
      ),
    children: [
      {
        path: 'local',
        loadComponent: () =>
          import('./features/playground/local/local.component').then(
            (c) => c.LocalComponent
          ),
      },
      {
        path: 'online',
        loadComponent: () =>
          import('./features/playground/online/online.component').then(
            (c) => c.OnlineComponent
          ),
      },
      {
        path: 'ai',
        loadComponent: () =>
          import('./features/playground/ai/ai.component').then(
            (c) => c.AiComponent
          ),
      },
    ],
  },
];
