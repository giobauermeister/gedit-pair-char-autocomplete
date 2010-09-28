#!/bin/sh
#
# Installs the plugin to the users folder

PLUGIN_FOLDER=~/.gnome2/gedit/plugins
ICON_FOLDER=~/.icons

install_file() {
	echo " - adding $1 to $PLUGIN_FOLDER"
	cp "$1" "$PLUGIN_FOLDER" || exit 1
}

install_icon() {
  echo " - adding $1 to $ICON_FOLDER"
	cp "$1" "$ICON_FOLDER" || exit 1
}

# Install plugin
echo "\nInstalling plugin"
mkdir -p $PLUGIN_FOLDER
mkdir -p $ICON_FOLDER
install_file 'paired_char_autocomplete.py'
install_file 'paired_char_autocomplete.gedit-plugin'
install_icon 'auto-pair-48.png'

echo '\n*** Restart gedit to complete the installation ***\n'

