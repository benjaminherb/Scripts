import os
import time
import re

# --- USERCONFIG --- #

STARTDIR = "/mnt/Daten/Design/"
TESTRUN = True
reg = re.compile(
    r'(^.*)( \(SFConflict seafile@benjaminherb\.de \d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\))(\..*$)')

# --- END OF USERCONFIG --- #


# https://stackoverflow.com/questions/8924173/how-to-print-bold-text-in-python
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    YELLOW = '\033[93m'
    RED = '\033[31m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class File:
    def __init__(self, file, path, size=0,
                 mod_time=time.time(), color=color.END):
        self.file = file
        self.path = path
        self.size = size
        self.mod_time = mod_time
        self.color = color


def main():
    counter = {
        'conflicts': 0,
        'conflicts_removed': 0,
        'originals_removed': 0,
    }

    for root, dirs, files in os.walk(STARTDIR):
        for file in files:
            if file.find("SFConflict seafile@benjaminherb.de") > -1:
                print(f"{color.BOLD}CONFLICT{color.END} {file}")
                original, conflict = check_conflict(file, root)

                print(f"{original.color}ORIGINAL  {original.size}  "
                      f"{time.ctime(original.mod_time)}  "
                      f"{original.path}{color.END}")
                print(f"{conflict.color}CONFLICT  {conflict.size}  "
                      f"{time.ctime(conflict.mod_time)}  "
                      f"{conflict.path}{color.END}")
                print("-------------------------")

                counter['conflicts'] = counter['conflicts'] + 1
                if conflict.color == color.RED:
                    counter['conflicts_removed'] = counter['conflicts_removed'] + 1
                if original.color == color.RED:
                    counter['originals_removed'] = counter['originals_removed'] + 1

    print(f"{color.BOLD}CONFLICTS: {counter['conflicts']}\n"
          f"ORIGINALS REMOVED: {counter['originals_removed']}\n"
          f"CONFLICTS REMOVED: {counter['conflicts_removed']}")


def check_conflict(file, root):
    conflict = File(file, f"{root}/{file}")
    _original_file = f"{reg.match(conflict.file).group(1)}{reg.match(conflict.file).group(3)}"
    original = File(_original_file, f"{root}/{_original_file}")

    if os.path.isfile(original.path) and os.path.isfile(conflict.path):
        original.size = os.path.getsize(original.path)
        conflict.size = os.path.getsize(conflict.path)
        original.mod_time = os.path.getmtime(original.path)
        conflict.mod_time = os.path.getmtime(conflict.path)
        if original.size == conflict.size:
            if original.mod_time > conflict.mod_time:
                original.color = color.RED
                conflict.color = color.GREEN
                if not TESTRUN:
                    os.remove(original.path)
                    os.rename(conflict.path, original.path)
            else:
                conflict.color = color.RED
                original.color = color.GREEN
                if not TESTRUN:
                    os.remove(conflict.path)

    return original, conflict


if __name__ == "__main__":
    main()
