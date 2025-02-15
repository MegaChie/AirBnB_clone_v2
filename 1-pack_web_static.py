#!/usr/bin/python3
# A Fabfile to generates a .tgz archive from the contents of web_static.
from datetime import datetime
from fabric.api import local
import os.path


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    date = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(date.year,
                                                         date.month,
                                                         date.day,
                                                         date.hour,
                                                         date.minute,
                                                         date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
