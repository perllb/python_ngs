#!/usr/bin/env python

import sys

for line in sys.stdin:
    items=line.split('\t')
    print(items)
    try:
        attr=dict(item.strip().split(' \"') for item in line.split('\t')[8].strip('\n').split(';') if item)
        print(attr)
        sys.stdout.write("chr" + items[0] + "\t" + items[3] + "\t" + items[4] + "\t" + attr['gene_name'].strip('\"') + "\t" + "." + "\t" + items[6] + "\n")
    except Exception as e:
        print(e)
        print(items)
