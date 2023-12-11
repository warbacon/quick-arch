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


packages_list: list = []
packages_file: str = ""
display_manager: str = ""
match profile:
    case 1:
        print(f"You selected {profiles[1]}")
        packages_file = "gnome_packages.txt"
        display_manager = "gdm"
    case 2:
        print(f"You selected {profiles[2]}")
        packages_file = "plasma_packages.txt"
        display_manager = "sddm"
    case _:
        print("An error has ocurred")

if os.path.exists(packages_file):
    with open(packages_file) as f:
       for line in f:
           packages_list.append(line.rstrip())
else:
    print(f"File {packages_file} does not exist")
    exit(1)

packages: str = " ".join(packages_list)
os.system(f"sudo pacman -S {packages} {display_manager}")
os.system(f"sudo systemctl enable {display_manager}")
