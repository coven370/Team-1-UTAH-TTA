import axios from 'axios';

export class CommonAPIService {
  constructor() {
    this.api_url = process.env.VUE_APP_API_URL;
    console.log(this.api_url);
    this.loggedIn = false;
  }

  newFileCall(url, files, router) {
    const fullUrl = this.api_url + url;
    return axios({
      method: 'get',
      url: fullUrl,
      responseType: 'blob',
      headers: {
        'Authorization': localStorage.getItem('jwtToken'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
        .then((response) => {
          return response;
        })
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            router.push({ path: '/login' });
          }
        });
  }

  // Main login method for the code
  login(loginPayload, router, store, errors, jump = true) {
    return axios.post(`${this.api_url}/api/auth/login`, loginPayload, {
      headers: {
        'Authorization': localStorage.getItem('jwtToken'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
        .then((response) => {
          localStorage.setItem('jwtToken', response.data.token);
          store.dispatch('ADD_USER', response.data.user);
          store.dispatch('SET_LOGGED_IN', true);
          return response.data;
        })
        .catch((e) => {
          errors.push(e);
          if (e.response && e.response.status === 401 && jump) {
            router.push({ path: '/login' });
          }
          return { success: false, msg: 'Invalid username and/or password. Please try again' };
        });
  }

  postCall(url, parameters, router) {
    const fullUrl = this.api_url + url;
    return axios.post(fullUrl, parameters, {
      headers: {
        'Authorization': localStorage.getItem('jwtToken'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            router.push({ path: '/login' });
          }
          throw error;
        });
  }

  fileCall(url, files, router) {
    const fullUrl = this.api_url + url;
    // For file uploads, we typically use multipart/form-data
    return axios.post(fullUrl, files, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': localStorage.getItem('jwtToken'),
        'Accept': 'application/json'
      }
    })
        .then((response) => {
          return response;
        })
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            router.push({ path: '/login' });
          }
          throw error;
        });
  }

  deleteCall(url, parameters, router) {
    const fullUrl = this.api_url + url;
    return axios.delete(fullUrl, {
      headers: {
        'Authorization': localStorage.getItem('jwtToken'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      data: parameters // Use the data property to pass request body with DELETE
    })
        .then((response) => response.data)
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            router.push({ path: '/login' });
          }
        });
  }

  putCall(url, parameters, router) {
    const fullUrl = this.api_url + url;
    return axios.put(fullUrl, parameters, {
      headers: {
        'Authorization': localStorage.getItem('jwtToken'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
        .then((response) => response.data)
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            router.push({ path: '/login' });
          }
          throw error;
        });
  }

  getCall(url, parameters, router) {
    const fullUrl = this.api_url + url;
    return axios.get(fullUrl, {
      headers: {
        'Authorization': localStorage.getItem('jwtToken'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      params: parameters // Pass query parameters through the "params" property
    })
        .then((response) => response.data)
        .catch((error) => {
          if (error.response && error.response.status === 401) {
            router.push({ path: '/login' });
          }
          // Optionally handle other errors or propagate them
        });
  }
}

export default CommonAPIService;
