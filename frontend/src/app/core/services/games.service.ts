import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GamesService {
  constructor(private http: HttpClient) {}

  getGames() {
    return this.http.get(`${environment.apiUrl}/games`);
  }

  connectGame(
    gameId: string,
    onMessage: Function,
    onClose: Function,
    onError?: Function
  ): WebSocket {
    const socket: WebSocket = new WebSocket(
      `${environment.apiWSUrl}/games/ws/watch/${gameId}`
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

  createGame() {
    return this.http.post(`${environment.apiUrl}/games/register`, null);
  }

  joinGame(joinCode: string) {
    return this.http.post(`${environment.apiUrl}/games/join/${joinCode}`, null);
  }

  makeMovement(gameId: string, columnIndex: number) {
    return this.http.post(`${environment.apiUrl}/games/${gameId}/move`, {
      column_index: columnIndex,
    });
  }
}
