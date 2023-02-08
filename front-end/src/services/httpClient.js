import axios from "axios";
import store from '@/store'

const httpClient = axios.create({
    baseURL: process.env.VUE_APP_SERVICE_URL,
    timeout: 6000, /* 6 seconds before timeout */
    headers: {
        "Content-Type": "application/json",
    }
});

const authInterceptor = () => {
    store.dispatch("loading/start");
}

const errorInterceptor = error => {
    /*  check if it's a server error */
    if (!error.response) {
        console.error("Service httpClient, errorInterceptor, server error:", error, "\n");
        store.dispatch("loading/finish");
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

    store.dispatch("loading/finish");
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

    store.dispatch("loading/finish");
    return response;
}

httpClient.interceptors.request.use(authInterceptor);
httpClient.interceptors.response.use(responseInterceptor, errorInterceptor);

export default httpClient;