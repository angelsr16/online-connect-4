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
        children: [
          {
            path: '',
            loadComponent: () =>
              import(
                './features/playground/pages/online/online.component'
              ).then((c) => c.OnlineComponent),
          },
          {
            path: ':gameId',
            loadComponent: () =>
              import(
                './features/playground/pages/online/game-session.component'
              ).then((c) => c.GameSessionComponent),
          },
        ],
      },
      {
        path: 'ai',
        loadComponent: () =>
          import('./features/playground/pages/ai/ai.component').then(
            (c) => c.AiComponent
          ),
      },
      {
        path: '',
        redirectTo: '/playground/local',
        pathMatch: 'full',
      },
    ],
  },
  { path: '**', redirectTo: '/playground', pathMatch: 'full' },
];
