#!/usr/bin/env python
# generator.py - iterate and generate statute
import generator
import sys

def do_generate(target_file):
    with open(target_file, 'r') as buf:
        task = generator.Task.from_json(buf)

    if task.generator == "printing":
        generator.printing.generate(task)
    else:
        sys.stderr.write('Unknown generator {}, stopped.'.format(task.generator))
        return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: generate.py [target_file]')
    else:
        do_generate(sys.argv[1])
