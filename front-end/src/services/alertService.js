import axios from "axios";

const httpClient = axios.create({
    baseURL: process.env.VUE_APP_SERVICE_URL_RULE,
    timeout: process.env.VUE_APP_TIMEOUT  || 6000, /* Default timeout of 6 seconds */
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