module.exports = app => {
    const router = require("express").Router();
    const { authJwt } = require("../middleware");
    const { proxyRequest } = require("../controller/proxy.controller");

    router.all("/*",
        [
            authJwt.verifyToken
        ],
        proxyRequest
    );

    app.use('/', router)
}