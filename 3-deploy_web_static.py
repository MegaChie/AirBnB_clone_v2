#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.

Usage:
    fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

# List of hosts (web servers) where the archive will be deployed
env.hosts = ["184.72.96.209", "100.25.152.248"]


def do_pack():
    """Generate a .tgz archive from the contents of the 'web_static' folder."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create 'versions' directory if it doesn't exist
        if not isdir("versions"):
            local("mkdir versions")

        # Create the archive with a timestamp
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))

        return file_name
    except BaseException:
        return None


def do_deploy(archive_path):
    """Deploy the archive to the web servers."""
    if not exists(archive_path):
        return False
    try:
        # Extract file name and base name (without extension) from the archive
        # path
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload archive to /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create the release folder on the server
        run("mkdir -p {}{}/".format(path, no_ext))

        # Uncompress the archive into the release folder
        run("tar -xzf /tmp/{} -C {}{}/".format(file_n, path, no_ext))

        # Remove the archive from /tmp/ after extraction
        run("rm /tmp/{}".format(file_n))

        # Move the contents out of the web_static folder and delete the folder
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))
        run("rm -rf {}{}/web_static".format(path, no_ext))

        # Remove the current symbolic link and create a new one pointing to the
        # new release
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path, no_ext))

        return True
    except BaseException:
        return False


def deploy():
    """Create an archive and deploy it to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
