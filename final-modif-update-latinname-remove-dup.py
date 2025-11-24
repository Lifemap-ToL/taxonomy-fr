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

        parts = line.split("\t")
        if len(parts) < 3:
            continue

        taxid, latin_name, vernacular = parts

        # if no taxid → ignore
        if taxid == "" or taxid.lower() == "none":
            continue

        # resolve true latin name
        try:
            taxid_int = int(taxid)
            true_name = ncbi.get_taxid_translator([taxid_int]).get(taxid_int)
        except Exception:
            continue  # invalid taxid

        if true_name is None:
            continue

        triplet = (taxid, true_name, vernacular)

        # write only first occurrence
        if triplet not in seen:
            seen.add(triplet)
            fout.write(f"{taxid}\t{true_name}\t{vernacular}\n")
