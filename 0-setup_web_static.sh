#!/usr/bin/env bash
# Script to configure a web server for deploying 'web_static'

# Update the package list and install Nginx
sudo apt-get update
sudo apt-get -y install nginx

# Allow HTTP traffic through the firewall for Nginx
sudo ufw allow 'Nginx HTTP'

# Create necessary directories for the deployment
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a sample HTML file to test the setup
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link to the current release
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# Set ownership of the /data/ directory to the ubuntu user
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content from the /data/web_static/current/ directory
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart Nginx to apply the changes
sudo service nginx restart
