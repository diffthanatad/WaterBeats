import httpClient from './httpClient';

const END_POINT = '/sensor';

const getAllSensorDetail = () => httpClient.get(`${END_POINT}`);

export {
    getAllSensorDetail
}