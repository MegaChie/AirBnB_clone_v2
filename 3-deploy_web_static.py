#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
using the function deploy
"""
from fabric.api import env
import os


do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy
env.hosts = ['54.84.162.208', '54.175.225.209']
archive_path = do_pack()


def deploy():
    """Function to deploy"""
    if archive_path is None:
        return False
    print("web_static packed: {} -> {}Bytes"
          .format(archive_path, os.path.getsize(archive_path)))
    return do_deploy(archive_path)
