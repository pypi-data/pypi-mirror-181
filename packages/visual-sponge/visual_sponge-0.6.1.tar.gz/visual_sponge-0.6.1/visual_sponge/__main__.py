import sys
from collections import deque
from pathlib import Path

from . import MACROS
from .backend import run


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("""Visual Sponge
    Visualization tool for SPONGE

usage: visual-sponge [MODEL [TRAJ [TRAJ2 [TRAJ3... ]]]] [--debug] [-h] 

optionals:
    -h, --help:         show this help and exit
    MODEL:              the model (topology) file to load
    TRAJ:               the trajectory file to load
    -d, --debug:        the flag that enables the debug mode
""")
        sys.exit(0)
    files = deque()
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue
        if arg == "--debug":
            MACROS.DEBUG_MODE = True
        else:
            files.appendleft(str(Path(arg)))

    run(files)

if __name__ == "__main__":
    main()
