#!/bin/bash
# Stop the Nginx service
sudo service nginx stop

# Remove the Nginx configuration file
sudo rm /etc/nginx/sites-enabled/default

# Disable the Nginx service from starting automatically
sudo systemctl disable nginx

# Uninstall Nginx
sudo apt-get purge nginx

# Remove directories and files created by the original script
sudo rm -rf /data/web_static
sudo rm -rf /data/

# Remove UFW rule allowing Nginx HTTP traffic
sudo ufw delete allow 'Nginx HTTP'
