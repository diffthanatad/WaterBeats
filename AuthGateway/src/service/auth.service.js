var jwt = require("jsonwebtoken");
var bcrypt = require("bcryptjs");
require('dotenv').config();

const userRepository = require("../repository/user.repository");

async function signUp(name, username, password, role) {
  const hashPassword = bcrypt.hashSync(password, 12)

  const result = await userRepository.create(name, username, hashPassword, role);

  return result;
}

async function signIn(username, password) {
  const user = await userRepository.findOne(username);
  if (!user) { throw new Error('No user found.'); }

  if (user.disable === true) { throw new Error('Disabled, contact admin.'); }

  const passwordIsValid = bcrypt.compareSync(password, user.password);
  if (!passwordIsValid) { throw new Error('Wrong password.'); }

  const token = jwt.sign({ id: user.id, username: user.username }, process.env.JWT_SECRET, { expiresIn: "1h" });

  return {
    name: user.name,
    username: user.username,
    role: `ROLE_${user.role.toUpperCase()}`,
    accessToken: token,
  };
}

module.exports = {
  signUp,
  signIn
};