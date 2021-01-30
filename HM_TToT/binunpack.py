import sys
import os

def unpack(file):
    pass
    return


if __name__ == "__main__":
    if len(sys.argv) == 1:

        sys.exit()
    path = sys.argv[1]
    fdir = os.path.dirname(os.path.realpath(path))
    input()
    fname = os.path.basename(path)
    os.mkdir(fdir + "/" fname)
    with open(sys.argv[1]) as f:
        
        unpack(f)