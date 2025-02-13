import { CommonAPIService } from './CommonHandler';

export class UserAPIService {
  constructor() {
    this.CommonAPIService = new CommonAPIService();
  }

  getUserList(router) {
    const url = '/api/users';
    return this.CommonAPIService.getCall(url, '', router);
  }

  createUser(parms, router) {
    const url = '/api/users';
    return this.CommonAPIService.postCall(url, parms, router);
  }

  getUserById(user_id, router) {
    const url = `/api/users/${user_id}`;
    return this.CommonAPIService.getCall(url, '', router);
  }

  updateUser(user_id, parms, router) {
    const url = `/api/users/${user_id}`;
    return this.CommonAPIService.putCall(url, parms, router);
  }

  resetPassword(parms, router) {
    const url = `/api/auth/reset`;
    return this.CommonAPIService.postCall(url, parms, router);
  }

  changePassword(parms, router) {
    const url = `/api/auth/change`;
    return this.CommonAPIService.postCall(url, parms, router);
  }
}

export default UserAPIService;
