import sys
import glob
import os

def getgaps(pos, ref):
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
    sequences = {}
    current_seqname = ""
    with open(filename, 'r') as alignment:
        for line in alignment:
            if line.startswith('>'):
                seqname = line[1:].split()[0].upper()
                sequences[seqname] = []
                current_seqname = seqname
            else:
                sequences[current_seqname].append(line.strip())
    for key in sequences:
        sequences[key] = ''.join(sequences[key])
    return sequences

def process_restrict(species_name, sequences, newdirect):
    filename = species_name + '.restrict'
    aligned_seq = sequences[species_name.upper()]
    output_filename = os.path.join(newdirect, species_name + 'new.restrict')
    
    with open(filename, 'r') as fhin, open(output_filename, 'w') as fhout:
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
                gapcount = getgaps(int(line[0]), aligned_seq)
                for position in [0, 1, 5, 6, 7, 8]:
                    if len(line) > position and line[position] != '.':
                        line[position] = str(int(line[position]) + gapcount)
                line = '\t'.join(line)
                print(line, file=fhout)
    return output_filename

# ---------- MAIN ----------
infile = 'ferret_alignment.fa'
if len(sys.argv) > 1:
    infile = sys.argv[1]
    print(f'Processing alignment file: {infile}')

sequences = splitalignment(infile)
newdirect = 'gappedrestrict'
os.makedirs(newdirect, exist_ok=True)

# Process both species
ferret_output = process_restrict('ferret .1', sequences, newdirect)
stoat_output = process_restrict('stoat .1', sequences, newdirect)

print(f'Finished processing:\n - {ferret_output}\n - {stoat_output}')

# Optional: Combine both into one file
combined_output = os.path.join(newdirect, 'ferret_stoat_combined.restrict')
with open(combined_output, 'w') as fout:
    for file in [ferret_output, stoat_output]:
        with open(file, 'r') as fin:
            fout.write(f'# From file: {file}\n')
            fout.writelines(fin.readlines())

print(f'Combined file written to: {combined_output}')
