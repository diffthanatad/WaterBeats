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