import getopt
args = '-a -b -cfoo -d bar a1 a2'.split()
optlist, args = getopt.getopt(args, 'abc:d:')
print(optlist)
print(args)