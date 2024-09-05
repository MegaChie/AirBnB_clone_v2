# Configures an Nginx web server for the deployment of the web_static application.

# Nginx configuration for handling web_static, redirects, and custom error pages
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root /var/www/html;
    index index.html index.htm;

    # Serve content for /hbnb_static using the current web_static release
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    # Redirect /redirect_me to an external URL
    location /redirect_me {
        return 301 https://th3-gr00t.tk;
    }

    # Custom 404 error page
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Ensure Nginx is installed via apt package manager
package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
} ->

# Set up the required directory structure for web_static
file { '/data':
  ensure  => 'directory'
} ->

file { '/data/web_static':
  ensure => 'directory'
} ->

file { '/data/web_static/releases':
  ensure => 'directory'
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory'
} ->

file { '/data/web_static/shared':
  ensure => 'directory'
} ->

# Create a simple index.html file for testing the deployment
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n"
} ->

# Create a symbolic link 'current' to point to the 'test' release
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
} ->

# Set ownership of the /data/ directory to 'ubuntu' user and group
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

# Ensure the default web directory exists for Nginx
file { '/var/www':
  ensure => 'directory'
} ->

file { '/var/www/html':
  ensure => 'directory'
} ->

# Create an index.html file for the default Nginx site
file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n"
} ->

# Create a custom 404 error page
file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n"
} ->

# Deploy the Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
} ->

# Restart the Nginx service to apply changes
exec { 'nginx restart':
  path => '/etc/init.d/'
}

