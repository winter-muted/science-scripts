#!/usr/bin/env bash

SCRIPT_DIR=`echo $PWD`
INSTALL_DIR=`echo $HOME/.bin`

# get an array of script names from names (later use)
mapfile < names
NUM_SCRIPTS="${#MAPFILE[@]}"

# set up directory
if [ -d "$INSTALL_DIR" ]; then
	echo "[DIR]: Install dir $INSTALL_DIR exists"
else
	echo "[DIR]: Creating $INSTALL_DIR"
	mkdir $INSTALL_DIR
fi

# install scripts
echo "[CPY]: Writing all scripts to install dir"
cd $SCRIPT_DIR/scripts
cp * $INSTALL_DIR
cd $SCRIPT_DIR

# Make sure $INSTALL_DIR is in $PATH
# apparently, .bash_profile is the proper location for path additions
if [ `echo $PATH | grep $INSTALL_DIR` ]; then
	echo "[ENV]: Install dir in path"
else
	echo "[ENV]: Now add install dir to ~/.bash_profile:"
	echo -n '<code> echo '\''PATH=$PATH:' && echo "$INSTALL_DIR' >> ~/.bash_profile </code>"

fi

# TODO make this work
# add an alias for each command to remove interpreter dependency
# aka test-1.py -> test-1     test-2.sh -> test-2

#for ((i = 0; i < $NUM_SCRIPTS; i++))
#do
#	echo "alias

echo "Finished."
