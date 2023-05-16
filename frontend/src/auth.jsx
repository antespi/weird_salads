import axios from 'axios';

export default axios.create({
  baseURL: `http://localhost:8000/api/`,
});

export function setUserIdSession(userId) {
  sessionStorage.setItem('user_id', userId);
}

export function getUserIdSession() {
  return sessionStorage.getItem('user_id');
}

export function logout() {
  sessionStorage.removeItem('user_id');
  window.location.reload();
}
