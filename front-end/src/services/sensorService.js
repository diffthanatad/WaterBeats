import httpClient from './httpClient';

const END_POINT = '/sensor';

const getAllLatest = () => httpClient.get(`${END_POINT}/allLatest`);

const getLatestById = (id) => httpClient.get(`${END_POINT}/getLatestById?sensor_id=${id}`);

const getRecord = (id, start, end) => httpClient.get(`${END_POINT}/record?id=${id}&start=${start}&end=${end}`);

export {
    getAllLatest,
    getLatestById,
    getRecord
}