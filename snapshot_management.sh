#!/bin/sh

date=$(date +"%Y%m%d_%H%m")

sudo btrfs subvolume snapshot -r / /.snapshots/root/${date}_snapshot_root
sudo btrfs subvolume snapshot -r /home /.snapshots/home/${date}_snapshot_home


