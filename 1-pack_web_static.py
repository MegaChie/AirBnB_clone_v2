#!/usr/bin/python3
"""Script that generates a .tgz archive from the web_static folder."""
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Create a compressed archive of the web_static folder.

    Returns:
        str: The file path of the created archive.
    """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(date)
    if local("sudo mkdir -p versions").failed is True:
        return None
    if local("sudo tar -cvzf {} web_static".format(file_name)).failed is True:
        return None
    return file_name
