#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local


def do_pack():
    """Function to compress files"""
    local("mkdir -p versions")
    timestamp = local("date +%Y%m%d%H%M%S", capture=True)
    archive_name = "web_static_{}.tgz".format(timestamp)
    file = local("tar -cvzf versions/{} web_static".format(archive_name))
    if file.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None
