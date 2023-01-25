require('dotenv').config();

const app = require("./app.js");
const SocketServer = require('ws').Server;

const PORT = process.env.PORT || 9090;
var server = app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});

/* websocket connection */
const wss = new SocketServer({ server });

//init Websocket ws and handle incoming connect requests
wss.on('connection', function connection(ws) {
    console.log("connection ...");

    //on connect message
    ws.on('message', function incoming(message) {
        console.log('received: %s', message);
        connectedUsers.push(message);
    });

    ws.send('message from server at: ' + new Date());
});