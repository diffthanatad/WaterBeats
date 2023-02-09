import httpClient from './httpClient';

const END_POINT = '/device';

const getLatestReadingForAllDevices = () => httpClient.get(`${END_POINT}/latest`);

export {
    getLatestReadingForAllDevices
}