require('dotenv').config();

const express = require("express");
const app = express();

/* CORS configuration */
const cors = require("cors");
const corsOptions = {
    origin: process.env.CLIENT_ORIGIN,
    optionsSuccessStatus: 200
}
app.use(cors(corsOptions));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/* API routes */
require("./route/default.route")(app);
require("./route/auth.route")(app);
require("./route/user.route")(app);
// require("./route/proxy.route")(app);

/* Database configuration. Uncomment when you want to clear database and let Sequelize generate SQL create statement for you. */
const db = require("./model");
db.sequelize.sync()
/* db.sequelize.sync({ force: true }); */

module.exports = app;