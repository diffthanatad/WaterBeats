require('dotenv').config();

const app = require("./app.js");
const SocketServer = require('ws').Server;
const GLOBAL = require("./global.js");

const PORT = process.env.PORT || 9090;
var server = app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});

/* websocket connection */
const wss = new SocketServer({ server });

// init Websocket ws and handle incoming connect requests
wss.on('connection', function connection(ws) {
  console.log("Websocket accept new connection ...");

  /* saving the metadata about this client. */
  var actuatorId = 0;

  /* Polling for the task. If task exists, then send it to the destination actuator. */
  setInterval(() => {
    const firstTask = GLOBAL.getFirstValue(actuatorId);
    // console.log(actuatorId, "firstTask:", firstTask, GLOBAL.clients);

    if (firstTask) {
      ws.send(JSON.stringify(firstTask));
      GLOBAL.removeFirstValue(actuatorId);
    }
  }, 5000);

  ws.on('message', function incoming(req) {
    /* 
      The received message is in byte array format in the buffer.
      Need to convert from byte into string format and then into JSON object.
    */
    const messageStr = new Buffer.from(req).toString();
    const message = JSON.parse(messageStr);
    const CONNECTION_TYPE = message.connectionType;
    const ID = message.actuatorId
    const isDeviceRegistered = GLOBAL.connectionExist(ID);

    if (CONNECTION_TYPE === "OPEN_CONNECTION") {
      if (isDeviceRegistered) { 
        ws.send(JSON.stringify({
          error: 66,
          message: "Duplicate actuator id in the system. This actuator id already connected to the server.",
        }))
      } else {
        actuatorId = ID;
        GLOBAL.addValueToList(ID);
      }
    } else if (CONNECTION_TYPE === "STATUS_REPORT") {
      if (isDeviceRegistered) {
        /* 
          Device is registered. Can now perform the desired tasks. 
          Need to see the business logic before can start working on this.
        */
      } else {
        ws.send(JSON.stringify({
          error: 77,
          message: "Device does not perform handshake with the server yet.",
        }))
      }
    } else {
      ws.send(JSON.stringify({
        error: 88,
        message: "Unknown connection type",
      }))
    }
  });
});

module.exports = wss;