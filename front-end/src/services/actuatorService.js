import httpClient from './httpClient';

const END_POINT = '/actuator';

const getAllActuatorDetail = () => httpClient.get(`${END_POINT}`);

export {
    getAllActuatorDetail
}