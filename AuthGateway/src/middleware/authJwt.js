const jwt = require("jsonwebtoken");
const db = require("../model");
const User = db.user;
const ROLES = ["admin", "moderator", "user"]

function verifyToken(req, res, next) {
  const bearerHeader = req.headers['authorization'];

  if (typeof bearerHeader === 'undefined'){
    return res.status(401).send({
      message: "No token provided."
    });
  }

  const bearer = bearerHeader.split(' ');
  const bearerToken = bearer[1];

  jwt.verify(bearerToken, process.env.JWT_SECRET, (err, decoded) => {
    if (err) {
      return res.status(401).send({
        message: "Unauthorized, invalid token."
      });
    }
    req.userId = decoded.id;
    next();
  });
}

async function isAdmin(req, res, next) {
  const user = await User.findByPk(req.userId)
  const role = user.role;

  if (role === ROLES[0]) {
    next();
    return;
  }

  res.status(403).send({
    message: `Require ${ROLES[0]} role.`
  });
  return;
};

module.exports = {
  verifyToken,
  isAdmin,
};