# usage: ./flash.sh <main.py> [-u] 

# user defs
SD_CARD="SD"

# globals
MOUNT_DIR=""
UNMOUNT=""

# check first arg is a file
[ -f "$1" ] || exit
PROG="$1"

# determine OS type and mount location 
if [[ "$OSTYPE" == "linux-gnu" ]]; then
    MOUNT_DIR="/media/$USER"
    UNMOUNT="umount $MOUNT_DIR/"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    MOUNT_DIR="/Volumes"
    UNMOUNT="diskutil unmount "
else
    echo "Unknown OS"
fi

# flash pyb
echo "flashing pyb with $PROG"
cp $PROG $MOUNT_DIR/$SD_CARD/main.py
cp _drivers/*.py $MOUNT_DIR/$SD_CARD/

# unmount SD card
if [[ "$2" == "-u" ]]; then 
    echo "unmounting SD card"
    $UNMOUNT$SD_CARD
fi 
