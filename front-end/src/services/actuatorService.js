import httpClient from './httpClient';

const END_POINT = '/actuator';

const getAllActuatorDetail = () => httpClient.get(`${END_POINT}`);

const getActuatorByType = (deviceType) => httpClient.get(`${END_POINT}/latestByType&type=${deviceType}`);

export {
    getAllActuatorDetail,
    getActuatorByType,
}