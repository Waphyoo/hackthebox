#!/bin/bash

# Secure entrypoint
chmod 600 /entrypoint.sh

# Initialize & Start MariaDB
mkdir -p /run/mysqld
chown -R mysql:mysql /run/mysqld
mysql_install_db --user=mysql --ldata=/var/lib/mysql
mysqld --user=mysql --console --skip-networking=0 &

# Wait for mysql to start
while ! mysqladmin ping -h'localhost' --silent; do echo 'not up' && sleep .2; done

mysql -u root << EOF
CREATE USER 'bn_myapp'@'localhost' IDENTIFIED BY '';
CREATE DATABASE bitnami_myapp;
GRANT ALL PRIVILEGES ON bitnami_myapp.* TO 'bn_myapp'@'localhost';
FLUSH PRIVILEGES;
EOF

cd /app && php artisan migrate
/usr/bin/supervisord -c /etc/supervisord.conf