import httpClient from './httpClient';

const END_POINT = '/rule-service/rule';

const getAllRules = () => httpClient.get(`${END_POINT}/getAllRules`);

const getRuleByActuatorId = (actuator_id) => httpClient.get(`${END_POINT}/getRuleByActuatorId?actuator_id=${actuator_id}`);

const addRule = (sensor_id, reading, relation, actuator_id, type, state, intensity, duration) => httpClient.post(
    `${END_POINT}/addRule?subject_sensor=${sensor_id}&sensor_reading=${reading}&relation=${relation}&` +
    `actuator_id=${actuator_id}&actuator_type=${type}&actuator_state=${state}&intensity=${intensity}&duration=${duration}`
);

const updateRuleByActuatorId = (sensor_id, reading, relation, actuator_id, state, intensity, duration) => httpClient.put(
    `${END_POINT}/updateRuleByActuatorId?subject_sensor=${sensor_id}&sensor_reading=${reading}&relation=${relation}&` +
    `actuator_id=${actuator_id}&actuator_state=${state}&intensity=${intensity}&duration=${duration}`
);

const deleteRuleByActuatorId = (actuator_id) => httpClient.delete(`${END_POINT}/deleteRuleByActuatorId?actuator_id=${actuator_id}`);

export {
    getAllRules,
    getRuleByActuatorId,
    addRule,
    updateRuleByActuatorId,
    deleteRuleByActuatorId
}