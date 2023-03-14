const bcrypt = require("bcryptjs");

const db = require("../model");
const Op = db.Sequelize.Op;

const userRepository = require("../repository/user.repository");

async function findByUsernameWithPagination(username, limit, offset) {
    var condition = {}
    if (username) { condition["username"] = { [Op.iLike]: `${username}%` }; }

    const order = [['id', 'ASC']];
    const attributes = { exclude: ['password'] }

    const result = await userRepository.findAndCountAll(condition, limit, offset, order, attributes);

    return result;
}

async function findOneByUsername(username) {
    return await userRepository.findOneByUsername(username);
}

async function updateUser(id, user) {
    return await userRepository.updateUser(id, user);
}

async function changePassword(id, oldPassword, newPassword) {
    const user = await userRepository.findById(id);
    if (!user) { throw new Error('No user found.'); }

    const passwordMatchExistingPassword = bcrypt.compareSync(oldPassword, user.password);
    if (!passwordMatchExistingPassword) { throw new Error('Wrong password.'); }

    const hashPassword = bcrypt.hashSync(newPassword, 12)
    return await userRepository.updateUser(id, { password: hashPassword });
}

async function deleteUser(id) {
    return await userRepository.deleteUser(id);
}

module.exports = {
    findByUsernameWithPagination,
    findOneByUsername,
    updateUser,
    changePassword,
    deleteUser,
};