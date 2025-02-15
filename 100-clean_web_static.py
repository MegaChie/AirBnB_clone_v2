#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.

Usage:
    fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

# Define the list of web servers where outdated archives will be deleted
env.hosts = ["184.72.96.209", "100.25.152.248"]


def do_clean(number=0):
    """
    Deletes out-of-date archives both locally and on remote servers.

    Args:
        number (int): The number of recent archives to keep.
                      If number is 0 or 1, it keeps only the most recent archive.
                      If number is 2, it keeps the most and second-most recent archives, and so on.

    The function works by:
    - Keeping the specified number of archives locally and removing the older ones.
    - Removing the corresponding older archives from the remote servers.
    """
    # Ensure that at least one archive is kept by default
    number = 1 if int(number) == 0 else int(number)

    # Clean local archives
    archives = sorted(os.listdir("versions"))
    [
        archives.pop() for i in range(number)
    ]  # Remove the most recent 'number' archives from the list
    with lcd("versions"):
        [local("rm ./{}".format(a))
         for a in archives]  # Delete older archives locally

    # Clean archives on remote servers
    with cd("/data/web_static/releases"):
        # List the archives sorted by modification time (oldest first)
        archives = run("ls -tr").split()
        archives = [
            a for a in archives if "web_static_" in a
        ]  # Filter out files that aren't web_static archives
        [
            archives.pop() for i in range(number)
        ]  # Remove the most recent 'number' archives from the list
        [
            run("rm -rf ./{}".format(a)) for a in archives
        ]  # Delete older archives on the remote server
