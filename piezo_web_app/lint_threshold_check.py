import sys
from pylint import lint

THRESHOLD = 9.00

if len(sys.argv) < 2:
    raise Exception("Module to evaluate needs to be the first argument")

run = lint.Run([sys.argv[1]], do_exit=False)
score = run.linter.stats['global_note']

if score < THRESHOLD:
    print("exit code = 1")
    sys.exit(1)
print("exit code = 0")
print("Passed with threshold level set at {}".format(THRESHOLD))
