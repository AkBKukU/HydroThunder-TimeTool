#!/bin/bash

#in bytes
pre_hash_size=123856361

f_size="$(du -b $1 | awk '{print $1}')"

t_size="$(du -b $2 | awk '{print $1}')"

if [[ "$f_size" == "0" ]]
then
    f_size="$(blockdev --getsize64 $1)"
fi


if [[ "$t_size" == "0" ]]
then
    t_size="$(blockdev --getsize64 $2)"
fi


f_data_start="$(expr $f_size - 123993699 )"
t_data_start="$(expr $t_size - 123993699 )"

echo $f_data_start
echo $t_data_start

if [[ "$3" == "-r" ]]
then
d_skip="skip=$f_data_start"
d_seek=""

elif [[ "$3" == "-w" ]]
then
d_skip=""
d_seek="seek=$t_data_start"

else
d_skip="skip=$f_data_start"
d_seek="seek=$t_data_start"
fi

echo "About to run:"
echo "dd if=$1 of=$2 $d_skip $d_seek count=$pre_hash_size"
read -p "Press enter to continue..."

sudo dd if=$1 of=$2 $d_skip $d_seek count=$pre_hash_size status=progress conv=notrunc \
bs=8M iflag=count_bytes,skip_bytes oflag=seek_bytes
