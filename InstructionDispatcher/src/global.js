var tasks = [];
var reports = [];
// var clients = new Map();
var clients = {};

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

function removeFirstValue(key) {
    clients[key].shift();
    return;
}

module.exports = {
    tasks,
    clients,
    addValueToList,
    connectionExist,
    getFirstValue,
    removeFirstValue,
}