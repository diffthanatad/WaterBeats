const proxyService = require('../service/proxy.service');

function proxyRequest(req, res) {
    proxyService.proxy(req, res, (error) => {
        res.status(500).send({ message: "Error proxying request: " + error.message });
    });
}

module.exports = {
    proxyRequest,
}