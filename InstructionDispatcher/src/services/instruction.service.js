const GLOBAL = require("../global.js");

function create(instructionObj) {
    const isDeviceRegistered = GLOBAL.connectionExist(instructionObj.actuatorId);
    if (!isDeviceRegistered) { throw new Error('Device does not exist in the connection pool yet.'); }

    GLOBAL.addValueToList(instructionObj.actuatorId, instructionObj.instruction);
    return;
}

module.exports = {
    create
}