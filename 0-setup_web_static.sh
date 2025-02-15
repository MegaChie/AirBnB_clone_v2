#!/usr/bin/env bash
# 0-setup_web_static.sh

# Install Nginx
if ! command -v nginx &> /dev/null; then
	sudo apt-get update
	sudo apt-get install -y nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web-static/shared/

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate the symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
sudo sed -i '/listen 80 default_server;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' $nginx_config

# Restart Nginx to apply changes
sudo service nginx restart

# Exit successfully
exit 0
