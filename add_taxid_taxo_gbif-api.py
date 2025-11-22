#!/usr/bin/env python3
from ete3 import NCBITaxa
import requests
import sys
from datetime import datetime

inp = sys.argv[1]

ncbi = NCBITaxa()

# generate date-hour string
dh = datetime.now().strftime("%Y%m%d-%H%M")

out_file = f"TAXO-WITH-TAXID-{dh}.txt"
problem_file = f"TAXO-PROBLEMS-{dh}.txt"

def gbif_accepted_name(name):
    r = requests.get("https://api.gbif.org/v1/species/match", params={"name": name}).json()
    if r.get("matchType") == "NONE":
        return None
    if r.get("status") == "ACCEPTED":
        return r.get("canonicalName")
    acc = r.get("acceptedUsageKey")
    if acc:
        d = requests.get(f"https://api.gbif.org/v1/species/{acc}").json()
        return d.get("canonicalName")
    return None

# first pass: count lines
with open(inp) as f:
    total = sum(1 for _ in f if _.strip())

with open(inp) as f, open(out_file, "w") as g, open(problem_file, "w") as p:
    for i, line in enumerate(f, 1):
        latin, vern = line.rstrip("\n").split("\t")
        taxids = ncbi.get_name_translator([latin]).get(latin, [])

        if len(taxids) == 0:
            accepted = gbif_accepted_name(latin)
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

        # print current progress as x/total
        print(f"Progress: {i}/{total}", end="\r", file=sys.stderr)

# print newline at the end to avoid overwriting
print(file=sys.stderr)
