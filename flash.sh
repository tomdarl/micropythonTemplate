# usage: ./flash.sh <main.py> [-u] 

#check first arg is a file
[ -f "$1" ] || exit
PROG="$1"

# determine OS type and mount location
LINUX=0
MAC=0
MOUNT_DIR=""

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    LINUX=1
    MOUNT_DIR="/media/$USER"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    MAC=1
    MOUNT_DIR="/Volumes"
else
    echo "Unknown OS"
fi

# flash pyb
echo "flashing pyb with $PROG"
cp $PROG $MOUNT_DIR/SD/main.py
cp _drivers/*.py $MOUNT_DIR/SD/

# unmount SD card
if [[ "$2" == "-u" ]]; then 
	echo "unmounting SD card"

	if [ "$LINUX" -eq "1" ]; then
	    umount $MOUNT_DIR/SD
	elif [ "$MAC" -eq "1" ]; then
	    diskutil unmount SD
	else 
		echo "Unknown OS"
	fi
fi 
