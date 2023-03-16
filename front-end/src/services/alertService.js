import axios from "axios";

const httpClient = axios.create({
    baseURL: "http://localhost:3001",
    timeout: 6000, /* 6 seconds before timeout */
    headers: {
        "Content-Type": "application/json"
    }
});

const END_POINT = '/alert';

const getAllAlerts = () => httpClient.get(`${END_POINT}/getAllAlerts`);

const getAlertBySensorId = (sensor_id) => httpClient.get(`${END_POINT}/getAlertBySensorId?sensor_id=${sensor_id}`);

const addAlert = (id, type, threshold, relation) => httpClient.post(
    `${END_POINT}/addAlert?sensor_id=${id}&sensor_type=${type}&threshold=${threshold}&relation=${relation}`
);

const updateAlertBySensorId = (id, threshold, relation) => httpClient.put(
    `${END_POINT}/updateAlertBySensorId?sensor_id=${id}&threshold=${threshold}&relation=${relation}`
);

const deleteAlertBySensorId = (sensor_id) => httpClient.delete(`${END_POINT}/deleteAlertBySensorId?sensor_id=${sensor_id}`);

const sendAlert = () => httpClient.post(`${END_POINT}/sendAlert`);

export {
    getAllAlerts,
    getAlertBySensorId,
    addAlert,
    updateAlertBySensorId,
    deleteAlertBySensorId,
    sendAlert
}