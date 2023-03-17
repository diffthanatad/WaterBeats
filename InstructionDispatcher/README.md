# Instruction Dispatcher Service
Hello and welcome to the Instruction Dispatcher service. This is one of the three services that are located in the IoT Base Station, in the original system architecture design.
\
\
The main functionality of these component is to listen for the request from the web back-end service that is running in the Farmer PC. This request is initiated from the user whenever they want to send an immediate command to the actuator such as turn on the sprinkler with id = 45 and water the plant for 3 minutes.

## Run
```bash
npm install --save
npm run start
```

## API Endpoint
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| GET | /api | Default route which tell the service name and version number |
| POST | /api/instruction | Send an instruction to the actuator. |

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