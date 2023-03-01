import httpClient from './httpClient';

const END_POINT = '/sensor';

// const getAllSensorDetail = () => httpClient.get(`${END_POINT}`);

// export {
//     getAllSensorDetail
// }

export function getAllLatest() {
    return httpClient.get(`${END_POINT}/allLatest`);
}

export function getLatestById(id){
    return httpClient.get(`${END_POINT}/getLatestById?sensor_id=` + id);
}

export function getRecord(id, start, end){
    return httpClient.get(`${END_POINT}/record?id=$` + id + '&start=$' + start + '&end=$' + end);
}