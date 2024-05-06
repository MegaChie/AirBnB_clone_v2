#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to servers
using the function deploy
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['34.74.59.91', '34.204.179.254']


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None

    
def do_deploy(archive_path):
    """distributes an archive to web server"""
    if exists(archive_path) is False:
        return False
    try:
        file_nm = archive_path.split("/")[-1]
        end_t = file_nm.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, end_t))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_nm, path, end_t))
        run('rm /tmp/{}'.format(file_nm))
        run('mv {0}[1}/web_static/* {0}{1}/'.format(path, end_t))
        run('rm -rf {}{}/web_static'.format(path, end_t))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, end_t))
        return True
    except:
        return False

    
def deploy():
    """creates and distributes archives to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
