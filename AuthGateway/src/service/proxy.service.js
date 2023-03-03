const httpProxy = require('http-proxy');
require('dotenv').config();

const proxyServer = httpProxy.createProxyServer({});

function proxy(req, res, errorCallback) {
    proxyServer.web(req, res, {
        target: process.env.BACKEND_URL ?? 'http://localhost:8080',
        changeOrigin: true,
    }, errorCallback);
}

module.exports = {
    proxy,
}