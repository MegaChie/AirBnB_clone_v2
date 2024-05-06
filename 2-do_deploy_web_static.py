#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web server
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['34.74.59.91', '34.294.179.254']


def do_deploy(archive_path):
    """distributes an archive to server"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        end_t = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, end_t))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, end_t))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, end_t))
        run('rm -rf {}{}/web_static'.format(path, end_t))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, end_t))
        return True
    except:
        return False
