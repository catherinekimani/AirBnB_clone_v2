#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static
    """
    local("sudo mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_archive = "versions/web_static_{}.tgz".format(timestamp)
    result = local("sudo tar -cvzf {} web_static".format(file_archive))
    if result.succeeded:
        return file_archive
