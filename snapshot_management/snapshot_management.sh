#!/bin/sh

date=$(date +"%Y%m%d_%H%m")

home_snap_dir="/.snapshots/home/"
root_snap_dir="/.snapshots/root/"

sudo btrfs subvolume snapshot -r / ${root_snap_dir}${date}_root
sudo btrfs subvolume snapshot -r /home ${home_snap_dir}${date}_home


home_snap_count=$(ls $home_snap_dir | wc -l)
while [ $home_snap_count -gt 10 ]; do
    snap_to_delete=$(ls -1 $home_snap_dir | head -n 1)
    sudo btrfs subvolume delete ${home_snap_dir}$snap_to_delete
    home_snap_count=$(ls $home_snap_dir | wc -l)
    echo "REMOVED ${home_snap_dir}${snap_to_delete} - ${home_snap_count} SNAPSHOTS LEFT!"
done


root_snap_count=$(ls $root_snap_dir | wc -l)
while [ $root_snap_count -gt 10 ]; do
    snap_to_delete=$(ls -1 $root_snap_dir | head -n 1)
    sudo btrfs subvolume delete ${root_snap_dir}$snap_to_delete
    home_snap_count=$(ls $root_snap_dir | wc -l)
    echo "REMOVED ${root_snap_dir}${snap_to_delete} - ${root_snap_count} SNAPSHOTS LEFT!"
done
