from ete3 import NCBITaxa

input_file = "TAXONOMIC-VERNACULAR-FR-CURATED-221125.txt"
output_file = "TAXONOMIC-VERNACULAR-FR-CURATED-221125-FILTERED-241125.txt"

ncbi = NCBITaxa()
seen = set()

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in fin:
        line = line.rstrip("\r\n")
        if not line:
            continue

        parts = line.split("\t")

        taxid, latin_name, vernacular = parts

        #if no vernacular name, skip
        if vernacular == "" or vernacular.lower() == "none":
            print(taxid)           
            continue

        # replace Latin name by NCBI official name if taxid exists
        if taxid != "" and taxid.lower() != "none":
            try:
                taxid_int = int(taxid)
                true_name = ncbi.get_taxid_translator([taxid_int]).get(taxid_int, latin_name)
            except Exception:
                true_name = latin_name
        else:
            true_name = latin_name  # keep original if no taxid

        # deduplicate on (taxid, true_name, vernacular)
        triplet = (taxid, true_name, vernacular)
        if triplet not in seen:
            seen.add(triplet)
            fout.write(f"{taxid}\t{true_name}\t{vernacular}\n")
