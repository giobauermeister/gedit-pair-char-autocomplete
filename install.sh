#!/bin/sh
#
# Installs the plugin to the users folder

PLUGIN_FOLDER=~/.local/share/gedit/plugins
ICON_FOLDER=~/.local/share/icons

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
install_file 'pair_char_completion.py'
install_file 'pair_char_lang.py'
install_file 'pair_char_completion.plugin'
install_icon 'pair_char_completion.png'

echo '\n*** Restart gedit to complete the installation ***\n'

