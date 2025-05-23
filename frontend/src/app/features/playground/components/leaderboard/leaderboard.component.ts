import { Component } from '@angular/core';
import { LeaderboardService } from '../../../../core/services/leaderboard.service';
import { UserInfo } from '../../../../core/models/UserInfo';

@Component({
  selector: 'app-leaderboard',
  imports: [],
  templateUrl: './leaderboard.component.html',
  styleUrl: './leaderboard.component.scss',
})
export class LeaderboardComponent {
  usersList: UserInfo[] = [];

  constructor(private leaderboardService: LeaderboardService) {
    // this.leaderboardService.getLeaderboard().subscribe((users) => {
    //   this.usersList = users as UserInfo[];
    //   console.log(users);
    // });

    this.leaderboardService.subscribeToLeaderboard(
      (users: any) => {
        this.usersList = users as UserInfo[];
      },
      () => {}
    );
  }
}
