module.exports = app => {
    const { body } = require('express-validator');
  
    const { authJwt } = require("../middleware");
  
    const auth = require("../controller/auth.controller");
  
    var router = require("express").Router();
  
    router.post(
      "/signup",
      [
        authJwt.verifyToken,
        authJwt.isAdmin,
        body('name', "No name provided.").notEmpty(),
        body('username', "No username provided.").notEmpty(),
        body('password', "No password provided.").notEmpty(),
        body('role', "No role provided.").isIn(['admin', 'moderator', 'user'])
      ],
      auth.signup
    );
  
    router.post(
      "/signin",
      [
        body('username', "No username provided.").notEmpty(),
        body('password', "No password provided.").notEmpty(),
      ],
      auth.signin
    );
  
    app.use('/api/auth', router)
  };