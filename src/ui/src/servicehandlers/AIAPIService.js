import { CommonAPIService } from './CommonHandler';

export class UserAPIService {
  constructor() {
    this.CommonAPIService = new CommonAPIService();
  }

  sendMessage(message, router){
    const url = `/api/generate`
    this.CommonAPIService.postCall(url, message, router)
  }
}

export default UserAPIService;
