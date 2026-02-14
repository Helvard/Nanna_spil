# Multi-stage build for game collection
FROM node:18-alpine AS web-builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (if any)
RUN if [ -f package-lock.json ]; then npm ci --omit=dev; \
    elif [ -f package.json ] && [ "$(node -p "Object.keys(require('./package.json').dependencies||{}).length")" != "0" ]; then npm install --omit=dev; \
    else echo "No production dependencies to install"; fi

# Copy web games
COPY Games/ ./Games/
COPY paw_patrol/ ./paw_patrol/
COPY *.html ./

# Build stage for final image
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy games from builder stage
COPY --from=web-builder /app /usr/share/nginx/html

# Create proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
