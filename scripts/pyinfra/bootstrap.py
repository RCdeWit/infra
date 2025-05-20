from pathlib import Path
from pyinfra.operations import server, files


server.user(
    name="Create deployment user",
    user="deploy",
    password=None,
    system=True,
    create_home=True,
    home="/home/deploy",
    groups=["sudo"],
)

files.put(
    src="sudoers",
    dest="/etc/sudoers",
)

files.put(
    src=Path.home() / ".ssh/id_rsa.pub",
    dest="/home/deploy/.ssh/authorized_keys",
    user="deploy",
)