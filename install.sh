#!/usr/bin/env bash

SCRIPT_DIR=`echo $PWD`
INSTALL_DIR=`echo $HOME/.bin`

# get an array of script names from names (later use)
mapfile < names
NUM_SCRIPTS="${#MAPFILE[@]}"
echo $NUM_SCRIPTS

# set up directory
if [ -d "$INSTALL_DIR" ]; then
	echo "[DIR]: install dir exists"
else
	echo "[DIR]: Creating $INSTALL_DIR"
	mkdir $INSTALL_DIR
fi

# install scripts 
echo "[COPY]: Writing all scripts to install dir"
cd $SCRIPT_DIR/scripts
cp * $INSTALL_DIR
cd $SCRIPT_DIR

# Make sure $INSTALL_DIR is in $PATH
# apparently, .bash_profile is the proper location for path additions
if [ `echo $PATH | grep $INSTALL_DIR` ]; then
	echo "[ENV] install dir in path"
else
	echo "[ENV] adding install dir to ~.bash_profile"
	PATH=$PATH:$INSTALL_DIR
fi

# TODO make this work
# add an alias for each command to remove interpreter dependency
# aka test-1.py -> test-1     test-2.sh -> test-2

#for ((i = 0; i < $NUM_SCRIPTS; i++))
#do
#	echo "alias

# source ~/.bashrc
