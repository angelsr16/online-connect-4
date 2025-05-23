import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { LOCAL_STORAGE_KEY } from '../constants/local-storage-keys';

@Injectable({
  providedIn: 'root',
})
export class UsersService {
  constructor(private httpClient: HttpClient) {}

  subscribeToUserInfo(
    onMessage: Function,
    onClose: Function,
    onError?: Function
  ) {
    const token = localStorage.getItem(LOCAL_STORAGE_KEY.ACCESS_TOKEN);
    if (token) {
      const socket: WebSocket = new WebSocket(
        `${environment.apiWSUrl}/users/ws/watch?token=${token}`
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

    return null;
  }
}
