import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() { }

    getToken(): string | null {
      return localStorage.getItem('access_token');
    }
  
    isAuthenticated(): boolean {
      return this.getToken() !== null;
    }
}
