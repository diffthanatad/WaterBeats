require('dotenv').config();

const { validationResult } = require('express-validator');

const authService = require("../service/auth.service");

async function signup(req, res) {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) { return res.status(400).json({ errors: errors.array() }); }

    const { name, username, password, role } = req.body;
    await authService.signUp(name, username, password, role);

    res.status(201).send();
  } catch (error) {
    res.status(500).send({ msg: error });
  }
}

async function signin(req, res) {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) { return res.status(400).json({ errors: errors.array() }); }

    const { username, password } = req.body;
    const result = await authService.signIn(username, password);

    return res.status(200).send(result);
  } catch(error) {
    res.status(500).send({ message: error.message });
  }
}

module.exports = {
  signup,
  signin,
};