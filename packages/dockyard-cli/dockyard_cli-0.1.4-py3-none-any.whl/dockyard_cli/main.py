from urllib import request
import click
from configparser import ConfigParser
from pathlib import Path
import requests
import os, sys
import subprocess
from datetime import datetime
import re

requests.packages.urllib3.disable_warnings()

config = ConfigParser()
config.read(str(Path.home() / ".dockyard.ini"))
install_cmd = "pip3 install --upgrade dockyard-cli"

def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return (getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix)


def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix

def get_formatted_name(name) :
    name=re.sub('[^A-Za-z0-9-]+', '-', name).lower()
    return name.strip("-")

def _update():
    home = str(Path.home())
    if in_virtualenv():
        p = subprocess.run(install_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=home, shell=True)
    else:
        cmd = install_cmd + " --user"
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=home, shell=True)
    if p.returncode != 0:
        if p.stderr:
            print(p.stderr.decode("ascii"))


    ini_file = str(Path.home() / ".dockyard.ini")
    timestamp = datetime.now().timestamp()
    os.utime(ini_file, (timestamp, timestamp))


def auto_update():
    if config.get("default", "auto_update", fallback="true") == "false":
        return

    ini_file = str(Path.home() / ".dockyard.ini")

    stat = os.stat(ini_file)
    d1 = datetime.fromtimestamp(stat.st_mtime)
    d2 = datetime.now()
    if (d2 - d1).days < 1:
        return
    _update()


@click.group()
def main(args=None):
    """Group for dockyard commands."""
    pass

@main.command()
def configure():
    """Configure Dockyard CLI"""

    if "default" not in config.sections():
        config.add_section("default")
        
    url = click.prompt("Dockyard URL", default="https://dockyard.lab.altoslabs.com")
    username = config.get("default","username",fallback=os.environ.get("USER",""))
    username = click.prompt("Username", default=username)
    config.set("default", "url", url)
    config.set("default", "username", username)

    with open(str(Path.home() / ".dockyard.ini"), "w") as f:
        config.write(f)


@main.command()
def update():
    """Update dockyard cli"""
    _update()


@main.command()
@click.argument("workspace_name")
def ssh(workspace_name):
    """SSH to dockyard workspace"""
    if "default" not in config.sections():
        raise click.UsageError("You need to run 'dcli configure' first.")

    url = config.get("default","url")
    user = config.get("default","username")

    r = requests.get(f"{url}/api/public/ssh/{user}/{workspace_name}", verify=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()

    resp = r.json()
    host = resp["ip"]
    port = resp["port"]
    print(f"running ssh {user}@{host} -p {port}")
    os.execlp("ssh","ssh", f"{user}@{host}", "-p", str(port))



@main.command()
@click.argument("source")
@click.argument("target")

def scp(source, target):
    """COPY files(s)/directory from/to dockyard workspace"""

    if ":" not in source and ":" not in target:
        click.UsageError("source or target needs to be of the format <worksapce_name>:/path")

    if "default" not in config.sections():
        raise click.UsageError("You need to run 'dcli configure' first.")

    url = config.get("default","url")
    user = config.get("default","username")

    local_source = False

    if ":" in source:
        workspace_name = source.split(":")[0]
        source = source.split(":")[1]
    else:
        workspace_name = target.split(":")[0]
        local_source = True
        target = target.split(":")[1]

    workspace_dir = get_formatted_name(workspace_name.lower())

    r = requests.get(f"{url}/api/public/ssh/{user}/{workspace_name}", verify=False)
    if r.status_code != 200:
        click.echo(r.text)
        raise click.Abort()

    resp = r.json()
    host = resp["ip"]
    port = resp["port"]
    
    if local_source:
        if target == "" or target[0] not in ["~","/"]:
            target = f"workspaces/{workspace_dir}/{target}"
        print("scp", "-r", "-P", str(port), source, f"{user}@{host}:{target}")
        os.execlp("scp","scp", "-r", "-P", str(port), source, f"{user}@{host}:{target}")
    else:
        if source == "" or source[0] not in ["~","/"]:
            source = f"workspaces/{workspace_dir}/{source}"
        print("scp", "-r", "-P", str(port), f"{user}@{host}:{source}", target)
        os.execlp("scp","scp", "-r", "-P", str(port), f"{user}@{host}:{source}", target)        