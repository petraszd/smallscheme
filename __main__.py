#!/usr/bin/env python
from smallscheme.runner import Runner
from smallscheme.datatypes import Null
from smallscheme import SchemeError
import sys
import os
import traceback

def repl():
    runner = Runner()
    print("--- smallscheme REPL. Press CTRL+D to exit.")
    while 1:
        try:
            sys.stdout.write("> ")
            src = raw_input().strip()
            if not src:
                continue
            result = runner.run(src)
            if not result is Null:
                print(str(result))
        except EOFError:
            print("")
            print("--- Good bye!")
            break
        except SchemeError as e:
            print(str(e))
        except Exception as e:
            print("Interpretation error: %s" % e)
            #traceback.print_exc()

def run_file(filename):
    runner = Runner()
    with open(filename, 'r') as f:
        try:
            runner.run(f.read())
        except Exception as e:
            print(str(e))

if len(sys.argv) > 1:
    if not os.path.exists(sys.argv[1]):
        print("File: %s does not exists..." % (sys.argv[1]))
    else:
        run_file(sys.argv[1])
else:
    repl()

