import os

# Get the current script directory so paths always work
script_dir = os.path.dirname(__file__)
gapped_path = os.path.join(script_dir, '..', 'restriction_analysis', 'gappedrestrict')


def read_restrict_file(filepath):
    sites = set()
    with open(filepath, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('#') or line.lower().startswith("start"):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            start = int(parts[0])
            enzyme = parts[3]
            key = (start, enzyme)
            sites.add(key)
    return sites

# Actual file paths
ferret_file = os.path.join(gapped_path, 'ferretnew.restrict')
stoat_file = os.path.join(gapped_path, 'stoatnew.restrict')

# Read in both
ferret_sites = read_restrict_file(ferret_file)
stoat_sites = read_restrict_file(stoat_file)

# Compare
ferret_unique = ferret_sites - stoat_sites
stoat_unique = stoat_sites - ferret_sites

# Output results (in gappedrestrict folder)
with open(os.path.join(gapped_path, 'ferret_unique_sites.txt'), 'w') as f_out:
    for start, enzyme in sorted(ferret_unique):
        f_out.write(f"{start}\t{enzyme}\n")

with open(os.path.join(gapped_path, 'stoat_unique_sites.txt'), 'w') as f_out:
    for start, enzyme in sorted(stoat_unique):
        f_out.write(f"{start}\t{enzyme}\n")

print("Unique restriction sites saved to:")
print(" - gappedrestrict/ferret_unique_sites.txt")
print(" - gappedrestrict/stoat_unique_sites.txt")
