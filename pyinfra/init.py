from pathlib import Path
from pyinfra.operations import server, files

server.user(
    name="Create deployment user",
    user="deploy",
    system=True,
    create_home=True,
    home="/home/deploy",
    groups=["sudo"],
)

files.put(
    src=Path.home() / ".ssh/id_rsa.pub",
    dest="/home/deploy/.ssh/authorized_keys",
    user="deploy",
)