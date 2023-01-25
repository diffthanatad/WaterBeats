module.exports = app => {
  var pjson = require('../../package.json');

  var router = require("express").Router();

  router.get('/', (req, res) => res.status(200).send({ 
    message: `Instruction Dispatcher Services (V ${pjson.version}).`
  }));

  app.use('/api', router);
};