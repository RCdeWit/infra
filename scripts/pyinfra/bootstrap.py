from pathlib import Path
from pyinfra.operations import server, files


server.user(
    name="Create deploy user",
    user="deploy",
    password=None,
    create_home=True,
    home="/home/deploy",
    groups=["sudo"],
    _sudo=True,
)

files.put(
    src="sudoers",
    dest="/etc/sudoers",
)

server.shell(
    name="Authorize root SSH keys for deploy user",
    commands=[
        "mkdir -p /home/deploy/.ssh",
        "cp /root/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys",
        "chown -R deploy:deploy /home/deploy/.ssh",
        "chmod 700 /home/deploy/.ssh",
        "chmod 600 /home/deploy/.ssh/authorized_keys",
    ],
    _sudo=True,
)