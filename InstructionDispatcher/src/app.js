require('dotenv').config();

const express = require("express");
const app = express();

/* Timezone configuration to United Kingdoms using moment.js library. */
const moment = require('moment')
moment.locale('uk')

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/* API routes */
require("./routes/default.routes")(app);
require("./routes/instruction.routes")(app);

module.exports = app;