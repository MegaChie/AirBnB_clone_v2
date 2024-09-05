#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers.

This script is based on the file 1-pack_web_static.py and is responsible for
deploying the content of a .tgz archive to the specified web servers.
"""

from fabric.api import put, run, env
from os.path import exists

# Define the list of web servers to deploy to
env.hosts = ["54.89.109.87", "100.25.190.21"]


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and sets up the deployment.

    Args:
        archive_path (str): The path to the .tgz archive to be deployed.

    Returns:
        bool: True if the deployment was successful, False otherwise.
    """

    # Check if the archive exists
    if not exists(archive_path):
        return False

    try:
        # Extract the file name and the base name without extension
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create the release directory
        run("mkdir -p {}{}/".format(path, no_ext))

        # Uncompress the archive to the release directory
        run("tar -xzf /tmp/{} -C {}{}/".format(file_n, path, no_ext))

        # Remove the uploaded archive from /tmp/
        run("rm /tmp/{}".format(file_n))

        # Move the contents out of the web_static subdirectory
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))

        # Remove the empty web_static folder
        run("rm -rf {}{}/web_static".format(path, no_ext))

        # Remove the old symbolic link and create a new one
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path, no_ext))

        return True
    except BaseException:
        return False
