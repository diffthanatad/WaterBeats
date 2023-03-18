var clients = {};

function addValueToList(key, value) {
    if (!key) { return; }

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
    if (!key || !(key in clients)) { return null; }
    
    const firstItem = clients[key].shift();
    return firstItem;
}

function removeKey(key) {
    delete clients[key];
    return;
}

function resetClients() {
    for (const key in clients) {
        delete clients[key];
    }
}

module.exports = {
    addValueToList,
    connectionExist,
    getFirstValue,
    removeAndReturnFirstValue,
    removeKey,
    resetClients,
}