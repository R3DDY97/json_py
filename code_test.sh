#!/bin/bash


cd sample_json

parser="$HOME/Documents/GEEK_SK00L/json_py/jsons.py"

clear
printf "\nWill be testing parser using  the below Sample JSON files .....\n\n"
printf "FILENAME     SIZE\n"
ls -lh | awk '{print $9 "  " $5}'
printf "\n\tPress Enter key to start testing one by one......."
read

for i in *json
do
    clear
    printf "Using $i \n"
    sleep 0.5
    printf "\njsons.py $i\n\n"
    sleep 1
    python3 ../jsons.py $i
    echo
    read -p "Press Enter key to test next sample JSON file"
done

printf "\nDone testing with available JSON files.....\n\n"
