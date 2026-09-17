
# Goal of this project
The aim of this repository is to propose an up-to-date correspondance between latin and vernacular french names for as many taxa as possible. This is used for the [french version of the Lifemap Explorer of the tree of Life](http://lifemap-fr.univ-lyon1.fr)


# Current reference file

[`TAXONOMIC-VERNACULAR-FR-LATEST.txt`](TAXONOMIC-VERNACULAR-FR-LATEST.txt) is the maintained reference file used by the Lifemap backend. Make future name corrections in this file and document them in a new dated `UPDATE YYYY-MM-DD` section below, with the most recent update first. The dated curated and filtered files are historical snapshots.

Each record has three tab-separated columns: NCBI taxid, scientific name, and French vernacular name. Multiple vernacular names can be associated with the same taxid. Some records have no taxid; these are retained for possible future matching.

# UPDATE 2026-09-17

Restored `TAXONOMIC-VERNACULAR-FR-CURATED-221125-FILTERED-241125.txt`, which was missing from the working directory, from its committed version in Git. Its contents are unchanged from the historical snapshot. Reorganized this README into dated update sections and clarified which file to edit for future corrections. No changes were made to `TAXONOMIC-VERNACULAR-FR-LATEST.txt` in this update.

# UPDATE 2026-01-14

Created `TAXONOMIC-VERNACULAR-FR-LATEST.txt` from the filtered snapshot as the reference file for subsequent updates and use by the Lifemap backend.

Corrected the French name for **Pomacanthidae** (NCBI taxid **30862**) from **demoiselles** to **Poissons-anges**. This is the only record that differs between the restored filtered snapshot and `LATEST` at this date. Both files contain **147,027 records**.

# UPDATE 2025-11-24

Used `final-modif-update-latinname-remove-dup.py` to produce `TAXONOMIC-VERNACULAR-FR-CURATED-221125-FILTERED-241125.txt` from the curated file:

- Replaced scientific names with the official NCBI names for their taxids where available.
- Removed records with an empty vernacular name or a name equal to `None` (case-insensitive).
- Removed duplicate combinations of taxid, normalized scientific name, and vernacular name.
- Retained records without a taxid for possible future use. An initial version removed them; this was corrected on the same day.
- Fixed handling of leading tabs so that records with an empty taxid retain the correct column structure.

The resulting file contains **147,027 records**, down from **209,316** in the curated file, while retaining **41,995 distinct nonempty taxids**. Of these records, **74,497** have no taxid.

# UPDATE 2025-11-22

Used `add_taxid_taxo.py` to transform `TAXONOMIC-VERNACULAR-FR.txt` into `TAXO-WITH-TAXID-20251122-0153.txt`. NCBI taxids were retrieved from scientific names using ete3. When no taxid was found, GBIF was queried for synonyms that could be matched to NCBI.

Ambiguous scientific names matching multiple taxids were recorded in `TAXO-PROBLEMS-20251122-0153.txt`. These cases were resolved manually after checking external sources, producing `TAXONOMIC-VERNACULAR-FR-CURATED-221125.txt`.

The curated file contains **209,316 records**, including **74,511** without a taxid, and **41,995 distinct nonempty taxids**. It is the input to the subsequent filtering step described above.

# Dataset produced
Using the three data sources listed below (GBIF, INPN and wikidata), and the dedicated code `extract-taxo.py` we recover vernacular names for 140 538 distinct taxa. 

The resulting tab-delimited file, `TAXONOMIC-VERNACULAR-FR.txt`, contains one vernacular name per taxa, so that taxa with multiple vernacular names are present multiple times. This file contains 209 313 rows.

# Data sources and retrieval strategies

For now, three sources of data are used. Here is the Venn diagram representing the content of each data source (in terms of the number of taxa with vernacular names in French) and their overlap. 

![venn diagram taxonomy comparison FR](img/venn.png)

> In total, we recover vernacular names for 140 538 distinct taxa. 


**1. Wikidata**


Wikidata is a great resource for species names translation. The following code (Sparkle) can be used to retrieve the common names of taxons in french, using the online service [https://query.wikidata.org](https://query.wikidata.org/).

```
SELECT DISTINCT ?sci ?comm WHERE {
  ?taxon wdt:P31 wd:Q16521;
    wdt:P225 ?sci;
    wdt:P1843 ?comm.
  FILTER(LANGMATCHES(LANG(?comm), "fr"))
  SERVICE wikibase:label { bd:serviceParam wikibase:language "fr". }
} 
```


The downloaded result (tsv format) is called `query.tsv`
> Vernacular names for 18 955 taxa (April 20th, 2020)

- data was modified as follows: 
    + Duplicates with other databases were removed. The version with more uppercase letters was always prefered. 

**2. GBIF**


GBIF contains vernacular names for many species in many languages. A single zip file can be downloaded here : 
http://rs.gbif.org/datasets/backbone/backbone-current.zip

The important files here are `VernacularName.tsv` and `Taxon.tsv`

> Vernacular names for 33 359 taxa (April 20th, 2020)

- data was modified as follows: 
    + Duplicates with other databases were removed. The version with more uppercase letters was always prefered. 

**3. INPN**


The INPN is a great resource for species names of species living in France (but not the others). The complete data can be downloaded from https://inpn.mnhn.fr/docs-web/docs/download/301786

The important file here is `TAXREFvXX.txt` where XX is the current version.

> Vernacular names for 114 193 taxa (April 20th, 2020; TAXREFv13)

- data was modified as follows: 
    + Articles (Le, La, L') were removed
    + Duplicates with other databases were removed. The version with more uppercase letters was always prefered. 

# Ambiguities
Of course, nothing is always simple, and some ambiguities exist because some taxa that are at distant in the tree of life have the same name. The most famous example is a genera of inscects that is called... __Bacteria__.  

Other example : 
- __Arenaria__ : genus of birds (Family: __Scolopacidae__) and genus of flower (Family: Caryophylaceae). The latter is called "Sablines" in french.


# Contributions 
If you think that some important data sources should be added, please open an issue indicating the resource you have in mind, and I will try to integrate it.

If you identify errors in the french names, please open an issue.  


Please note the GBIF ans INPN are already combining data from a variety of sources. 


For questions, remarks, or if you want to help and contribute, please send me an email or open an issue. 

# Citation 
If you use this dataset, please cite the paper presenting Lifemap: de Vienne DM. 2016. Lifemap: Exploring the Entire Tree of Life. PLOS Biolgy.



