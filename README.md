# Substitute_Influenza_taxID_with_host_taxID
Scripts that were used to change the TaxID of the uniprot alignments of the Influenza sequences 
into its corresponding Host TaxID

# Step 1: Download Influnza genome dataset from NCBI
NCBI Influenza genome dataset stored sequences of all the Influenza viruses from GenBank. The information of which host organisms these Influenza strains infect is stored in a file called genomeset.dat.
This file can be downloaded via the link: https://ftp.ncbi.nih.gov/genomes/INFLUENZA/genomeset.dat

The version of genomeset.dat used in the thesis was downloaded on 17/03/2024, which can be downloaded via this link: https://drive.google.com/file/d/1xWEnhNHfJHMLgizyAavAXGaOySguemyi/view?usp=share_link 

# Step 2: Map Genbank ID to UniProt Accession
Since the sequences in this genomeset.dat file are annotated with the Genbank IDs but in the UniProt alignment file created by AlphaFold Multimer, the aligned homologues were annotated with UniProt accessions.
Thus it is necessary to map the Genbank IDs to UniProt accessions. Before mapping, all the Genbank IDs from the genomeset.dat were extracted and deduplicated. ```all_genbank_ids.txt``` in this repo is the result
of the deduplication. Then, run the following command:
```
python map_genbank_to_uniprot.py --input_genbank=./all_genbank_ids.txt 
```
This python script will generate a series of ```genbank_mapping_results_xxx.json```files. I have change the json files into CSV tables so that the mapping results are easier to be processed in the next steps.
The CSV tables can be downloaded from: https://drive.google.com/drive/folders/18ic57NGFNZeIOuMHaLxiEB17RcDV_HWz?usp=share_link

# Step 3: Change the Influenza taxonomy IDs into host taxonomy IDs in the UniProt alignment file
After AlphaFold alignes the sequence against the UniProt database, an MSA file called ```uniprot.sto``` will be created. All the aligned sequences are stored in the stockholm format.
With the CSV tables creted by **Step 2**, now it is ready to substitute the taxonomy IDs of the Influenza homologues with the host organism taxonomy IDs.
Run the following command:
```python modify_uniprot_fasta.py --genome_dat=./genomeset.dat \
  --msa_dir=/g/alphafold/influenza_gs/ --host_ox_codes=./influenza_host_species_OX_codes.csv
```
⚠️ ```/g/alphafold/influenza_gs/``` is the path to all the sequene alignment results on the EMBL HPC cluster in Heidelberg. Each Influenza protein has its own subfolder under this path
```
/g/alphafold/influenza_gs/
      |- A0A2Z5U3Y7/
              |-bfd_uniref_hits.a3m
              |-mgnify_hits.sto
              |-old_uniprot.sto
              |-uniprot.sto
              ...
      |- B4UPG3/
              |-bfd_uniref_hits.a3m
              |-mgnify_hits.sto
              |-old_uniprot.sto
              |-uniprot.sto
              ...
      ...
```
# Step 4: Re-run the feature generation step of AlphaPulldown
After **Step 3**, the first step of AlphaPulldown needs to be rerun but using the updated uniprot.sto files. Simply run the ```create_individual_features.py```script from [AlphaPulldown](https://github.com/KosinskiLab/AlphaPulldown/tree/main)
but with the ```use_precomputed_msas``` flag turned on.

