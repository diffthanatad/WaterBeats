# Instruction Dispatcher Service
Hello and welcome to the Instruction Dispatcher service. This is one of the three services that are located in the IoT Base Station, in the original system architecture design.
\
\
The main functionality of these component is to listen for the request from the web back-end service that is running in the Farmer PC. This request is initiated from the user whenever they want to send an immediate command to the actuator such as turn on the sprinkler with id = 45 and water the plant for 3 minutes.

---

## Run
```bash
npm install --save
npm run start
```

---

## Test
* Test both HTTPS status and request/response body.
* Provide test coverage.
```bash
npm run test
```

---

## API Endpoint
| No.| HTTP Verbs | Endpoints | Action |
| --- | --- | --- | --- |
| 1. | GET | /api | Default route which tell the service name and version number |
| 2. | POST | /api/instruction | Send an instruction to the actuator. |

### 1. Default Route
```
GET localhost:9090/api/
```
- example of response body
```json
{
  "message": "Instruction Dispatcher Services (V 1.0.0).",
}
```

### 2. Send instruction to the actuator
```
POST localhost:9090/api/instruction
```
- example of request body
```json
{
  "actuatorId": "1",
  "instruction": "watering"
}
```
| HTTP status | Description |
| --- | --- |
| 200 | The instruction is successfully send. |
| 500 | The instruction is not successfully send. |

---

## Docker
### Build an Docker Image

```yaml
FROM node:16-alpine
WORKDIR /usr/src/app
COPY . .
RUN npm install
RUN npm run build

FROM node:16-alpine
WORKDIR /usr/src/app
COPY --from=0 /usr/src/app/package.json ./package.json
COPY --from=0 /usr/src/app/dist ./dist
RUN npm install --only=production
EXPOSE 9090
CMD npm start
```

```bash
docker build . -t <account_name>/<image_name>:<tag>
```

### Run an Docker Image
```yaml
version: '3'
services:
  InstructionDispatcherService:
    image: "<account_name>/<image_name>:<tag>"
    container_name: InstructionDispatcher
    ports:
      - "9090:9090"
```
```bash
docker-compose up -d
```