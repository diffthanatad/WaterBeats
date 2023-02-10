require('dotenv').config();

const instructionService = require("../services/instruction.service");
const { validationResult } = require('express-validator');

async function create(req, res) {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const instructionObj = {
      actuatorId: req.body.actuatorId,
      instruction: req.body.instruction,
    };

    instructionService.create(instructionObj);

    res.status(200).send();
  } catch (error) {
    res.status(500).send({ msg: error });
  }

  return;
};

module.exports = {
  create
}