FROM node:current-alpine

# Install necessary dependencies
RUN apk update \
    && apk add --no-cache chromium nss freetype harfbuzz ttf-freefont \
    && apk add --no-cache curl wget xvfb unzip supervisor \
    && rm -rf /var/cache/apk/*

# Set environment variable for Puppeteer to use the system-installed Chromium
ENV PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Install Node.js dependencies
WORKDIR /app
COPY challenge .
RUN npm install

# Copying required files
COPY flag.txt /
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port
EXPOSE 1337

# Start supervisor
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
