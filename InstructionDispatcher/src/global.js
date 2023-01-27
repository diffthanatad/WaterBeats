var tasks = [];
var reports = [];
// var clients = new Map();
var clients = {};

/*
    {
        "1": ["watering", "off"]
        "2": ["pumping", "off"]
    }
*/

// RPi:
//     Edge computing
//     instruction dispatcher
//     data Buffer
//     redis

/*
    send to actuator
        confirm -> done
        unconfirm -> data buffer
    
    GET /instruction?actuatorId=1&timestamp=2023-10-22
    actuatorId_1 = 1row
    redis = 300 rows;


    receive instruction from POST API
    send redis
    websocket:
        pull the 
        send instructionto actuator
        
*/

function addValueToList(key, value) {
    clients[key] = clients[key] || [];

    if (value) {
        clients[key].push(value);
    }
}

function connectionExist(key) {
    return key in clients;
}

function getFirstValue(key) {
    if (clients[key]) {
        return clients[key][0];
    } else {
        return null;
    }
}

function removeAndReturnFirstValue(key) {
    return clients[key].shift();
}

function removeKey(key) {
    delete clients[key];
    return;
}

module.exports = {
    tasks,
    clients,
    addValueToList,
    connectionExist,
    getFirstValue,
    removeAndReturnFirstValue,
    removeKey,
}