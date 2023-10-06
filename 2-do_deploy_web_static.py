#!/usr/bin/python3
"""
fab script hat creates and distributes an archive to
your web servers, using the function deploy:
"""


from os.path import exists
from fabric.api import *
from datetime import datetime


# Set the host IP
env.hosts = ['54.157.141.67', '100.25.169.176']


def do_deploy(archive_path):
    """distribute an archive to your web servers"""
    if exists(archive_path) is False:
        return False
    file_archive = archive_path.split('/')[-1]
