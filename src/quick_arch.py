#!/bin/python3

import os
import sys
import utils

SCRIPT_DIR = os.path.dirname(__file__)

if os.geteuid() != 0:
    sys.exit("You need to have root privileges to run this script.")

profiles: list = ["Gnome", "KDE Plasma"]

# Show available profiles
for profile_number, profile in enumerate(profiles, start=1):
    print(f"{profile_number}. {profile}")

# Profile selection
selection: str = ""
PROFILE: int = 0

while PROFILE == 0:
    print('Select a profile (enter "c" to cancel):', end=" ")
    selection: str = input()

    if selection.isdigit() and int(selection) in range(1, len(profiles) + 1):
        PROFILE = int(selection)
    else:
        if selection == "c":
            sys.exit(1)
        else:
            print(f"Enter a valid number [1-{len(profiles)}]")


package_list: list = []
PROFILE_FILE: str = ""
DISPLAY_MANAGER: str = ""
match PROFILE:
    case 1:
        print(f"You selected {profiles[0]}")
        PROFILE_FILE = "gnome_packages.txt"
        DISPLAY_MANAGER = "gdm"
    case 2:
        print(f"You selected {profiles[1]}")
        PROFILE_FILE = "plasma_packages.txt"
        DISPLAY_MANAGER = "sddm"
        with open("/etc/sddm.conf", "w", encoding="utf8") as f:
            f.write("[Theme]\nCurrent=breeze")
    case _:
        sys.exit("An error has ocurred.")

# Read packages from profile_file
PROFILE_PATH=f"{SCRIPT_DIR}/profiles/{PROFILE_FILE}"
if os.path.exists(PROFILE_PATH):
    with open(PROFILE_PATH, encoding="utf8") as f:
        for line in f:
            package_list.append(line.rstrip())
else:
    print(f"File {PROFILE_FILE} does not exist")
    sys.exit(1)

# Install packages
if utils.install_packages([*package_list, DISPLAY_MANAGER]) != 0:
    sys.exit(1)

# Enable display manager
utils.enable_services([DISPLAY_MANAGER])

# Configure virtual machine
virt_packages: list = []
VIRT_SERVICE: str = ""
match utils.virt_system():
    case "vmware":
        virt_packages = ["open-vm-tools", "gtkmm3"]
        VIRT_SERVICE = "vmtoolsd"
    case "oracle":
        virt_packages = ["virtualbox-guest-utils"]
        VIRT_SERVICE = "vboxservice"
    case _:
        sys.exit(0)

if utils.install_packages(virt_packages) == 0:
    utils.enable_services([VIRT_SERVICE])
