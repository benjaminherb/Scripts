#!/bin/bash

## Inputfarben
color='tput setaf 5'
nocolor='tput sgr0'

##Start
echo "RAWSUCHER"
echo

## Abfragen was kopiert werden soll
echo "$($color)Auswahlordner:$($nocolor)"
read -e selection
echo "$($color)Bilderordner:$($nocolor)"
read -e origin
echo "$($color)RAW-Extension(zB:\".ARW\"):$($nocolor)"
read -e extension
echo "$($color)Auswahl-Extension(zB:\".JPG\"):$($nocolor)"
read -e selextension

## Speicherort festlegen
echo
echo "Standardspeicherort für AuswahlJPG und AuswahlRAW ändern? (Default ist der Bilderordner: $origin)"
echo "$($color)y/n:$($nocolor)"
read -e changelocation

if [ $changelocation == y ]; then
    echo "$($color)Neuer Speicherort:$($nocolor)"
    read -e savepath
else
    savepath="$origin"
fi

## Zielordner erstellen (und prüfen ob es ihn schon gibt)
echo
cd "$savepath"

if [ -d "$savepath"/AuswahlRaw ]; then
    echo AuswahlRaw gibt es bereits
else
    mkdir AuswahlRaw
    echo created folder AuswahlRaw in $savepath
fi

if [ -d "$savepath"/AuswahlJPG ]; then
    echo AuswahlJPG gibt es bereits
else
    mkdir AuswahlJPG
    echo created folder AuswahlJPG in $savepath
fi

## Variablen für die Zielordner festlegen
cd AuswahlRaw
destinationraw=$(pwd)
cd ..
cd AuswahlJPG
destinationjpg=$(pwd)

## Wie oft muss der Prozess wiederholt werden?
cd "$selection"
fotoamount=$(ls *$selextension -1 2>/dev/null | wc -l)
echo
echo $fotoamount Fotos

## JPG und RAW in die jeweiligen Ordner verschieben/kopieren
echo
for ((fotoamount; fotoamount > 0; fotoamount--)); do
    file=$(find . -name "*$selextension" 2>/dev/null | head -n 1)
    name=$(echo "$file" | cut -c3- | rev | cut -c5- | rev)
    mv "$file" "$destinationjpg"
    fileraw=$(find "$origin" -name $name$extension)
    cp "$fileraw" "$destinationraw"
    echo $name JPEG und RAW kopiert
done

## Fragt ob die JPGs wieder in den ursprünglichen Ordner kopiert werden sollen
echo
echo "JPEGs im ursprünglichen Auswahl Ordner behalten (wurden in AuswahlJPG kopiert)?"
echo "$($color)y/n:$($nocolor)"
read -e backtofolder

if [ $backtofolder == y ]; then
    cp "$destinationjpg"/*.{JPG,jpg,Jpg,jpeg,JPEG} "$selection" 2>/dev/null
    echo
    echo Fertig
else

    ## Schaut ob der Auswahlordner leer ist fragt ob er gelöscht werden soll (sofern er leer ist)
    if [ -z "$(ls -A "$selection")" ]; then
        echo "Den leeren ürsprüngliche Auswahlordner löschen?"
        echo "$($color)y/n:$($nocolor)"
        read -e del

        if [ $del == y ]; then
            rmdir "$selection"
            echo Ordner wurde gelöscht!
        else
            echo Ordner wurde nicht gelöscht
        fi
    else
        echo Der Auswahlordner ist nicht leer und wurde daher nicht gelöscht werden
    fi

fi
