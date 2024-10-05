#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy
"""
from fabric.api import local, put, run, env, sudo
from datetime import datetime
from os import path

env.hosts = ['52.91.140.138', '54.242.127.47']


def do_deploy(archive_path):
    """Function to deploy"""
    if not path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        name = archive_path.split('/')[1].split('.')[0]
        sudo("mkdir -p /data/web_static/releases/{}/".format(name))
        sudo("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
             .format(name, name))
        run("rm /tmp/{}.tgz".format(name))
        sudo("mv /data/web_static/releases/{}/web_static/*\
             /data/web_static/releases/{}/".format(name, name))
        sudo("rm -rf /data/web_static/releases/{}/web_static".format(name))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current"
             .format(name))
        return True
    except Exception:
        return False
