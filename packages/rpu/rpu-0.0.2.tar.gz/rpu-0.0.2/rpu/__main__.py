import platform
import sys
import webbrowser

import rpu

from .cli import ConsoleClient

client = ConsoleClient()


@client.command(
    name="version",
    description="gives you the version of rpu you are running",
    brief="gives you the version of rpu your using",
    aliases=["v"],
)
def cmd_version():
    print(rpu.__version__)


@client.command(
    name="docs",
    description="opens rpu's documentation. If your using alpha/beta, latest docs will be brought up. If your using final then stable docs will be brought up.",
    brief="opens rpus docs",
    aliases=["d"],
)
def cmd_docs():
    version = "stable" if rpu.version_info.releaselevel == "final" else "latest"

    print(f"Opening the {version} docs in your browser")
    webbrowser.open(f"https://rpu.cibere.dev/{version}/index")


@client.command(
    name="system-info",
    description="gives you system information. Specifically rpu version, python version, and os",
    brief="gives you system info",
    aliases=["os", "s"],
)
def cmd_system_info():
    info = {}

    info["ciberedev.py"] = rpu.__version__
    info["python"] = sys.version.split(" ")[0]
    info["OS"] = platform.platform()

    nl = "\n"
    print(nl.join([f"{item}: {info[item]}" for item in info]))


client.run()
