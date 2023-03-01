module.exports = app => {
    var pjson = require('../../package.json');

    var router = require("express").Router();

    router.get('/', (req, res) => res.status(200).send({
        message: `Authentication Gateway Service (V ${pjson.version}).`
    }));

    app.use('/api', router);
};