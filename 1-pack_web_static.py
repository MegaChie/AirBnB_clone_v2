#!/usr/bin/python3
"""#This generates .tgz archive from teh web_static"""

from datetime import datetime
from fabric.api import *


def do_pack():
    """
    archive file making
    """

    tme = datetime.now()
    arch = 'web_static_' + tme.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    make = local('tar -cvzf versions/{} web_static'.format(arch))
    if make is not None:
        return arch
    else:
        return None
