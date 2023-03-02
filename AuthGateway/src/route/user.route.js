module.exports = app => {
    const { body, param } = require('express-validator');

    const { authJwt } = require("../middleware");

    const user = require("../controller/user.controller");

    var router = require("express").Router();

    router.get(
        "/single/:username",
        [
            authJwt.verifyToken,
            param('username', "No username provided.").notEmpty(),
        ],
        user.getOneByUsername
    );

    router.get(
        "/pagination",
        [
            authJwt.verifyToken,
            authJwt.isAdmin,
        ],
        user.getByUsernameWithPagination
    );

    router.put(
        "/info",
        [
            authJwt.verifyToken,
            authJwt.isAdmin,
            body('id', "No id provided.").notEmpty().isInt(),
            body('name', "No name provided.").notEmpty(),
            body('username', "No username provided.").notEmpty(),
            body('role', "No role provided.").isIn(['admin', 'moderator', 'user']),
            body('disable', "No disable provided.").isIn(['0', '1']),
        ],
        user.updateInfo
    );

    router.put(
        "/personal",
        [
            authJwt.verifyToken,
            body('id', "No id provided.").notEmpty().isInt(),
            body('name', "No name provided.").notEmpty(),
            body('username', "No username provided.").notEmpty(),
        ],
        user.updatePersonal
    );

    router.put(
        "/password",
        [
            authJwt.verifyToken,
            body('id', "No id provided.").notEmpty().isInt(),
            body('oldPassword', "No name provided.").notEmpty(),
            body('newPassword', "No name provided.").notEmpty(),
        ],
        user.changePassword
    );

    router.delete(
        "/:id",
        [
            authJwt.verifyToken,
            authJwt.isAdmin,
            param('id', "No id provided.").notEmpty().isInt(),
        ],
        user.deleteUser
    );

    app.use('/api/user', router)
};