# Authenticate Gateway Service
Hello and welcome to the Authentication Gateway service or AuthGateway for short. This service is part of the Farmer PC and is responsible for authenticating all API requests that will be send to all other services in the back-end. We uses the PostgreSQL to keep the  users' detail.
\
\
There are two main functionalities for this component. First, as mentioned earlier is to authenticate the user. After the successful authentication, the service check whether does the route is related to the /user and /auth. If it is, then the service consume the requests. Otherwise, it forwards the request to the service layer where the redirecting operation is perform. Then, the service is send to the dedicated back-end service. Second, authorization is also in place. However, at the current stage, the authorization is only applied to the admin operation such as deactivating and deleting user.

---

## Run
* For development, please start the PostgreSQL database. The Docker image that we used and compose file is provided below.
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
| No. | HTTP Verbs | Endpoints | Role | Action | JWT required |
| --- | --- | --- | --- | --- | --- |
| 1. | GET | /api | admin, moderator, user | Default route which tell the service name and version number | No |
| 2. | POST | /api/auth/signup | admin | Create new user. | Yes |
| 3. | POST | /api/auth/signin | admin, moderator, user | Sign in to the system. User will get the JWT in return along with other user's metadata. | No |
| 4. | GET | /api/user/single/:username | admin, moderator, user | Get user's detail by username. | Yes |
| 5. | GET | /api/user/pagination?page=<page>&size=<size>&username=<username> | admin, moderator, user | Get users' detail with username query and return in the pagination format. | Yes |
| 6. | PUT | /api/user/info | admin | Update any user info. Can only be used by admin. | Yes |
| 7. | PUT | /api/user/personal | admin, moderator, user | Update personal detail. | Yes |
| 8. | PUT | /api/user/password | admin, moderator, user | Update personal password. | Yes |
| 9. | DEL | /api/user/personal | admin | Delete user by id. | Yes |
| 10. | * | /rule-service/* | admin, moderator, user | Proxy routes redirect to the rule service. | Yes |
| 11. | * | /* | admin, moderator, user | Proxy routes redirect to the back-end. | Yes |

### JWT required
* In this service, we use the JWT token with the bearertoken format.
``` js
  config.headers["Authorization"] = "Bearer xxxxxx.yyyyyy.zzzzzz";
```

### 1. Default Route
```
GET localhost:9091/api/
```
- example of response body
```json
{
  "message": "Authentication Gateway Service (V 1.0.0).",
}
```

### 2. Sign up
```
POST localhost:9091/api/auth/signup
```
- example of request body
```json
{ 
  "name": "firstName lastName",
  "username": "first-l",
  "password": "12345678",
  "role": "user"
}
```
| HTTP status | Description |
| --- | --- |
| 201 | Successfully sign up. |
| 500 | Fail to sign up. |

### 3. Sign In
```
POST localhost:9091/api/auth/signin
```
- example of request body
```json
{
  "username": "david-b",
  "password": "12345678"
}
```
- example of response body
```json
{
  "name": "David Brown",
  "username": "david-b",
  "role": "ROLE_ADMIN",
  "accessToken": "xxxxxx.yyyyyy.zzzzzz"
}
```
| HTTP status | Description |
| --- | --- |
| 200 | Successfully sign in. |
| 500 | Fail to sign in. |

### 4. Get user's detail by username.
```
GET localhost:9091/api/user/single/david-b
```
- example of response body
```json
{
  "id": 1,
  "name": "David Brown",
  "username": "david-b",
  "role": "admin"
}
```
| HTTP status | Description |
| --- | --- |
| 200 | Successfully retrieve user's detail. |
| 204 | User does not exist. |
| 500 | Fail to retrieve user's detail. |

### 5. Get users' detail with username query and return in the pagination format.
```
GET localhost:9091/user/pagination?page=0&size=10&username=da
```
- example of response body
```json
{
  "totalItems": 2,
  "users": [
    {
      "id": 1,
      "name": "David Brown",
      "username": "david-b",
      "disable": false,
      "role": "admin"
    },
    {
      "id": 2,
      "name": "Daniel Smith",
      "username": "daniel-s",
      "disable": false,
      "role": "moderator"
    }
  ],
  "totalPages": 1,
  "currentPage": 0
}
```
| HTTP status | Description |
| --- | --- |
| 200 | Successfully retrieve users' detail. |
| 204 | Successfully retrieve users' detail. |
| 500 | Fail to retrieve users' detail. |

### 6. Update any user info.
```
PUT localhost:9091/user/info
```
- example of request body
```json
{
  "id": 1,
  "name": "firstName lastName",
  "username": "first-l",
  "role": "admin",
  "disable": "1"
}
```
| HTTP status | Description |
| --- | --- |
| 200 | Successfully update user's detail. |
| 500 | Fail to update user's detail. |

### 7. Update personal detail.
```
PUT localhost:9091/user/personal
```
- example of request body
```json
{
  "id": 5,
  "name": "firstName lastName",
  "username": "bob-d"
}
```
| HTTP status | Description |
| --- | --- |
| 200 | Successfully update user's detail. |
| 500 | Fail to update user's detail. |

### 8. Change password
```
PUT localhost:9091/user/password
```
- example of request body
```json
{
  "id": 5,
  "oldPassword": "12345678",
  "newPassword": "1"
}
```
| HTTP status | Description |
| --- | --- |
| 200 | Successfully change password. |
| 500 | Fail to change password. |

### 9. Delete user
```
DEL localhost:9091/user/1
```
| HTTP status | Description |
| --- | --- |
| 200 | Successfully delete user. |
| 500 | Fail to delete user. |

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

---

## Database
We strongly recommend user to create a new password. The password appear here is only for development and demonstration purpose. Please create and hash the new password before proceeding.

``` SQL
DROP TABLE IF EXISTS "public"."users";

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS users_id_seq START 5;
DROP TYPE IF EXISTS "public"."enum_users_role";
CREATE TYPE "public"."enum_users_role" AS ENUM ('admin', 'moderator', 'user');

-- Table Definition
CREATE TABLE "public"."users" (
    "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    "name" varchar(150) NOT NULL,
    "username" varchar(150) UNIQUE NOT NULL,
    "password" varchar(300) NOT NULL,
    "disable" bool DEFAULT false,
    "role" "public"."enum_users_role" DEFAULT 'user'::enum_users_role,
    PRIMARY KEY ("id")
);

-- It is strongly recommended to hash a new password before using the system in the PRODUCTION system. 
-- These passwords are only used for development.
INSERT INTO "public"."users" ("id", "name", "username", "password", "disable", "role") VALUES
(1, 'David Brown', 'david-b', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'admin'),
(2, 'Daniel Smith', 'daniel-s', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'moderator'),
(3, 'Bob Smith', 'bob-s', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'T', 'user'),
(4, 'Alice Mac', 'alice-m', '$2a$12$JSR03lduQ6WNuM5ltjcUh.ANvLywn1F0GkjVJ.z5Rc.zfNU80fNOu', 'f', 'user');
```