import os
from jupyter_server.auth import passwd
from dotenv import load_dotenv

load_dotenv(dotenv_path="/home/.vncpwd.env")


# vncpwd = "${vncpwd}"

vncpwd = os.getenv("vncpwd")

hash = passwd(vncpwd)

# Configuration file for jupyter-notebook.

c = get_config()

# Set the port to 8888
c.ServerApp.port = 8888

# Allow root to run JupyterLab
c.ServerApp.allow_root = True

# Listen on all IP addresses
c.ServerApp.ip = "0.0.0.0"

# Disable authentication token and use a password
c.ServerApp.open_browser = False

# Optional: Set a specific working directory
c.ServerApp.notebook_dir = "/home"

# Setting hashed_password for IdentityProvider
c.IdentityProvider.hashed_password = hash

c.ServerApp.token = ""
c.ServerApp.password = hash
c.ServerApp.password_required = True
