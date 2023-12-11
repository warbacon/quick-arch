import subprocess
import os

profiles: dict = {1: "Gnome", 2: "KDE Plasma (BETA)"}

for profile_number, profile_name in profiles.items():
    print(f"{profile_number}. {profile_name}")

selection: str = ""
profile: int = 0

while profile == 0:
    print('Select a profile (enter "c" to cancel):', end=" ")
    selection: str = input()

    if selection.isdigit() and int(selection) in profiles:
        profile = int(selection)
    else:
        if selection == "c":
            exit(1)
        else:
            print("Enter a valid number [1-2]")


packages: list = []
profile_file: str = ""
display_manager: str = ""
match profile:
    case 1:
        print(f"You selected {profiles[1]}")
        profile_file = "gnome_packages.txt"
        display_manager = "gdm"
    case 2:
        print(f"You selected {profiles[2]}")
        profile_file = "plasma_packages.txt"
        display_manager = "sddm"
    case _:
        print("An error has ocurred")

if os.path.exists(profile_file):
    with open(profile_file) as f:
        for line in f:
            packages.append(line.rstrip())
else:
    print(f"File {profile_file} does not exist")
    exit(1)

subprocess.run(["sudo", "pacman", "-S", *packages, display_manager])
subprocess.run(["sudo", "systemctl", "enable", display_manager])

match subprocess.run("systemd-detect-virt", capture_output=True).stdout.decode():
    case "vmware":
        subprocess.run(["sudo", "pacman", "-S", "open-vm-tools", "gtkmm3"])
        subprocess.run(["sudo", "systemctl", "enable", "vmtoolsd.service"])
    case "oracle":
        subprocess.run(["sudo", "pacman", "-S", "virtualbox-guest-utils"])
        subprocess.run(["sudo", "systemctl", "enable", "vboxservice.service"])
