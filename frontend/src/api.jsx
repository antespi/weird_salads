import axios from 'axios';
import { getUserIdSession } from './auth';

function _getUserId() {
  const user_id = getUserIdSession();
  return user_id;
}

let instance = axios.create({
  baseURL: `http://localhost:8000/api/`,
  headers: {'X-User-Id': _getUserId()}
});

export default instance;
