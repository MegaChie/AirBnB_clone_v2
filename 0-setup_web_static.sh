#!/usr/bin/env bash
<<<<<<< HEAD
# Sets up a web server for deployment of web_static.

apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Holberton School" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

service nginx restart
=======
# script that sets up web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Add test HTML file to the test folder
sudo tee /data/web_static/releases/test/index.html > /dev/null <<EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# Create a symbolic link to /data/web_static/current
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/; }' /etc/nginx/sites-enabled/default

# Test the Nginx configuration to ensure there are no syntax errors
sudo nginx -t

# Restart Nginx to apply the changes
sudo service nginx restart
>>>>>>> 8c4e35510d77a5ef3680cd4a33a027addfeecf6b
