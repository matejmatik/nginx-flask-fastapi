#!/bin/bash
envsubst '$FLASK_APP_ADDRESS:$FLASK_APP_PORT' < /tmp/default.conf > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'
