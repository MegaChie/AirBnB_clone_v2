#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the web_static folder.

Usage:
    fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from fabric.api import *


def do_pack():
    """
    Creates a .tgz archive of the web_static folder.

    The archive will be stored in the 'versions' directory and will be
    named using the current timestamp to ensure uniqueness.

    Returns:
        The archive path if the creation is successful, otherwise None.
    """

    # Get the current time and format it for the archive name
    time = datetime.now()
    archive = "web_static_" + time.strftime("%Y%m%d%H%M%S") + ".tgz"

    # Create the 'versions' directory if it doesn't exist
    local("mkdir -p versions")

    # Create the archive and store it in the 'versions' directory
    create = local("tar -cvzf versions/{} web_static".format(archive))

    # Return the archive name if successful, otherwise return None
    if create is not None:
        return archive
    else:
        return None
