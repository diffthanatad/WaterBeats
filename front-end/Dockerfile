FROM node:lts-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

## BUILD COMMAND = docker buildx build --platform=linux/amd64 . -t diffs/ucl-waterbeats:front-end_1.0.1 --no-cache
