#!/bin/sh
set -e

echo "== התקנת OpenShot דרך Flatpak =="

# זיהוי מנהל חבילות לפי ההפצה
if [ -f /etc/os-release ]; then
    . /etc/os-release
fi

install_flatpak() {
    case "$ID" in
        ubuntu|debian|linuxmint|pop|elementary|zorin)
            sudo apt update
            sudo apt install -y flatpak gnome-software-plugin-flatpak
            ;;
        fedora|nobara)
            sudo dnf install -y flatpak
            ;;
        arch|manjaro|endeavouros)
            sudo pacman -Syu --noconfirm flatpak
            ;;
        opensuse*|sles)
            sudo zypper install -y flatpak
            ;;
        *)
            echo "לא זוהתה הפצה מוכרת. התקן ידנית: flatpak + gnome-software-plugin-flatpak"
            exit 1
            ;;
    esac
}

command -v flatpak >/dev/null 2>&1 || install_flatpak

sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
sudo flatpak install -y flathub org.openshot.OpenShot

echo "== הותקן! להרצה: flatpak run org.openshot.OpenShot =="
