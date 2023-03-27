const httpProxy = require('http-proxy');
require('dotenv').config();

const proxyServerBackEnd = httpProxy.createProxyServer({});
const proxyServerRuleService = httpProxy.createProxyServer({});

function proxyBackEnd(req, res, errorCallback) {
    proxyServerBackEnd.web(req, res, {
        target: process.env.BACKEND_URL || 'http://localhost:8888',
        changeOrigin: true,
    }, errorCallback);
}

function proxyServiceRuleService(req, res, errorCallback) {
    proxyServerRuleService.web(req, res, {
        target: process.env.RULE_SERVICE_URL || 'http://localhost:3001',
        changeOrigin: true,
    }, errorCallback);
}

module.exports = {
    proxyBackEnd,
    proxyServiceRuleService,
}