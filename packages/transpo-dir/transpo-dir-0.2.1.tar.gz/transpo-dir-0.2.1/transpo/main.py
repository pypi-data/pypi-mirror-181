import os
import shlex
import sys

from docopt import docopt


def fixed_depth_walk(top_dir, depth):
    from os import listdir
    from os.path import join, isdir

    def w_i(top_list, depth_remain):
        assert depth_remain >= 1

        top_dir = join(*top_list)
        names = sorted(listdir(top_dir))

        for name in names:
            l = top_list + [name]

            p = join(top_dir, name)
            if not isdir(p):
                yield 'f', l
            elif depth_remain == 1:
                yield 'd', l
            else:
                yield from w_i(l, depth_remain - 1)
    
    yield from w_i([top_dir], depth)


__doc__ = """Transpose directory structure.

Usage:
  transpo [options] <src> -d DEST

Options:
  -d DEST       Destination directory.
  -i INDICES, --index-order=INDICES     The order of indices for transpose [default: 21].
"""


def main():
    normpath = os.path.normpath
    quote = shlex.quote
    join = os.path.join
    def qj(*l):
        return quote(join(*l))

    args = docopt(__doc__)

    src_dir = normpath(args['<src>'])
    dest_dir = normpath(args['-d'])

    try:
        index_order = [int(v) for v in args['--index-order']]
    except ValueError:
        sys.exit("Error: invalid string as index order: %s" % repr(args['--index-order']))
    e = [i + 1 for i in range(len(index_order))]
    if len(index_order) < 2 or sorted(index_order) != e:
        sys.exit("Error: wrong index order (such as duplicated or missing): %s" % repr(args['--index-order']))
    if index_order == e:
        sys.exit("Error: index order is kept as same, not transposed: %s" % repr(args['--index-order']))

    if os.path.exists(dest_dir):
        sys.exit('Error: destination directory exists: %s' % dest_dir)

    # setup as a bash script
    print("#!/bin/bash")
    print("set -ex")  # stop on any error / show commands being executed
    print()

    # make the destination directory
    print("mkdir %s" % quote(dest_dir))

    # make and move directories
    len_index_order = len(index_order)
    mkdir_done_set = set()
    direct_child_dir_set = set()
    direct_child_dir_set_having_unmovable_files = set()
    for k, n in fixed_depth_walk(src_dir, len_index_order):
        if k == 'f':
            if len(n) >= 2:
                direct_child_dir_set_having_unmovable_files.add(tuple(n[:2]))
            print("# unmovable file: %s" % qj(*n))
            continue  # for k, n

        direct_child_dir_set.add(tuple(n[:2]))
        transposed_dir = [dest_dir] + [n[i] for i in index_order[:-1]]
        t = tuple(transposed_dir)
        if t not in mkdir_done_set:
            print("mkdir -p %s" % qj(*transposed_dir))
            mkdir_done_set.add(t)
        transposed_n = transposed_dir + [n[index_order[-1]]] + n[len_index_order + 1:]
        print("mv %s %s" % (qj(*n), qj(*transposed_n)))

    # remove original directories
    for c in sorted(direct_child_dir_set):
        if c not in direct_child_dir_set_having_unmovable_files:
            print("rm -rf %s" % qj(*c))

if __name__ == '__main__':
    main()
