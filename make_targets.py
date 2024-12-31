"""
Given a valid path to a directory with a makefile,
identify all the make targets and print them to stdout. 
"""

import os
import sys

IGNORED_TARGETS = {"."}    

partial_target = sys.argv[1] if len(sys.argv) > 1 else ""
makefile_candidates = [f for f in os.listdir('.') if f.lower().startswith('makefile')]

if not makefile_candidates:
    print("No Makefile found")
    pass

targets = []
try:
    with open(makefile_candidates[0], 'r') as f: # only analyze the first makefile found
        for line in f:
            if ':' in line and not line.strip().startswith('#'):
                target = line.split(':')[0].strip() # isolate the make target
                if not any(target.startswith(ignore_target) for ignore_target in IGNORED_TARGETS):
                    if len(partial_target) > 0:
                        if target.startswith(partial_target):
                            targets.append(target)
                    else:
                        targets.append(target)
except FileNotFoundError:
    print("No Makefile found")
    pass

targets.sort()
for target in targets:
    print(target)