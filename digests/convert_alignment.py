import sys
import glob
import os

def getgaps(pos, ref):
    """Takes a position in the original sequence and outputs the position in the aligned sequence (accounting for gaps)."""
    workpos = 0
    gaps = 0
    for f in ref:
        if f == '-':
            gaps += 1
        else:
            workpos += 1
        if workpos == pos:
            break
    return gaps

def splitalignment(filename):
    """Takes a FASTA file containing alignments and outputs a dictionary with accession number as key and sequence as value."""
    sequences = {}
    seqlist = []
    with open(filename, 'r') as alignment:
        for line in alignment:
            if line[0] == '>':
                seqname = line[1:].split('/')[0].split('.')[0]
                seqlist.append(seqname.upper())
                sequences[seqname.upper()] = []
            else:
                sequences[seqname.upper()].append(line.strip())
    for f in seqlist:
        sequences[f] = ''.join(sequences[f])
    return sequences

# --- Config ---
infile = 'ferret_alignment.fa'  # Real input FASTA file
if len(sys.argv) > 1:
    infile = sys.argv[1]
    print(f'Processing {infile}')

sequences = splitalignment(infile)

newdirect = 'gappedrestrict'  # Real output folder name
os.makedirs(newdirect, exist_ok=True)

extension = '.restrict'  # Real file extension
filelist = [f for f in glob.glob("*" + extension)]
files = [f[0:-(len(extension))] for f in filelist if f[0:-(len(extension))].upper() in sequences]

print('Processing:', files)

for file in files:
    print(f'Going through file {file + extension}')
    with open(file + '.restrict', 'r') as fhin:
        with open(os.path.join(newdirect, file + 'new.restrict'), 'w') as fhout:
            linein = fhin.readline()
            while len(linein) <= 3 or linein.strip()[0] == '#':
                print(linein, end='', file=fhout)
                linein = fhin.readline()
            linein = '\t'.join(linein.strip().split())
            print(linein, file=fhout)

            for line in fhin:
                if len(line) <= 3 or line.strip()[0] == '#':
                    print(line, end='', file=fhout)
                else:
                    line = line.strip().split()
                    gapcount = getgaps(int(line[0]), sequences[file.upper()])
                    for position in [0, 1, 5, 6, 7, 8]:
                        if len(line) > position and line[position] != '.':
                            line[position] = str(int(line[position]) + gapcount)
                    line = '\t'.join(line)
                    print(line, file=fhout)
