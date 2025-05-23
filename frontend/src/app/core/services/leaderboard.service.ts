import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class LeaderboardService {
  constructor(private httpClient: HttpClient) {}

  subscribeToLeaderboard(
    onMessage: Function,
    onClose: Function,
    onError?: Function
  ) {
    const socket: WebSocket = new WebSocket(
      `${environment.apiWSUrl}/leaderboard/ws/watch`
    );

    socket.onopen = (event) => {
      // console.log(event);
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    socket.onclose = (event) => {
      onClose(event);
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return socket;
  }
}
