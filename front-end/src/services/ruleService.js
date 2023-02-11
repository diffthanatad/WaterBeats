import httpClient from './httpClient';

const END_POINT = '/rule';

const getRuleByActuatorId = (id) => httpClient.get(`${END_POINT}?id=${id}`);

const updateRuleByActuatorId = (id, obj) => httpClient.post(`${END_POINT}?id=${id}`, obj);

export {
    getRuleByActuatorId,
    updateRuleByActuatorId,
}