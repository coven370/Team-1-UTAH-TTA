import { CommonAPIService } from './CommonHandler';

export class UserAPIService {
  constructor() {
    this.CommonAPIService = new CommonAPIService();
  }

  sendMessage(messages, router){
    const url = `/generate/message`
    return this.CommonAPIService.aiCall(url, {messages}, router)
  }

  getReference(question, router){
    const url = `/generate/references`
    return this.CommonAPIService.aiCall(url, {messages: question}, router)
  }

  getScenario(router){
    const url = '/generate/scenario'
    return this.CommonAPIService.getAICall(url, null, router)
  }
}

export default UserAPIService;
