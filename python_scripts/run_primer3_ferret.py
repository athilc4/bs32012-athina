import os

# --- Path setup ---
script_dir = os.path.dirname(__file__)
repo_root = os.path.abspath(os.path.join(script_dir, '..'))

input_file = os.path.join(repo_root, 'primer3', 'ferret_primer3_input.txt')
raw_output_file = os.path.join(repo_root, 'primer3', 'ferret_primer3_raw_output.txt')
filtered_output_file = os.path.join(repo_root, 'primer3', 'ferret_primer3_filtered_output.txt')

# --- Step 1: Run Primer3 ---
print("Running Primer3 on ferret input...")
os.system(f"primer3_core < {input_file} > {raw_output_file}")

# --- Step 2: Parse and filter output ---
primer_hits = []

with open(raw_output_file, "r") as infile:
    blocks = infile.read().split("=")

for block in blocks:
    lines = block.strip().splitlines()
    if not lines:
        continue

    result = {
        "SEQUENCE_ID": None,
        "PRIMER_LEFT_SEQUENCE": None,
        "PRIMER_RIGHT_SEQUENCE": None,
        "PRODUCT_SIZE": None,
        "TM_LEFT": None,
        "TM_RIGHT": None
    }

    for line in lines:
        if line.startswith("SEQUENCE_ID="):
            result["SEQUENCE_ID"] = line.split("=")[1]
        elif line.startswith("PRIMER_LEFT_0_SEQUENCE="):
            result["PRIMER_LEFT_SEQUENCE"] = line.split("=")[1]
        elif line.startswith("PRIMER_RIGHT_0_SEQUENCE="):
            result["PRIMER_RIGHT_SEQUENCE"] = line.split("=")[1]
        elif line.startswith("PRIMER_PAIR_0_PRODUCT_SIZE="):
            result["PRODUCT_SIZE"] = int(line.split("=")[1])
        elif line.startswith("PRIMER_LEFT_0_TM="):
            result["TM_LEFT"] = float(line.split("=")[1])
        elif line.startswith("PRIMER_RIGHT_0_TM="):
            result["TM_RIGHT"] = float(line.split("=")[1])

    if all(result.values()):
        if 100 <= result["PRODUCT_SIZE"] <= 300 and 58 <= result["TM_LEFT"] <= 62 and 58 <= result["TM_RIGHT"] <= 62:
            primer_hits.append(result)

# --- Step 3: Save filtered hits ---
with open(filtered_output_file, "w") as out:
    for hit in primer_hits:
        out.write(f"🧬 {hit['SEQUENCE_ID']}\n")
        out.write(f"Forward Primer: {hit['PRIMER_LEFT_SEQUENCE']} (Tm: {hit['TM_LEFT']:.2f})\n")
        out.write(f"Reverse Primer: {hit['PRIMER_RIGHT_SEQUENCE']} (Tm: {hit['TM_RIGHT']:.2f})\n")
        out.write(f"Product Size: {hit['PRODUCT_SIZE']} bp\n")
        out.write("-" * 50 + "\n")

print(f"Filtered primer pairs saved to: {filtered_output_file}")
