#!/bin/sh

ROOT_DIR=/app

# Replace env vars in files served by NGINX
for file in $ROOT_DIR/js/*.js* $ROOT_DIR/index.html $ROOT_DIR/precache-manifest*.js;
do
  sed -i 's|VUE_APP_SERVICE_URL_PLACEHOLDER|'${VUE_APP_SERVICE_URL}'|g' $file
  # Your other variables here...
done
# Starting NGINX
nginx -g 'daemon off;'