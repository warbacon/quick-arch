import subprocess
import os

profiles: dict = {1: "Gnome", 2: "KDE Plasma (BETA)"}

# Show available profiles
for profile_number, profile_name in profiles.items():
    print(f"{profile_number}. {profile_name}")

# Profile selection
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

# Read packages from profile_file
if os.path.exists(profile_file):
    with open(profile_file) as f:
        for line in f:
            packages.append(line.rstrip())
else:
    print(f"File {profile_file} does not exist")
    exit(1)

# Install packages
if subprocess.run(["sudo", "pacman", "-S", *packages, display_manager]).returncode != 0:
    exit(1)

# Enable display manager
subprocess.run(["sudo", "systemctl", "enable", display_manager])

# Configure virtual machine
virt_system: str = subprocess.run(
    "systemd-detect-virt", capture_output=True
).stdout.decode()

virt_packages: list = []
virt_service: str = ""
match virt_system:
    case "vmware":
        virt_packages = ["open-vm-tools", "gtkmm3"]
        virt_service = "vmtoolsd.service"
    case "oracle":
        virt_packages = ["virtualbox-guest-utils"]
        virt_service = "vboxservice.service"

if subprocess.run(["sudo", "pacman", "-S", *virt_packages]).returncode == 0:
    subprocess.run(["sudo", "systemctl", "enable", virt_service])

# Baconize :)
print("Baconize? [y/N]:", end=" ")
selection = input()

match selection:
    case "y" | "Y":
        home_dir = os.environ["HOME"]

        # neovim config
        nvim_dependencies: list = ["nodejs-lts-iron", "npm", "gcc", "fd", "unzip"]
        subprocess.run(["sudo", "pacman", "-S", *nvim_dependencies])

        if not os.path.exists(f"{home_dir}/.config"):
            os.mkdir(f"{home_dir}/.config")

        if not os.path.exists(f"{home_dir}/.config/nvim"):
            os.rmdir(f"{home_dir}/.config/nvim")

        subprocess.run(
            [
                "git",
                "clone",
                "https://github.com/Warbacon/nvim-config",
                f"{home_dir}/.config/nvim",
            ]
        )

        # zunder-zsh
        if not os.path.exists(f"{home_dir}/.config/zunder-zsh"):
            subprocess.run(["git", "clone", "https://github.com/Warbacon/zunder-zsh"])
        else:
            subprocess.run(["git", "pull"], cwd="zunder-zsh")
        subprocess.run("./zunder-zsh/install.sh")
    case _:
        print("No baconize :(")
