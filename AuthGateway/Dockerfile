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
CMD npm start

## BUILD COMMAND = docker buildx build --platform=linux/amd64 . -t diffs/ucl-waterbeats:auth-gateway_1.0.0 --no-cache