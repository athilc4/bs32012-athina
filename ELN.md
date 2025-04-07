# Electronic Lab Notebook BS32012
_**Project Title:**_ Mitochondrial DNA-Based Identification of Mustelid Species from Scat

_**Module Manager:**_ Dr David Martin 

_**Student:**_ Athina Lorraine Chatziplis

_**Student ID:**_ 2406306

---

## Week 1 - 24th to 28th of February
**Title:** Identification of the Appropriate Sequences 

**Aim:** Effective searching and acquisition of the mitochondrial sequences of the black footed ferret and stoat.

**Method:** Web based search on the NCBI website [https://www.ncbi.nlm.nih.gov/](https://www.ncbi.nlm.nih.gov/) for the appropriate species.

**Results:** 
1. Identified and downloaded mitochondrial sequences for *Mustela nigripes* (black footed ferret) and *Mustela erminea* (stoat) from NCBI
2. Saved files to the project repository as `black_footed_ferret.fasta` and `stoat.fasta`. They were placed into the folder `sequences` of the repository which was subsequently created. 

---

## Week 2 – 3rd to 7th of March
**Title:**  Sequence Alignment, Restriction Site Identification and Position Adjustment for Alignment Gaps

**Aim:** Align sequences, produce `.restrict` files and then adjust the output via python scripts to ensure appropriate alignment of the circular genomes (gapped restrict).

**Method:** 
1. Aligned ferret and stoat sequences using Jalview software 
2. Ran EMBOSS restrict on both sequences to find enzyme cut sites
3. Generated a python script to organise the contents of `*.restrict.orig` files into numerical order.
4. Wrote another two python scripts to correct restriction site positions, within the `*.restrict` files, based on gapped alignment.
5. A third python script was generated to identify the unique sites present in each of the two species'

**Results:** 
1.  Produced alignment and exported it as `ferret-stoat_alignment.fa` in new `/restriction_analysis` folder; also changed the sequence headers in the alignment from accession numbers to  'ferret' and 'stoat' in order for them to work with restriction files.
2. Running EMBOSS restrict produced two files: `ferret.restrict` and `stoat.restrict`. These files were also placed in `/restriction_analysis`.
```bash
restrict -auto -enzymes /usr/share/EMBOSS/data/REBASE/embossre.enz -sequence stoat.fasta -outfile stoat.restrict
```
3. A custom script named `sortmyfiles.sh` was then run and re-produced the output files: `ferret.restrict` and `stoat.restrict` but sorted into numerical order. The original (unsorted) outputs of EMBOSS were renamed to `ferret.restrict.orig` and `stoat.restrict.orig` respectively.

```bash
mv ferret.restrict ferret.restrict.orig 
head -n 26 ferret.restrict.orig > ferret.restrict 
tail -n +27 ferret.restrict.orig | head -n -10 | sort -n >> ferret.restrict 
tail -n 10 ferret.restrict.orig >> ferret.restrict
```
4. `convert-ferret.py` and `convert-stoat.py` were ran on the `*.restrict` files, resulting in the output of: `ferretnew.restrict` and `stoatnew.restrict`, which were placed in the new subfolder: `/restriction_analysis/gappedrestrict`.
5. The `find_unique_sites.py` script successfully produced: `ferret_unique_sites.txt` and `stoat_unique_sites.txt` which detail the sites unique to each species; and are located in `/restriction_analysis/gappedrestrict` of the repository. 

**Notes:** All python scripts used are located in the `/python_scripts` folder of the repository except the two `convert-*.py` scripts which operate from within `/restriction_analysis` and subsequently had to be placed there. 

---

## Week 3 – 10th to 14th of March
**Title:** Site Selection

**Aim:** Extract appropriate data for primer design, filter primer candidates to narrow selection, select sites.

**Method:** 
1. Extracted 100bp upstream and downstream of each unique site using python script and `*_unique_sites.txt`
2. Chose the ferret DNA to be cut
3. Narrowed down selection of primers using python

**Results:** 
1. Generated Primer3 input file: `ferret_primer3_input.txt` using `generate_ferret_primer3_input.py` python script and placed into new folder `primer3` in repository.
2. Utilised `filter_ferret_sites.py` script to filter based on GC content (40–60%), avoidance of long homopolymers and sequence length (200bp). Output: `ferret_sites_filtered.txt`
3. Proceeded to choose three candidate sites at random to test from the output file: NIaIV, BsrBI, BaeI

**Notes:** `stoat_primer3_input.txt` was also produced in case it was needed at any point 

---

## Week 4 - 17th to 21st of March
 
**Title:** Primer Design and Verification

**Aim:** Acquire appropriate primer pairs for each site

**Method:** Used Primer3 web interface to test the three candidates and produce primer pairs for each


**Results:** Primer3 software deemed the three candidate sites appropriate for this experiment as they produced satisfactory primer pairs

---

## Week 5 – 24th to 28th of March
**Title:** Specificity Testing via Benchling and Confirmation via BLAST

**Aim:**
Ensure that selected sites are ferret specific

**Method:**
1. Extracted same aligned region from stoat and simulated enzyme digest in Benchling
2. BLASTed each ferret amplicon against NCBI nucleotide database.

**Results:** 
1. Confirmation of Cut in ferret  / No cut in stoat 
2.  BLAST results: Top hit: *Mustela nigripes* only / No significant stoat matches

---