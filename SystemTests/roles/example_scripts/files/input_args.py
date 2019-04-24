from __future__ import print_function

import sys

if __name__ == "__main__":
    output_dir = sys.argv[1]
    arg2 = sys.argv[2] if len(sys.argv) > 2 else "2nd"
    arg3 = sys.argv[3] if len(sys.argv) > 3 else "3rd"
    arg4 = sys.argv[4] if len(sys.argv) > 4 else "4th"

    print("First argument is %s" % output_dir)
    print("Second argument is %s" % arg2)
    print("Third argument is %s" % arg3)
    print("Fourth argument is %s" % arg4)
