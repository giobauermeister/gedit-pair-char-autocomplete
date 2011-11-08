#!/bin/sh

PLUGIN_FOLDER=~/.local/share/gedit/plugins
ICON_FOLDER=~/.local/share/icons

uninstall_file() {
	if [ -f $PLUGIN_FOLDER/$1 ]; then
		echo " - removing $PLUGIN_FOLDER/$1"
		rm $PLUGIN_FOLDER/$1 || exit 1
	fi
}

uninstall_icon() {
	if [ -f $ICON_FOLDER/$1 ]; then
		echo " - removing $ICON_FOLDER/$1"
		rm $ICON_FOLDER/$1 || exit 1
	fi 
}

echo "\nUninstalling plugin"
uninstall_file 'pair_char_completion.plugin'
uninstall_file 'pair_char_completion.py'
uninstall_file 'pair_char_lang.py'
uninstall_file 'pair_char_completion.pyc'
uninstall_file 'pair_char_lang.pyc'
uninstall_icon 'pair_char_completion.png'

