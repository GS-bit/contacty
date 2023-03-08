#!/bin/sh

# This is Contacty uninstall script.

# Checking for root:
if (( $EUID != 0 )); then
    echo "This uninstall script can only be run by the root user."
    exit
fi

echo "Contacty uninstall started..."

# Icon:
rm /usr/share/pixmaps/contacty.png

# Desktop entry:
rm /usr/share/applications/contacty.desktop

# Contacty files:
rm -rf /usr/share/contacty/
rm /usr/local/bin/contacty

# Removing MIME type:
xdg-mime uninstall dist/contacty.xml
xdg-icon-resource uninstall --context mimetypes --size 64 contacty.png application-x-contacty
update-mime-database /usr/share/mime
update-desktop-database

echo "Uninstall finished."
echo "If you want to remove PyQt5 too, use 'pip uninstall PyQt5' command. Make sure you don't have other program that uses PyQt5 in your computer before running this command."
