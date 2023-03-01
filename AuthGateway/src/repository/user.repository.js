require('dotenv').config();

const db = require("../model");
const User = db.user;

async function create(name, username, password, role) {
  await User.create({
    name,
    username,
    password,
    role,
  });

  return;
}

async function findOne(username) {
  const user = await User.findOne({
    where: { username: username }
  });

  return user;
}

async function findAndCountAll(condition, limit, offset, order, attributes) {
  const users = await User.findAndCountAll({
    attributes: attributes,
    where: condition,
    limit,
    offset,
    order: order,
  });

  return users;
}

async function findOneByUsername(username) {
  return await User.findOne({
    where: { username: username },
    attributes: { exclude: ['password', 'disable'] }
  });
}

async function updateUser(id, user) {
  return await User.update(user, { where: { id } });
}

async function findById(id) {
  return await User.findByPk(id);
}

async function deleteUser(id) {
  return await User.destroy({ where: { id } });
}

module.exports = {
  create,
  findOne,
  findAndCountAll,
  findOneByUsername,
  updateUser,
  findById,
  deleteUser,
};