import subprocess


def install_packages(packages: list) -> int:
    """Installs a list of programs with pacman."""
    cmd = subprocess.run(["pacman", "-S", *packages])
    return cmd.returncode


def enable_services(services: list) -> int:
    """Enables a list of systemd services."""
    for service in services:
        cmd = subprocess.run(["systemctl", "enable", f"{service}.service"])
        if cmd.returncode != 0:
            return cmd.returncode
    return 0


def virt_system() -> str:
    """Detects if the current system is running in a virtual machine
    and returns its type."""
    cmd = subprocess.run("systemd-detect-virt", capture_output=True)
    return cmd.stdout.decode().rstrip()
