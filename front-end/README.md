# front-end
Hello and welcome to the front-end web application. This application is part of the Farmer PC and is responsible for providing interface for user to interact with the whole system.
\
\
There are three main functionalities for this web interface. First, the front-end provides a device visualisation in various formats. For instance, user can view the device in a map which is located in the Home page or via graph in Graph visalisation page. Second, rule and alert configuration page. These pages are for setting and definign rules. Third, the user configuration is provided. This includes admin portal (only administrator role has an access to this page) and personal setting page where user can change his/her password.

---

## Start the project
```
npm install
npm run serve
```

---

## Pages
| No. | Name | Route | Authentication | Authorisation | Description |
|---|---|---|---|---|---|
| 1. | Home (i.e., Map Visualisation) | / | Yes | user, moderator, admin | Present device's detail in geolocation format where devices are present as a coloured marker on the map. |
| 2. | Graph Visualisation | /graph | Yes | user, moderator, admin | Provide an interface for user to plot the sensor data. |
| 3. | Actuator Configuration | /actuator_configuration | Yes | user, moderator, admin | Set the rules for the actuators. |
| 4. | Alert | /alerts | Yes | user, moderator, admin | Set the alerts based on the sensors' reading. |
| 5. | Admin | /admin | Yes | admin | Admin interface which including creating new user, disable user and update user's detail. |
| 6. | Setting | /setting | Yes | user, moderator, admin | Personal setting page which allows user to update his/her account password. |
| 7. | Log In | /login | No | user, moderator, admin | First page that the user will see where user key in username and password. |

---

## Docker
### Environment variable injection
* When the application is built, the environment variable is turn into a hard coded string. So, we need to add a script which will replace these hard coded string. For more information check the links below.
* Sources: 
    * https://moreillon.medium.com/environment-variables-for-containerized-vue-js-applications-f0aa943cb962. Last accessed: 6 April 2023
    * https://stackoverflow.com/questions/53010064/pass-environment-variable-into-a-vue-app-at-runtime/57928031#57928031. Last accessed 6 April 2023
```bash
#!/bin/sh

ROOT_DIR=/app

# Replace env vars in files served by NGINX
for file in $ROOT_DIR/js/*.js* $ROOT_DIR/index.html $ROOT_DIR/precache-manifest*.js;
do
  sed -i 's|VUE_APP_SERVICE_URL_PLACEHOLDER|'${VUE_APP_SERVICE_URL}'|g' $file
  sed -i 's|VUE_APP_TIMEOUT_PLACEHOLDER|'${VUE_APP_TIMEOUT_PLACEHOLDER}'|g' $file
  # Your other variables here...
done
# Starting NGINX
nginx -g 'daemon off;'
```

### Build an Docker Image
```yaml
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build

FROM nginx:stable-alpine as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf

COPY ./substitute_environment_variables.sh /substitute_environment_variables.sh
RUN chmod +x /substitute_environment_variables.sh
ENTRYPOINT ["/substitute_environment_variables.sh"]
```

```bash
docker build . -t <account_name>/<image_name>:<tag>
```

### Run an Docker Image
```yaml
version: '3'
services:
  front-end:
    image: "<account_name>/<image_name>:<tag>"
    container_name: waterbeats-front-end
    environment:
      VUE_APP_SERVICE_URL: <Authentication_Gateway_service_URL>
    ports:
      - "8080:80"
```
```bash
docker-compose up -d
```