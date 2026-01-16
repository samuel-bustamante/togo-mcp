# Exploration Progress

## Session 1 - January 15, 2026

### Completed Databases (6 of 22)
1. amrportal ✅ - AMR Portal (antimicrobial resistance data)
2. bacdive ✅ - Bacterial Diversity Metadatabase  
3. chebi ✅ - Chemical Entities of Biological Interest
4. chembl ✅ - ChEMBL bioactivity database
5. clinvar ✅ - Clinical variant database
6. go ✅ - Gene Ontology

## Session 2 - January 15, 2026

### Completed Databases (10 of 22)
7. ddbj ✅ - DNA Data Bank of Japan (nucleotide sequences)
8. ensembl ✅ - Genome annotations (87K human genes)
9. glycosmos ✅ - Glycoscience portal (117K glycans, 153K glycoproteins)
10. medgen ✅ - Medical genetics (234K clinical concepts)

## Session 3 - January 15, 2026

### Completed Databases (22 of 22)
11. mediadive ✅ - Microbial culture media database
12. mesh ✅ - Medical Subject Headings
13. mondo ✅ - Disease ontology
14. nando ✅ - Japanese rare diseases
15. ncbigene ✅ - NCBI Gene database
16. pdb ✅ - Protein Data Bank
17. pubchem ✅ - Chemical molecules
18. pubmed ✅ - Biomedical literature (37M+ citations)
19. pubtator ✅ - Entity annotations (Disease/Gene from literature)
20. reactome ✅ - Pathway database
21. rhea ✅ - Biochemical reactions
22. taxonomy ✅ - NCBI Taxonomy
23. uniprot ✅ - Protein sequences

### ALL DATABASES EXPLORED ✅

### Notes from Session 3
- PubMed: 37M+ citations with MeSH annotations, author metadata, DOI cross-refs
- PubTator: Disease/Gene annotations from literature via text mining
- Both integrate well via same SPARQL endpoint (different graphs)
- Key tools: ncbi_esearch, get_article_metadata, search_articles, convert_article_ids

### Key Patterns Discovered (All Sessions)
1. FALDO ontology used consistently for genomic coordinates (DDBJ, Ensembl)
2. Cross-references via rdfs:seeAlso are common
3. Species filtering via taxonomy IDs essential for multi-species databases
4. bif:contains works across all Virtuoso-backed databases
5. identifiers.org namespace used for standardized cross-references
6. Web Annotation Ontology (oa:) used in PubTator for annotation modeling
7. OLO (Ordered List Ontology) used in PubMed for author ordering
