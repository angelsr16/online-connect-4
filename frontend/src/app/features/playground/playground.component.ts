import { Component, HostListener, OnInit } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CommonModule } from '@angular/common';
import { PopoverModule } from 'primeng/popover';
import { AvatarModule } from 'primeng/avatar';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { BasicUserInfo } from '../../core/models/BasicUserInfo';

@Component({
  selector: 'app-playground',
  imports: [
    ButtonModule,
    CommonModule,
    PopoverModule,
    AvatarModule,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
  ],
  standalone: true,
  templateUrl: './playground.component.html',
  styleUrl: './playground.component.scss',
})
export class PlaygroundComponent {
  isSidebarExpanded: boolean = true;
  isMobile: boolean = false;
  sidebarToggle: boolean = false;

  userInfo!: BasicUserInfo | null;

  menuItems: any = [
    { label: 'Local', icon: 'assets/icons/local_icon.png', path: 'local' },
    { label: 'Online', icon: 'assets/icons/online_icon.png', path: 'online' },
    { label: 'AI', icon: 'assets/icons/ai_icon.png', path: 'ai' },
  ];

  constructor(private authService: AuthService) {
    this.userInfo = this.authService.getUserInfoFromToken();
  }

  onSignOut() {
    this.authService.logOut();
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: Event) {
    const windowWidth = window.innerWidth;
    this.isSidebarExpanded = windowWidth > 1280;
    this.isMobile = windowWidth < 640;
  }

  getSidebarWidth(): string {
    if (!this.isSidebarExpanded && this.isMobile) {
      return '0'; // Hidden on mobile
    }
    if (this.isSidebarExpanded && this.isMobile) {
      return '75%'; // Show on mobile
    }
    if (this.isSidebarExpanded && !this.isMobile) {
      return '32rem'; // Desktop full size (like w-128)
    }
    return '6rem'; // Collapsed width (like w-24)
  }

  getSidebarPadding(): string {
    if (this.isMobile && !this.isSidebarExpanded) {
      return '0';
    }
    return '1.25rem';
  }
}
