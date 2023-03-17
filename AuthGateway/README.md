# Authenticate Gateway Service
Hello and welcome to the Authentication Gateway service or AuthGateway for short. This service is part of the Farmer PC and is responsible for authenticating all API requests that will be send to all other services in the back-end. We uses the PostgreSQL to keep the  users' detail.
\
\
There are two main functionalities for this component. First, as mentioned earlier is to authenticate the user. After the successful authentication, the service check whether does the route is related to the /user and /auth. If it is, then the service consume the requests. Otherwise, it forwards the request to the service layer where the redirecting operation is perform. Then, the service is send to the dedicated back-end service. Second, authorization is also in place. However, at the current stage, the authorization is only applied to the admin operation such as deactivating and deleting user.

## Run
```bash
npm install --save
npm run start
```

## Test
```bash
npm run test
```

## API Endpoint
| HTTP Verbs | Endpoints | Role |Action |
| --- | --- | --- | --- |
| GET | /api | admin, moderator, user | Default route which tell the service name and version number |
| POST | /api/auth/signup 
| admin | Create new user. |
| POST | /api/auth/signin | admin, moderator, user | Sign in to the system. User will get the JWT in return along with other user's metadata. |
| GET | /api/user/single/:username | admin, moderator, user | Get user's detail by username. |
| GET | /api/user/pagination | admin, moderator, user | Get users' detail with username query and return in the pagination format. |
| PUT | /api/user/info | admin | Update any user info. Can only be used by admin. |
| PUT | /api/user/personal | admin, moderator, user | Update personal detail. |
| PUT | /api/user/password | admin, moderator, user | Update personal password. |
| DEL | /api/user/personal | admin | Delete user by id. |
| * | /rule-service/* | admin, moderator, user | Proxy routes redirect to the rule service. |
| * | /* | admin, moderator, user | Proxy routes redirect to the back-end. |

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
EXPOSE 9091
CMD npm run-script run
```

```bash
docker build . -t <account_name>/<image_name>:<tag>
```

### Run an Docker Image
```yaml
version: '3'
services:
  proxy-server:
    image: "<account_name>/<image_name>:<tag>"
    container_name: waterbeats-auth-gateway
    environment:
      JWT_SECRET=<JWT_SECRET>
      DATABASE_URL=postgres://<username>:<password>@<ip_address>:<port_number>/<database_name>
      CLIENT_ORIGIN=<front-end-url>
      BACKEND_URL=<BACKEND_URL>
    ports:
      - "9091:9091"
    depends_on:
      - database
  database:
    image: "postgres:14"
    container_name: postgres14-waterbeats
    environment:
      POSTGRES_USER: <username>
      POSTGRES_PASSWORD: <password>
      POSTGRES_DB: waterbeats
    volumes:
      - ./postgres_database_schema.sql:/docker-entrypoint-initdb.d/<database_schema_file>.sql
    ports:
      - "5432:5432"
```
```bash
docker-compose up -d
```