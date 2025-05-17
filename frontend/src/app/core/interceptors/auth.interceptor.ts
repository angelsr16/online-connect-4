import { HttpInterceptorFn } from '@angular/common/http';
import { LOCAL_STORAGE_KEY } from '../constants/local-storage-keys';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem(LOCAL_STORAGE_KEY.ACCESS_TOKEN);
  if (token) {
    const cloned = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${token}`),
    });
    return next(cloned);
  }
  return next(req);
};
