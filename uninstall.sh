#!/bin/sh

PLUGIN_FOLDER=~/.gnome2/gedit/plugins

uninstall_file() {
	if [ -f $PLUGIN_FOLDER/$1 ]; then
		echo " - removing $PLUGIN_FOLDER/$1"
		rm $PLUGIN_FOLDER/$1 || exit 1
	fi
}

echo "\nUninstalling plugin"
uninstall_file 'paired_char_autocomplete.py'
uninstall_file 'paired_char_autocomplete.pyc'
uninstall_file 'paired_char_autocomplete.gedit-plugin'

