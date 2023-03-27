const proxyService = require('../service/proxy.service');

function proxyRequestBackEnd(req, res) {
    proxyService.proxyBackEnd(req, res, (error) => {
        res.status(500).send({ message: "Error proxying request: " + error.message });
    });
}

function proxyRequestRuleService(req, res) {
    proxyService.proxyServiceRuleService(req, res, (error) => {
        res.status(500).send({ message: "Error proxying request from Rule Service: " + error.message });
    });
}

module.exports = {
    proxyRequestBackEnd,
    proxyRequestRuleService,
}