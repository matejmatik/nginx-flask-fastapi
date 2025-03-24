FROM nginx:stable-bullseye AS base

# Set up Timezone
ENV TZ="Europe/Ljubljana"

# Install dependencies
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Builder stage
FROM base AS builder

# Copy necessary files
COPY --chown=nginx:nginx nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx start.sh /app/start.sh

# Set permissions
RUN chown -R nginx:nginx /app && chmod -R 755 /app && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chmod -R 755 /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && chown -R nginx:nginx /var/run/nginx.pid

# Final image
FROM base

# Copy built files from builder stage
COPY --from=builder --chown=nginx:nginx /app /app
COPY --from=builder --chown=nginx:nginx /etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Set permissions
RUN chown -R nginx:nginx /app && chmod -R 755 /app && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chmod -R 755 /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && chown -R nginx:nginx /var/run/nginx.pid

USER nginx

CMD ["nginx", "-g", "daemon off;"]
