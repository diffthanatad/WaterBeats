module.exports = app => {
    const router = require("express").Router();
    const { authJwt } = require("../middleware");
    const proxyRequest = require("../controller/proxy.controller");

    router.all("/rule-service/*",
        [
            authJwt.verifyToken
        ],
        proxyRequest.proxyRequestRuleService
    );

    router.all("/*",
        [
            authJwt.verifyToken
        ],
        proxyRequest.proxyRequestBackEnd
    );

    app.use('/', router)
}