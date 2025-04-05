from Bio import SeqIO
import os

# --- Config ---
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
alignment_file = os.path.join(repo_root, 'restriction_analysis', 'ferret-stoat_alignment.fa')
restrict_file = os.path.join(repo_root, 'restriction_analysis', 'gappedrestrict', 'ferret_unique_sites.txt')
output_file = os.path.join(repo_root, 'restriction_analysis', 'gappedrestrict', 'ferret_sites_filtered.txt')

# --- Load ferret sequence (ungapped) ---
records = SeqIO.to_dict(SeqIO.parse(alignment_file, 'fasta'))
ferret_id = [r for r in records if r.lower().startswith("ferret")][0]
ferret_seq = str(records[ferret_id].seq).replace('-', '')
ferret_len = len(ferret_seq)

# --- Filter restriction sites ---
filtered = []
with open(restrict_file, 'r') as fh:
    for line in fh:
        if not line.strip():
            continue
        pos, enzyme = line.strip().split()
        pos = int(pos)

        # Keep enzymes with 5+ bp recognition, and not too close to sequence edges
        if 100 < pos < (ferret_len - 100) and len(enzyme) >= 5:
            filtered.append((pos, enzyme))

# --- Save output ---
with open(output_file, 'w') as out:
    for pos, enzyme in filtered:
        out.write(f"{pos}\t{enzyme}\n")

print(f"Filtered to {len(filtered)} restriction sites.")
print(f"Saved to: {output_file}")
