import axios from "axios";

const httpClient = axios.create({
    baseURL: process.env.VUE_APP_SERVICE_URL,
    timeout: process.env.VUE_APP_TIMEOUT  || 6000, /* Default timeout of 6 seconds */
    headers: {
        "Content-Type": "application/json"
    }
});

const getAuthToken = () => localStorage.getItem('jwt');

const authInterceptor = (config) => {
    config.headers['Authorization'] = `Bearer ${getAuthToken()}`;
    return config;
}

const errorInterceptor = error => {
    console.log(error);
    /*  check if it's a server error */
    if (!error.response) {
        console.error("Service httpClient, errorInterceptor, server error:", error, "\n");
        return Promise.reject(error);
    }

    /* all the error responses */
    switch(error.response.status) {
        case 400:
            break;
        case 401:
            break;
        case 403:
            break;
        case 500:
            break;
        case 502:
            break;
        default:
            console.error("Service httpClient, errorInterceptor, status other status code:", error, "\n");
    }

    return Promise.reject(error);
}

const responseInterceptor = response => {
    switch(response.status) {
        case 200:
            break;
        case 201:
            break;
        case 204:
            break;
        default:
            break;
    }

    return response;
}

httpClient.interceptors.request.use(authInterceptor);
httpClient.interceptors.response.use(responseInterceptor, errorInterceptor);

export default httpClient;