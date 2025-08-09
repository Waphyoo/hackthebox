FROM bitnami/laravel:10.3.3

RUN apt-get update \
    && apt-get install -y wget supervisor mariadb-server mariadb-client gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 libxshmfence-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY flag.txt /flag.txt
COPY --chown=root challenge /app
COPY config/supervisord.conf /etc/supervisord.conf

WORKDIR /app

RUN npm install --global --unsafe-perm puppeteer@19.4.0
RUN composer install

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]