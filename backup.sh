#!/bin/bash

# Formatting
BOLD=$(tput bold)
NORMAL=$(tput sgr0)

script_dir="$(cd "$(dirname "$(readlink -f ${BASH_SOURCE[0]})")" &>/dev/null && pwd)"
backup_dir="/run/media/ben/Backup"

# telegram.sh token
token="TOKEN"
chat="CHAT"

## Start

echo
echo "${BOLD}BORGBACKUP${NORMAL}"
echo
echo "$backup_dir"
echo

if [[ -d "$backup_dir"/data/ ]]; then
    borg list $backup_dir
    echo
else
    echo "No backupdisk found"
    echo "ABORT!"
    exit 0
fi

## Choice

echo "${BOLD}Choose Backups Directories:${NORMAL} Daten (0) | Video (1) | Projekt (2) | System (3) | Games (4)"
read -e backup
echo

## Backup Drives

syntax=' '

if [[ $backup == *"0"* ]]; then
    syntax=$syntax' /mnt/Daten/'
fi

if [[ $backup == *"1"* ]]; then
    syntax=$syntax' /mnt/Video/'
fi

if [[ $backup == *"2"* ]]; then
    syntax=$syntax' /mnt/Projekt/'
fi

if [[ $backup == *"3"* ]]; then
    syntax=$syntax' /mnt/Windows/ /home/ben'
fi

if [[ $backup == *"4"* ]]; then
    syntax=$syntax' /mnt/Games/'
fi

## Check

echo "${BOLD}Following command will be used:${NORMAL}"
echo borg create --progress $backup_dir::$(date +%Y_%m_%d) $syntax
echo

echo "${BOLD}Shutdown after the backup? (y/n)${NORMAL}"
read -e shutdown
while [ ! $shutdown == "y" ] && [ ! $shutdown == "n" ]; do
    echo
    echo "${BOLD}Invalid answer! Shutdown after the backup? (y/n)${NORMAL}"
    read -e shutdown
done

echo
echo "${BOLD}Press enter to start backup...${NORMAL}"
read -e
echo

## Execution + Log

archive="$backup_dir::$(date +%Y_%m_%d)"

command="borg create --progress $archive $syntax"
echo "-------------------------"
echo
startTime=$(date +%s)

$script_dir/telegram -c $chat -t $token -H  "<b>Borg Backup Started</b>"$'\n'"$command"

$command

endTime=$(date +%s) elapsedTime=$(($endTime - $startTime))

((h = $elapsedTime / 3600))
((m = $elapsedTime % 3600 / 60))
((s = $elapsedTime % 60))

h=$(printf "%02d" $h)
m=$(printf "%02d" $m)
s=$(printf "%02d" $s)

info_file="/tmp/$(date +%Y_%m_%d)_backup_info.txt"

borg info "$archive" > "$info_file"

$script_dir/telegram -c $chat -t $token -H "<b>Borg Backup Complete</b> ($h:$m:$s)"
$script_dir/telegram -c $chat -t $token -f "$info_file"

rm  "$info_file"

## Shutdown
if [[ $shutdown == "y" ]]; then
    echo
    echo "Shutting down in 60s"
    sleep 60
    shutdown
fi
