import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { jwtDecode } from 'jwt-decode';
import { LOCAL_STORAGE_KEY } from '../constants/local-storage-keys';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { LoginForm } from '../models/ui/login/LoginForm';
import { BasicUserInfo } from '../models/BasicUserInfo';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private router: Router, private http: HttpClient) {}

  setToken(token: string) {
    localStorage.setItem(LOCAL_STORAGE_KEY.ACCESS_TOKEN, token);
  }

  getToken(): string | null {
    return localStorage.getItem(LOCAL_STORAGE_KEY.ACCESS_TOKEN);
  }

  getUserInfoFromToken(): BasicUserInfo | null {
    const token = localStorage.getItem(LOCAL_STORAGE_KEY.ACCESS_TOKEN);
    if (!token) return null;

    try {
      const decoded: any = jwtDecode(token);
      const userInfo: BasicUserInfo = {
        username: decoded.sub,
        uid: decoded.uid,
      };
      return userInfo;
    } catch (e) {
      console.error('Invalid token', e);
      return null;
    }
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const decoded: any = jwtDecode(token);
      const now = Date.now().valueOf() / 1000;
      if (decoded.exp === undefined) return true;
      return decoded.exp > now;
    } catch {
      return false;
    }
  }

  login(loginData: LoginForm): Observable<any> {
    const body = new URLSearchParams();
    body.set('grant_type', 'password');
    body.set('username', loginData.username);
    body.set('password', loginData.password);
    body.set('scope', '');
    body.set('client_id', '');
    body.set('client_secret', '');

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
    });

    return this.http.post<any>(
      `${environment.apiUrl}/auth/login`,
      body.toString(),
      { headers }
    );
  }

  logOut() {
    localStorage.removeItem(LOCAL_STORAGE_KEY.ACCESS_TOKEN);
    this.router.navigate(['/login']);
  }
}
