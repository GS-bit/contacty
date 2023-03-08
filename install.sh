#!/bin/sh

# This is Contacty installation script.

# Checking for root:
if (( $EUID != 0 )); then
    echo "This installation script can only be run by the root user."
    exit
fi

echo "Contacty installation started..."

# Icon:
cp res/contacty.png /usr/share/pixmaps/contacty.png

# Desktop entry:
cp dist/contacty.desktop /usr/share/applications/

# Giving permission of execution to main.py:
chmod +x src/main.py

# Contacty files:
mkdir -p /usr/share/contacty/
cp -r src/ /usr/share/contacty/
cp -r lang/ /usr/share/contacty/
cp -r res/ /usr/share/contacty/
mv /usr/share/contacty/src/main.py /usr/local/bin/contacty
sed -i 's/import sys/import sys\nsys.path.insert(1, "\/usr\/share\/contacty\/src")/g' /usr/local/bin/contacty

# Adding MIME type:
xdg-mime install dist/contacty.xml --novendor
xdg-mime default /usr/share/applications/contacty.desktop application/x-contacty
xdg-icon-resource install --context mimetypes --size 64 res/contacty.png application-x-contacty
update-mime-database /usr/share/mime
update-desktop-database

# All done:
echo "Installation finished."
echo "However, make sure you have PyQt5 installed. You can install it, or test if it is installed, running 'pip install PyQt5'"
