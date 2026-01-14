
# Goal of this project
The aim of this repository is to propose an up-to-date correspondance between latin and vernacular french names for as many taxa as possible. This is used for the [french version of the Lifemap Explorer of the tree of Life](http://lifemap-fr.univ-lyon1.fr)


# UPDATE NOV. 2025
In this important update, we did the following: 
with the code `add_taxid_taxo.py` wo transformed the file `TAXONOMIC-VERNACULAR-FR.txt` into a new file `TAXO-WITH-TAXID-20251122-0153.txt` by getting taxids from NCBI from the names thants to ete3 and when the taxid was not found, we queried gbif to see if the name was the synonym of another one and if yes this other one was used to recover the taxid. *

In the process we also recovered all AMBIGUITIES: when a latin name corresponds to multiple taxids. These cases were written down in `TAXO-PROBLEMS-20251122-0153.txt`by the script. 

Finally, the problems were solved manually after internet lookup to correct the names in order to produce the final file: 
`TAXONOMIC-VERNACULAR-FR-CURATED-221125.txt`
This file will be used for the french version of Lifemap. 




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



