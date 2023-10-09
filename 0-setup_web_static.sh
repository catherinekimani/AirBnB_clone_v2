#!/usr/bin/env bash
# set up web servers for deployment of web static

# Install Nginx
sudo apt-get update
sudo apt-get install -y nginx

# create folders
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Create a fake HTML file
echo "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
	</html>" >> /data/web_static/releases/test/index.html

# create symbolink & recreate it too
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user, group
sudo chown -R ubuntu:ubuntu /data/

# update nginx config to server the content of /data/web_static/current/ to hbnb_static
sudo sed -i "26i \\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

# restart nginx for chnages to be applied
sudo service nginx restart
