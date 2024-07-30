from Bio import SeqIO
from absl import app,logging,flags
import os
import pandas as pd
import subprocess
flags.DEFINE_string("genome_dat","","The input influenza genome dat that includes all NCBI influenza ids and host ox codes")
flags.DEFINE_string("msa_dir","","directory where all the pickles and their uniprot.sto are stored")
flags.DEFINE_string("host_ox_codes","","file that maps host ox names to codes")
FLAGS = flags.FLAGS

def prepare_genome_dat():
    df = pd.read_table(FLAGS.genome_dat,low_memory=False,header=None)
    df = df.iloc[:,0:2]
    df.columns = ["ID",'host_ox']
    return df

def prepare_host_ox_df():

    df = pd.read_csv(FLAGS.host_ox_codes)
    return df

def prepare_mapping_results(id_map_df:pd.DataFrame,host_ox_df):
    csv_files = [i for i in os.listdir() if i.startswith("mapping_results_")]
    output_dict = {}
    for csv_file in csv_files:
        for line in open(csv_file,'r'):
            key = line.split(",")[1]
            value = line.split(",")[0]
            if id_map_df['ID'].eq(value).any():
                host_ox_name = id_map_df[id_map_df["ID"]==value]['host_ox'].values[0]
                if host_ox_df['species_name'].eq(host_ox_name).any():
                    host_ox_code = host_ox_df[host_ox_df['species_name']==host_ox_name]["ox"].values[0]
                    logging.info(f"uniprot is {key} ncbi_id is {value} and host_ox_code is {host_ox_code}")
                    output_dict[key.rstrip()] = host_ox_code
                else:
                    output_dict[key.rstrip()] = "no_ox_code"
            else:
                logging.info(f"value is : {value} and not in mapping df")
                output_dict[key.rstrip()]="no_ox_code"

    return output_dict

def modify_stockhom(sto_file_dir:str,mapping_results:dict):
    new_uniprot_sto = os.path.join(sto_file_dir,"new_uniprot.sto")
    old_uniprot_sto = os.path.join(sto_file_dir,"uniprot.sto")
    with open(new_uniprot_sto,"w") as outfile:
        for line in open(old_uniprot_sto,'r'):
            line = line.strip()
            if line and line.startswith(('#', '//')):
                print(line,file=outfile)
            elif line and not line.startswith(('#', '//')):
                name, sequence = line.split()
                if "|" in name:
                    uniprot = name.split("|")[1]
                    if uniprot in mapping_results:
                        logging.info(f"{uniprot} in sto has host ox : {mapping_results[uniprot]}")
                        name = f"host_OX={mapping_results[uniprot]}|{name}"
                print(f"{name}\t {sequence}",file=outfile)
    
        outfile.close()
def remove_and_rename_sto(sto_file_dir):
    new_uniprot_sto = os.path.join(sto_file_dir,"new_uniprot.sto")
    old_uniprot_sto = os.path.join(sto_file_dir,"uniprot.sto")
    os.rename(old_uniprot_sto,os.path.join(sto_file_dir,"old_uniprot.sto"))
    os.rename(new_uniprot_sto,os.path.join(sto_file_dir,"uniprot.sto"))

def main(argv):
    
    genome_dat = prepare_genome_dat()
    host_ox_df = prepare_host_ox_df()
    map_dict = prepare_mapping_results(genome_dat,host_ox_df)
    all_proteins = [i.split(".")[0] for i in os.listdir(FLAGS.msa_dir) if i.endswith(".pkl")]
    for protein in all_proteins:
        work_dir = os.path.join(FLAGS.msa_dir,protein)
        modify_stockhom(work_dir,map_dict)
        remove_and_rename_sto(work_dir)
if __name__ == "__main__":
    app.run(main)