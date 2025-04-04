#!/usr/bin/python3
<<<<<<< HEAD
"""distrutes the archive"""
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["54.175.253.142", "34.239.255.28"]


def do_deploy(archive_path):
    """gives the archives
    """
    if os.path.isfile(archive_path) is False:
        return False
    fi = archive_path.split("/")[-1]
    nme = fi.split(".")[0]

    if put(archive_path, "/tmp/{}".format(fi)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(nme)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(nme)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(fi, nme)).failed is True:
        return False
    if run("rm /tmp/{}".format(fi)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(nme, nme)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(nme)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(nme)).failed is True:
        return False
    return True
=======
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['3.84.201.218', '54.224.215.237']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
>>>>>>> 8c4e35510d77a5ef3680cd4a33a027addfeecf6b
