#!/usr/bin/env python3
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists

# Define the list of web servers
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your actual server IPs
env.user = 'ubuntu'  # Replace with your SSH username
env.key_filename = 'my_ssh_private_key'  # Replace with your SSH private key path

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        # Create the versions folder if it doesn't exist
        if not exists("versions"):
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
            archive_size = local(f"stat -c%s {archive_path}", capture=True)
            print(f"web_static packed: {archive_path} -> {archive_size}Bytes")
            return archive_path
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
        archive_filename = archive_path.split('/')[-1]
        archive_no_ext = archive_filename.split('.')[0]
        remote_tmp_path = f"/tmp/{archive_filename}"
        put(archive_path, remote_tmp_path)

        # Create the target directory for the release
        release_path = f"/data/web_static/releases/{archive_no_ext}"
        run(f"mkdir -p {release_path}")

        # Uncompress the archive to the release directory
        run(f"tar -xzf {remote_tmp_path} -C {release_path}")

        # Remove the uploaded archive from the web server
        run(f"rm {remote_tmp_path}")

        # Move the contents of the web_static folder to the release directory
        run(f"mv {release_path}/web_static/* {release_path}/")

        # Remove the now-empty web_static folder
        run(f"rm -rf {release_path}/web_static")

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new release
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def deploy():
    """
    Creates and distributes an archive to your web servers.
    """
    # Step 1: Create the archive
    archive_path = do_pack()
    if not archive_path:
        print("Failed to create archive.")
        return False

    # Step 2: Deploy the archive
    return do_deploy(archive_path)
