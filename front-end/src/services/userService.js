import httpClient from './httpClient';

const END_POINT = '/user';

const logIn = (obj) => httpClient.post(`${END_POINT}/login`, obj);

export {
    logIn,
}