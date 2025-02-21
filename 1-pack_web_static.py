#!/usr/bin/python3
<<<<<<< HEAD
"""#This generates .tgz archive from teh web_static"""
=======
"""
Fabric script to genereate tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""
>>>>>>> 8c4e35510d77a5ef3680cd4a33a027addfeecf6b

from datetime import datetime
from fabric.api import *


def do_pack():
    """
<<<<<<< HEAD
    archive file making
    """

    tme = datetime.now()
    arch = 'web_static_' + tme.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    make = local('tar -cvzf versions/{} web_static'.format(arch))
    if make is not None:
        return arch
=======
    making an archive on web_static folder
    """

    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    create = local('tar -cvzf versions/{} web_static'.format(archive))
    if create is not None:
        return archive
>>>>>>> 8c4e35510d77a5ef3680cd4a33a027addfeecf6b
    else:
        return None
