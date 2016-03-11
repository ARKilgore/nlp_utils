import sys

if len(sys.argv) != 3:
    sys.exit('Incorrect number of args')

window_size = 5

with open(sys.argv[1], 'r') as fpi, open(sys.argv[2], 'w') as fpo:
    fpi.readline()
    outside_indices = {}
    outside_count = 0
    inside_count = 0
    for line in fpi:
        idx _ _ cdx _ _ _ = line.split(' ')
        idx = int(idx)
        cdx = int(cdx)
        # Outside
        if cdx < idx - window_size or cdx > idx + window_size:
            inside_count += 1
        else:
            outside_count += 1
            if cdx in outside_indices:
                outside_indices[cdx] += 1
            else:
                outside_indices[cdx] = 1
    fpo.write('total inside outside')
    fpo.write(str(inside_count+outside_count) + ' ' + str(inside_count) + ' ' + str(outside_count) + '\n')
    map(lambda (i, count): fpo.write(str(i)+':'+str(count)+' ', outside_indices.iteritems()))

