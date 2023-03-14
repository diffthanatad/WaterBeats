require('dotenv').config();

const { validationResult } = require('express-validator');

const userService = require("../service/user.service");

const getPagingData = (data, page, limit) => {
    const { count: totalItems, rows: users } = data;
    const currentPage = page ? + page : 0;
    const totalPages = Math.ceil(totalItems / limit);

    return { totalItems, users, totalPages, currentPage };
};

function getPagination(page, size) {
    const limit = size ? + size : 10;
    const offset = page ? page * limit : 0;

    return { limit, offset };
};

async function getOneByUsername(req, res) {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) { return res.status(400).json({ errors: errors.array() }); }
        
        const { username } = req.params;
        const user = await userService.findOneByUsername(username);

        if (user) {
            res.status(200).send(user);
        } else {
            res.status(204).send();
        }
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
    return;
}

async function getByUsernameWithPagination(req, res) {
    try {
        const { page, size, username } = req.query;
        const { limit, offset } = getPagination(page, size);
        const result = await userService.findByUsernameWithPagination(username, limit, offset);

        if (result.count !== 0) {
            const response = getPagingData(result, page, limit);
            res.status(200).send(response);
        } else {
            res.status(204).send();
        }
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
    return;
}

async function updateInfo(req, res) {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) { return res.status(400).json({ errors: errors.array() }); }

        const { id, name, username, role, disable } = req.body;
        await userService.updateUser(id, { name, username, role, disable });

        res.status(200).send();
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
    return;
}

async function updatePersonal(req, res) {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) { return res.status(400).json({ errors: errors.array() }); }

        const { id, name, username } = req.body;
        const result = await userService.updateUser(id, { name, username });

        res.status(200).send();
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
    return;
}

async function changePassword(req, res) {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) { return res.status(400).json({ errors: errors.array() }); }

        const { id, oldPassword, newPassword } = req.body;
        await userService.changePassword(id, oldPassword, newPassword);

        res.status(200).send();
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
    return;
}

async function deleteUser(req, res) {
    try {
        const errors = validationResult(req);
        if (!errors.isEmpty()) { return res.status(400).json({ errors: errors.array() }); }

        const { id } = req.params;
        await userService.deleteUser(id);

        res.status(200).send();
    } catch (error) {
        res.status(500).send({ message: error.message });
    }
    return;
}

module.exports = {
    getOneByUsername,
    getByUsernameWithPagination,
    updateInfo,
    updatePersonal,
    changePassword,
    deleteUser,
};