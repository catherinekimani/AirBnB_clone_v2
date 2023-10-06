#!/usr/bin/python3
"""script  that creates and distributes an archive to your web servers
"""


from os.path import exists
from fabric.api import *
from datetime import datetime


env.hosts = ['54.157.141.67', '100.25.169.176']


def do_pack():
    """generates a .tgz archive the web_static folder
    """
    local("sudo mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
