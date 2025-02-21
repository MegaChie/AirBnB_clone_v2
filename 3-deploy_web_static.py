#!/usr/bin/python3
"""
<<<<<<< HEAD
deploys the web static
=======
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers

execute: fab -f 3-deploy_web_static.py deploy -i ~/.ssh/id_rsa -u ubuntu
>>>>>>> 8c4e35510d77a5ef3680cd4a33a027addfeecf6b
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
<<<<<<< HEAD
env.hosts = ['34.228.159.176', '18.234.150.129']


def do_pack():
    """makes a tgz archive"""
=======
env.hosts = ['34.226.191.215', '34.235.167.216']


def do_pack():
    """generates a tgz archive"""
>>>>>>> 8c4e35510d77a5ef3680cd4a33a027addfeecf6b
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
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
<<<<<<< HEAD
        file_name = archive_path.split("/")[-1]
        no_ex = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ex))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ex))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ex))
        run('rm -rf {}{}/web_static'.format(path, no_ex))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ex))
=======
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
>>>>>>> 8c4e35510d77a5ef3680cd4a33a027addfeecf6b
        return True
    except:
        return False


def deploy():
<<<<<<< HEAD
    """creates and distribte the servers"""
=======
    """creates and distributes an archive to the web servers"""
>>>>>>> 8c4e35510d77a5ef3680cd4a33a027addfeecf6b
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
