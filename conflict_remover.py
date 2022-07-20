import os
import time
import re


reg = re.compile(r'(^.*)( \(SFConflict seafile@benjaminherb\.de \d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\))(\..*$)')
STARTDIR = "/home/ben/Studium/"

for root, dirs, files in os.walk(STARTDIR):
    for file in files:
        if file.find("SFConflict seafile@benjaminherb.de") > -1:
            conf_file = file
            print("-------------------------")
            print("CONFLICT")
            og_file = f"{reg.match(conf_file).group(1)}{reg.match(conf_file).group(3)}"
            og_path = f"{root}/{og_file}"
            conf_path = f"{root}/{conf_file}"
            print(og_path)
            print(conf_path)
            if os.path.isfile(og_path) and os.path.isfile(conf_path):
                og_size = os.path.getsize(og_path)
                conf_size = os.path.getsize(conf_path)
                og_time = os.path.getmtime(og_path)
                conf_time = os.path.getmtime(conf_path)
                print(f"OG:   {og_size} - {time.ctime(og_time)}")
                print(f"CONF: {conf_size} - {time.ctime(conf_time)}")
                if og_size == conf_size:
                    print("MATCHING SIZE")
                    if og_time > conf_time:
                        print("CONF WINS")
                        print(f"Removing {og_path}")
                        os.remove(og_path)
                        print(f"Renaming {conf_path} to {og_path}")
                        os.rename(conf_path, og_path)
                    else:
                        print(f"Removing {conf_path}")
                        os.remove(conf_path)
