from Bio import SeqIO
import os

# --- Config ---
script_dir = os.path.dirname(__file__)
repo_root = os.path.abspath(os.path.join(script_dir, '..'))

alignment_file = os.path.join(repo_root, 'restriction_analysis', 'ferret-stoat_alignment.fa')
ferret_id = 'FERRET'
restrict_file = os.path.join(repo_root, 'restriction_analysis', 'gappedrestrict', 'ferret_unique_sites.txt')
output_file = os.path.join(repo_root, 'primer3', 'ferret_primer3_input.txt')


flank = 100  # 100bp on each side

# --- Load aligned sequences ---
sequences = {}
with open(alignment_file, 'r') as fh:
    for record in SeqIO.parse(fh, 'fasta'):
        seq_id = record.id.split('/')[0].split('.')[0].upper()
        sequences[seq_id] = str(record.seq)

# Make sure ferret is in there
if ferret_id not in sequences:
    raise ValueError(f"Could not find {ferret_id} in alignment FASTA.")

ferret_seq = sequences[ferret_id]
seq_len = len(ferret_seq)

# --- Read restriction sites ---
with open(restrict_file, 'r') as fh:
    sites = [line.strip().split() for line in fh if line.strip()]
    sites = [(int(pos), enzyme) for pos, enzyme in sites]

# --- Generate Primer3 input ---
with open(output_file, 'w') as out:
    for pos, enzyme in sites:
        start = max(0, pos - flank)
        end = min(seq_len, pos + flank)

        chunk = ferret_seq[start:end]
        site_in_chunk = pos - start  # relative position
        site_len = 6  # default restriction site length

        out.write(f"SEQUENCE_ID=Ferret_{pos}_{enzyme}\n")
        out.write(f"SEQUENCE_TEMPLATE={chunk}\n")
        out.write(f"SEQUENCE_TARGET={site_in_chunk},{site_len}\n")
        out.write("=\n")

print(f"Primer3 input written to: {output_file}")
