module.exports = app => {
  const { body } = require('express-validator');
  var router = require("express").Router();

  const instruction = require("../controllers/instruction.controller.js");

  router.post(
    "/",
    [
      body('actuatorId', 'Actuator Id is in integer format.').isInt(),
      body('instruction', 'Invalid instruction').isIn(['watering', 'pumping', 'on', 'off'])
    ],
    instruction.create
  );

  app.use('/api/instruction', router);
};