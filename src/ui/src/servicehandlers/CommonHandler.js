import axios from 'axios';

export class CommonAPIService {
  constructor() {
    this.api_url = process.env.VUE_APP_API_URL;
    console.log(this.api_url)
    this.loggedIn = false;
  }

  newFileCall(url, files, router) {
    const fullUrl = this.api_url + url;
    axios.defaults.headers.common.Authorization = localStorage.getItem('token');
    return axios({
      method: 'get',
      url: fullUrl,
      responseType: 'blob',
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      if (error.response.status === 401) {
        router.push({
          path: '/login'
        });
      }
    });
  }

  // main login method for the code
  login(login, router, store, errors, jump = true) {
    axios.defaults.headers.common.Authorization = localStorage.getItem('token');
    return axios.post(`${this.api_url}/login/access-token`, {...login, grant_type: 'password'}, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
      .then((response) => {
        localStorage.setItem('token' + '', response.data.access_token);
        //store.dispatch('ADD_USER', response.data.user);
        store.dispatch('SET_LOGGED_IN', true)
        return response.data;
      })
      .catch((e) => {
        console.error(e)
        if (e.response.status === 401) {
          if (jump) {
            router.push({
              path: '/login',
            });
          }
        }
        return {success: false, msg: 'Invalid username and/or password. Please try again'};
      });
  }

  postCall(url, parameters, router) {
    axios.defaults.headers.common.Authorization = localStorage.getItem('token');
    const fullUrl = this.api_url + url;
    return axios.post(fullUrl, parameters)
      .then((response) => {
        // console.debug('postCall response', response);
        return response.data
      })
      .catch((error) => {
        if (error.response.status === 401) {
          router.push({
            path: '/login',
          });
        }
        throw error
      });
  }

  fileCall(url, files, router) {
    const fullUrl = this.api_url + url;
    return axios.post(fullUrl, files,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': localStorage.getItem('token'),
        }
      })
      .then((response) => {
      return response
      // return response.data
    })
      .catch((error) => {
        if (error.response.status === 401) {
          router.push({
            path: '/login',
          });
        }
        throw error
      });
  }

  deleteCall(url, parameters, router) {
    axios.defaults.headers.common.Authorization = localStorage.getItem('token');
    const fullUrl = this.api_url + url;
    return axios.delete(fullUrl, parameters)
      .then(response => response.data)
      .catch((error) => {
        if (error.response.status === 401) {
          router.push({
            path: '/login'
          });
        }
      });
  }

  putCall(url, parameters, router) {
    axios.defaults.headers.common.Authorization = localStorage.getItem('token');
    const fullUrl = this.api_url + url;
    return axios.put(fullUrl, parameters)
      .then(response => response.data)
      .catch((error) => {
        if (error.response.status === 401) {
          router.push({
            path: '/login'
          });
        }
        throw error;
      });
  }

  getCall(url, parameters, router) {
    axios.defaults.headers.common.Authorization = localStorage.getItem('token');
    const fullUrl = this.api_url + url;
    return axios.get(fullUrl, parameters)
      .then(response => response.data)
      .catch((error) => {
        if (error.response.status === 401) {
          router.push({
            path: '/login'
          });
        }
        // throw error
      });
  }
}

export default CommonAPIService;
