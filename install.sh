#!/bin/sh
#
# Installs the plugin to the users folder

PLUGIN_FOLDER=~/.gnome2/gedit/plugins

install_file() {
	echo " - adding $1 to $PLUGIN_FOLDER"
	cp "$1" "$PLUGIN_FOLDER" || exit 1
}

# Install plugin
echo "\nInstalling plugin"
mkdir -p $PLUGIN_FOLDER
install_file 'paired_char_autocomplete.py'
install_file 'paired_char_autocomplete.gedit-plugin'

echo '\n*** Restart gedit to complete the installation ***\n'



