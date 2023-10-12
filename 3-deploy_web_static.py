#!/usr/bin/python3
"""script  that creates and distributes an archive to your web servers
"""


import os
from fabric.api import *
from datetime import datetime


env.hosts = ['54.157.141.67', '100.25.169.176']


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    # current date and time
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # path where archive will be saved
    archive_path = "versions/web_static_{}.tgz".format(now)

    # create directory if it doesn't exist
    local("mkdir -p versions")

    # create a compresses archive
    archived = local("tar -cvzf {} web_static".format(archive_path))

    # Check archive Creation Status
    if archived.return_code != 0:
        return None
    else:
        return archive_path


def do_deploy(archive_path):
    """use os module to check for valid file path"""
    if os.path.exists(archive_path):
        archive = archive_path.split('/')[1]
        a_path = "/tmp/{}".format(archive)
        folder = archive.split('.')[0]
        f_path = "/data/web_static/releases/{}/".format(folder)

        put(archive_path, a_path)
        run("mkdir -p {}".format(f_path))
        run("tar -xzf {} -C {}".format(a_path, f_path))
        run("rm {}".format(a_path))
        run("mv -f {}web_static/* {}".format(f_path, f_path))
        run("rm -rf {}web_static".format(f_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(f_path))
        return True
    return False


def deploy():
    """
    Create and archive and get its path
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
