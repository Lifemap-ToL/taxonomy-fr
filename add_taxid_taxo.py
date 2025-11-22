#!/usr/bin/env python3
from ete3 import NCBITaxa
import pandas as pd
import sys
from datetime import datetime

inp = sys.argv[1]

ncbi = NCBITaxa()

# generate date-hour string
dh = datetime.now().strftime("%Y%m%d-%H%M")

out_file = f"TAXO-WITH-TAXID-{dh}.txt"
problem_file = f"TAXO-PROBLEMS-{dh}.txt"

# --- Load GBIF backbone locally ---
usecols = ['taxonID', 'canonicalName', 'taxonomicStatus', 'acceptedNameUsageID']
df = pd.read_csv("backbone/Taxon.tsv", sep="\t", dtype=str, usecols=usecols)
# df = pd.read_csv("backbone/Taxon.tsv", sep="\t", dtype=str)

# Accepted taxa
accepted_dict = dict(zip(
    df.loc[(df['taxonomicStatus'] == 'accepted') & df['canonicalName'].notna(), 'canonicalName'],
    df.loc[(df['taxonomicStatus'] == 'accepted') & df['canonicalName'].notna(), 'taxonID']
))

# Synonyms
syn_df = df.loc[(df['taxonomicStatus'] == 'synonym') & df['canonicalName'].notna() & df['acceptedNameUsageID'].notna(),
                ['canonicalName', 'acceptedNameUsageID']]
syn_dict = dict(zip(syn_df['canonicalName'], syn_df['acceptedNameUsageID']))

# Map taxonID -> canonicalName
id_to_name = dict(zip(df.loc[df['taxonID'].notna(), 'taxonID'], 
                      df.loc[df['taxonID'].notna(), 'canonicalName']))


# # accepted taxa: canonicalName -> taxonID
# accepted_dict = {row['canonicalName']: row['taxonID']
#                  for _, row in df.iterrows() if row['taxonomicStatus'] == 'accepted'}
# print("done")
# # synonyms: canonicalName -> accepted taxonID
# syn_dict = {row['canonicalName']: row['acceptedNameUsageID']
#             for _, row in df.iterrows() if row['taxonomicStatus'] == 'synonym'}
# print("done")
# # taxonID -> canonicalName (to resolve acceptedNameUsageID)
# id_to_name = {row['taxonID']: row['canonicalName'] for _, row in df.iterrows()}
# print("done")

# --- Function to resolve a name locally ---
def gbif_accepted_name_local(name):
    if name in accepted_dict:
        return name  # already accepted
    elif name in syn_dict:
        accepted_id = syn_dict[name]
        if pd.isna(id_to_name.get(accepted_id)):
            return None  # no accepted name found
        return id_to_name.get(accepted_id)  # resolved canonical name
    else:
        return None  # not found in backbone


# --- Main processing ---
with open(inp) as f, open(out_file, "w") as g, open(problem_file, "w") as p:
    # count total lines for progress
    total = sum(1 for _ in f if _.strip())
    f.seek(0)  # rewind file

    for i, line in enumerate(f, 1):
        if not line.strip():
            continue
        latin, vern = line.rstrip("\n").split("\t")

        # NCBI lookup first
        taxids = ncbi.get_name_translator([latin]).get(latin, [])

        # if not found, resolve locally via GBIF backbone
        if len(taxids) == 0:
            accepted = gbif_accepted_name_local(latin)
            if accepted:
                taxids = ncbi.get_name_translator([accepted]).get(accepted, [])

        if len(taxids) == 0:
            g.write(f"\t{latin}\t{vern}\n")
        else:
            if len(taxids) > 1:
                msg = f"Multiple taxids for {latin}: {','.join(map(str, taxids))}"
                print(f"Warning: {msg}", file=sys.stderr)
                p.write(msg + "\n")
            for t in taxids:
                g.write(f"{t}\t{latin}\t{vern}\n")

        # print progress x/total
        print(f"Progress: {i}/{total}", end="\r", file=sys.stderr)

print(file=sys.stderr)  # newline at end
