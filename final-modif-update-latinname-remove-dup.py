from ete3 import NCBITaxa

input_file = "TAXONOMIC-VERNACULAR-FR-CURATED-221125.txt"
output_file = "TAXONOMIC-VERNACULAR-FR-CURATED-221125-FILTERED-241125.txt"

ncbi = NCBITaxa()
seen = set()

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in fin:
        line = line.strip()
        if not line:
            continue

        # ensure at least 3 columns
        parts = line.split("\t")
        while len(parts) < 3:
            parts.insert(0, "")  # pad missing taxid at start

        taxid, latin_name, vernacular = parts

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
