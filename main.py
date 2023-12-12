#!/bin/python3

import os
import subprocess
import sys

profiles: dict = {1: "Gnome", 2: "KDE Plasma (BETA)"}

# Show available profiles
for profile_number, profile_name in profiles.items():
    print(f"{profile_number}. {profile_name}")

# Profile selection
selection: str = ""
PROFILE: int = 0

while PROFILE == 0:
    print('Select a profile (enter "c" to cancel):', end=" ")
    selection: str = input()

    if selection.isdigit() and int(selection) in profiles:
        PROFILE = int(selection)
    else:
        if selection == "c":
            sys.exit(1)
        else:
            print("Enter a valid number [1-2]")


packages: list = []
PROFILE_FILE: str = ""
DISPLAY_MANAGER: str = ""
match PROFILE:
    case 1:
        print(f"You selected {profiles[1]}")
        PROFILE_FILE = "gnome_packages.txt"
        DISPLAY_MANAGER = "gdm"
    case 2:
        print(f"You selected {profiles[2]}")
        PROFILE_FILE = "plasma_packages.txt"
        DISPLAY_MANAGER = "sddm"
    case _:
        print("An error has ocurred")

# Read packages from profile_file
if os.path.exists(PROFILE_FILE):
    with open(PROFILE_FILE, encoding="utf8") as f:
        for line in f:
            packages.append(line.rstrip())
else:
    print(f"File {PROFILE_FILE} does not exist")
    sys.exit(1)

# Install packages
if subprocess.run(["sudo", "pacman", "-S", *packages, DISPLAY_MANAGER]).returncode != 0:
    sys.exit(1)

# Enable display manager
subprocess.run(["sudo", "systemctl", "enable", DISPLAY_MANAGER])

# Configure virtual machine
virt_system: str = subprocess.run(
    "systemd-detect-virt", capture_output=True
).stdout.decode()

virt_packages: list = []
VIRT_SERVICE: str = ""
match virt_system:
    case "vmware":
        virt_packages = ["open-vm-tools", "gtkmm3"]
        VIRT_SERVICE = "vmtoolsd.service"
    case "oracle":
        virt_packages = ["virtualbox-guest-utils"]
        VIRT_SERVICE = "vboxservice.service"

if subprocess.run(["sudo", "pacman", "-S", *virt_packages]).returncode == 0:
    subprocess.run(["sudo", "systemctl", "enable", VIRT_SERVICE])
