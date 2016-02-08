#!/bin/bash
echo ------------------------
echo Setup script by meastro
echo ------------------------
echo
echo ------------------------
echo checking for clean script!
echo ------------------------
clean=clean.sh
if [ -f $clean ]; then
    echo "$clean found!"
    rm $clean
    wget -q https://raw.githubusercontent.com/maestroi/Hardeningdebian/master/clean.sh
    chmod 755 $clean
    echo "$clean newest version downloaded!"
else 
    echo "$clean does not exist"
    wget -q https://raw.githubusercontent.com/maestroi/Hardeningdebian/master/clean.sh
    chmod 755 $clean
    echo "$clean new version downloaded!"
fi
echo ------------------------
echo done checking script!
echo ------------------------

echo ------------------------
echo update ubuntu
echo ------------------------

update=1
if [ $update -eq 1 ]; then
    sudo apt-get update && sudo apt-get upgrade -y
    update=2
fi

echo ------------------------
echo update finished
echo ------------------------
