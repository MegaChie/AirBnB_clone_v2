#!/usr/bin/env python3
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        # Create the versions folder if it doesn't exist
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        # Generate the archive name using the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"web_static_{timestamp}.tgz"
        archive_path = f"versions/{archive_name}"

        # Create the .tgz archive
        print(f"Packing web_static to {archive_path}")
        result = local(f"tar -cvzf {archive_path} web_static")

        # Check if the archive was created successfully
        if result.succeeded:
            archive_size = os.path.getsize(archive_path)
            print(f"web_static packed: {archive_path} -> {archive_size}Bytes")
            return archive_path
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    pass
