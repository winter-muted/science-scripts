#!/usr/bin/env bash

SCRIPT_DIR=`echo $PWD`
#INSTALL_DIR=`echo $HOME/bin`
INSTALL_DIR=`echo $PWD/bin`
#echo $SCRIPT_DIR
INSTALL_DIR=`echo /home/etheros/Bin`
# create the ~/.bin directory if it doesnt exist
echo $INSTALL_DIR

#if [ -d "$INSTALL_DIR" ]; then
#	echo "[Directory]: install dir exists"
#else
#	echo "[Directory]: Creating $INSTALL_DIR"
#	mkdir $INSTALL_DIR
#fi

# install scripts 
#echo "[COPY]: Writing all scripts to install dir"
#cd $SCRIPT_DIR/scripts
#cp * $INSTALL_DIR
#cd $SCRIPT_DIR

# Make sure $INSTALL_DIR is in $PATH
if [ `echo $PATH | grep $INSTALL_DIR` ]; then
	echo "[ENV] install dir in path"
else
	echo "[ENV] adding install dir to ~.bash_profile"
	PATH=$PATH:$INSTALL_DIR
fi



# add the list of script commands to ~/.bashrc




# source ~/.bashrc
