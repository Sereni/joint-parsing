"""
Add range markers to xbest file obtained with english morph-analyzer
"""

with open('/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/english_cutoff/eng_test_0.9') as f:
    out = open('/Users/Sereni/PycharmProjects/Joint Parsing/parser/data/english_cutoff/eng_test_0.9_', 'w')
    last_index = '0'
    for line in f:
        if line == '\n':
            last_index = 0
            out.write(line)
        else:
            index = line.split('\t')[0]
            if index != last_index:
                last_index = index
                out.write('{0}-{0}\n'.format(index))
                out.write(line)
            else:
                out.write(line)