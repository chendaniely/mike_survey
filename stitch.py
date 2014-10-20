import sys

fp = open(sys.argv[2], 'w')

for n, file in enumerate(open(sys.argv[1])):
    for m, line in enumerate(open(file.rstrip())):
            dat = line.rstrip().split(',')
            dat.insert(0, file.rstrip().split('.txt')[0])
            fp.write('%s\n' % ','.join(dat))
