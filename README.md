# Substitute_influenza_taxID_with_host_taxID
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
