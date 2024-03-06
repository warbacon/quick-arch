#!/usr/bin/env bash

install_package() {
    sudo pacman -S --needed --noconfirm "$@"
}

install_general() {
    local packages=(
        wl-clipboard
        power-profiles-daemon
    )

    install_package "${packages[@]}"
    sudo systemctl enable power-profiles-daemon.service
}

install_gnome() {
    local packages=(
        evince
        gnome-backgrounds
        gnome-calculator
        gnome-characters
        gnome-control-center
        gnome-disk-utility
        gnome-font-viewer
        gnome-logs
        gnome-shell
        gnome-terminal
        gst-plugins-good
        gvfs-google
        loupe
        malcontent
        nautilus
        sushi
        tracker3-miners
        xdg-desktop-portal-gnome
        xdg-user-dirs-gtk
    )

    install_package "${packages[@]}"
    install_package gdm
    sudo systemctl enable gdm.service
}

install_plasma() {
    local packages=(
        breeze-gtk
        dolphin
        ffmpegthumbs
        kde-gtk-config
        kdegraphics-thumbnailers
        kdeplasma-addons
        kio-gdrive
        konsole
        kscreen
        okular
        plasma-desktop
        plasma-nm
        plasma-pa
        plasma-wayland-session
        sddm-kcm
        xdg-desktop-portal-gtk
        xdg-desktop-portal-kde
        xsettingsd
    )

    install_package "${packages[@]}"
    install_package sddm
    sudo systemctl enable sddm.service
    sudo tee -a /etc/sddm.conf >/dev/null <<EOF
[Theme]
Current=breeze
EOF
}

install_hyprland() {
    local packages=(
        hyprland
        kitty
        mako
        waybar
        xdg-desktop-portal-hyprland
    )

    install_package "${packages[@]}"

    # PROVISIONAL
    install_package sddm
    sudo systemctl enable sddm.service
}

configure_vm() {
    case "$VIRT_SYSTEM" in
        "vmware")
            install_package open-vm-tools gtkmm3
            sudo systemctl enable vmtoolsd.service
            ;;
        "oracle")
            install_package virtualbox-guest-utils
            sudo systemctl enable vboxservice.service
            ;;
        *)
            echo "Jaja no que ha pasao."
            ;;
    esac
}

main() {
    if which gum &>/dev/null; then
        gum_was_installed=true
    else
        sudo pacman -S gum || {
            echo "gum is required."
            exit 1
        }
    fi

    SELECTED_PROFILE="$(gum choose 'Gnome' 'KDE Plasma' 'Hyprland')"

    [[ -n "$SELECTED_PROFILE" ]] && echo "You selected $SELECTED_PROFILE."

    install_general

    case "$SELECTED_PROFILE" in
        "Gnome")
            install_gnome
            ;;
        "KDE Plasma")
            install_plasma
            ;;
        "Hyprland")
            install_hyprland
            ;;
        *)
            echo "Cancelled."
            exit 1
            ;;
    esac

    VIRT_SYSTEM="$(systemd-detect-virt)"
    VIRT_SYSTEM="${VIRT_SYSTEM//[$'\n']/}"

    if [[ "$VIRT_SYSTEM" != "none" ]]; then
        configure_vm
    fi

    if [[ "$gum_was_installed" != true ]]; then
        sudo pacman -Rns gum
    fi
}

main "$@"
