require('dotenv').config();

const app = require("./app.js");
const SocketServer = require('ws').Server;
const GLOBAL = require("./global.js");
const PENDING_INSTRUCTION = {};

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
  const sendInstructionInterval = setInterval(async () => {
    // console.log("setInterval", actuatorId, ws.readyState);

    var firstTask = GLOBAL.removeAndReturnFirstValue(actuatorId);
    // if (!firstTask) {
    //   const response = await axios.get(`localhost:23333/instruction?actuatorId=${actuatorId}`);
    //   if (response.status === 200) {
    //     firstTask = response.data;
    //   }
    // }

    if (firstTask) {
      PENDING_INSTRUCTION[actuatorId] = firstTask;

      ws.send(JSON.stringify({
        actuatorId,
        instruction: firstTask,
      }));
      
      setTimeout(() => {
        if (actuatorId in PENDING_INSTRUCTION) {
          /* The instruction does not reached the actuator. I wil call the data buffer. */
          // axios.post()
          console.log(`Actuator does not reply ${actuatorId}`);
        }
      }, 2000)
    }
  }, 5000);

  /*
    actuator off line
    back online?
    data buffer

    accept instruction from REST API
    put into global
    websocket:
      first, check the global -> send
      second, check data buffer -> send ------- GET /instruction?actuatorId=1 give me only latest ONE. Just remove it from Redis.
    
      set 2 seconds out. Then, send the instruction to the Data buffer.
    
  */

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
    } else if (CONNECTION_TYPE === "ACKNOWLEDGEMENT") {
      delete PENDING_INSTRUCTION[actuatorId];
    } else {
      ws.send(JSON.stringify({
        error: 88,
        message: "Unknown connection type",
      }))
    }
  });

  ws.on('close', function() {
    console.log(`Connection to actuator id ${actuatorId} is closed.`);

    clearInterval(sendInstructionInterval);
    GLOBAL.removeKey(actuatorId);
  });
});

module.exports = wss;