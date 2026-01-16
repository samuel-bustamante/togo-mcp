# NCBI Gene Database Exploration Report

## Database Overview
- **Purpose**: Comprehensive gene database covering all organisms
- **Scope**: 57M+ gene entries including protein-coding, ncRNA, tRNA, pseudogenes
- **Key data types**: Gene symbols, descriptions, chromosomal locations, gene types, cross-references, orthology

## Schema Analysis (from MIE file)

### Main Entity Type
- **insdc:Gene** - Gene entity with comprehensive properties

### Key Properties
- `rdfs:label` - Gene symbol (INS, BRCA1, TP53)
- `dct:description` - Full gene name (insulin, tumor protein p53)
- `dct:identifier` - NCBI Gene ID (integer)
- `ncbio:typeOfGene` - Gene type (protein-coding, ncRNA, pseudo, etc.)
- `ncbio:taxid` - Taxonomic classification (identifiers.org/taxonomy/ID)
- `insdc:chromosome` - Chromosome location
- `insdc:map` - Cytogenetic map location (e.g., "11p15.5")
- `insdc:gene_synonym` - Alternative names
- `insdc:dblink` - External database links (IRI)
- `orth:hasOrtholog` - Orthologous genes in other species

## Search Queries Performed

1. **Gene ID 1 (A1BG)** → alpha-1-B glycoprotein, protein-coding, chr19, 19q13.43

2. **Insulin gene (3630)** → INS, protein-coding, chr11, 11p15.5

3. **BRCA1 (672)** → BRCA1 DNA repair associated, protein-coding, chr17, 17q21.31

4. **TP53 (7157)** → tumor protein p53, protein-coding, chr17, 17p13.1

5. **Human gene type distribution** → biological-region (128K), ncRNA (22K), protein-coding (20.5K), pseudo (17K)

## SPARQL Queries Tested

```sparql
# Query 1: Basic gene info retrieval
PREFIX ncbio: <https://dbcls.github.io/ncbigene-rdf/ontology.ttl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?label ?description ?type ?chromosome ?map
FROM <http://rdfportal.org/dataset/ncbigene>
WHERE {
  <http://identifiers.org/ncbigene/672> rdfs:label ?label ;
    ncbio:typeOfGene ?type .
  OPTIONAL { <http://identifiers.org/ncbigene/672> dct:description ?description }
  OPTIONAL { <http://identifiers.org/ncbigene/672> insdc:chromosome ?chromosome }
  OPTIONAL { <http://identifiers.org/ncbigene/672> insdc:map ?map }
}
# Results: BRCA1, "BRCA1 DNA repair associated", protein-coding, 17, 17q21.31
```

```sparql
# Query 2: Gene type distribution for human
PREFIX ncbio: <https://dbcls.github.io/ncbigene-rdf/ontology.ttl#>

SELECT ?type (COUNT(?gene) as ?count)
FROM <http://rdfportal.org/dataset/ncbigene>
WHERE {
  ?gene ncbio:typeOfGene ?type ;
        ncbio:taxid <http://identifiers.org/taxonomy/9606> .
}
GROUP BY ?type
ORDER BY DESC(?count)
# Results: biological-region (128,261), ncRNA (22,103), protein-coding (20,595), etc.
```

```sparql
# Query 3: Search insulin-related genes
PREFIX ncbio: <https://dbcls.github.io/ncbigene-rdf/ontology.ttl#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?gene ?label ?description ?sc
FROM <http://rdfportal.org/dataset/ncbigene>
WHERE {
  ?gene a insdc:Gene ;
        rdfs:label ?label ;
        dct:description ?description ;
        ncbio:taxid <http://identifiers.org/taxonomy/9606> .
  ?description bif:contains "'insulin'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 20
# Results: INS, INSR, IGF1, IGF2, IGFBPs, IRS1, etc.
```

```sparql
# Query 4: Find INS orthologs across species
PREFIX orth: <http://purl.org/net/orth#>
PREFIX ncbio: <https://dbcls.github.io/ncbigene-rdf/ontology.ttl#>

SELECT ?ortholog ?label ?taxid
FROM <http://rdfportal.org/dataset/ncbigene>
WHERE {
  <http://identifiers.org/ncbigene/3630> orth:hasOrtholog ?ortholog .
  ?ortholog rdfs:label ?label ;
            ncbio:taxid ?taxid .
}
LIMIT 20
# Results: Found orthologs in mouse (Ins2), rat (Ins2), cattle (INS), pig (INS), etc.
```

## Interesting Findings

### Specific Verifiable Facts
- Gene ID 1 = A1BG (alpha-1-B glycoprotein), chromosome 19q13.43
- Gene ID 3630 = INS (insulin), chromosome 11p15.5
- Gene ID 672 = BRCA1, chromosome 17q21.31
- Gene ID 7157 = TP53, chromosome 17p13.1
- Human has 20,595 protein-coding genes

### Gene Type Distribution (Human)
1. biological-region: 128,261
2. ncRNA: 22,103
3. protein-coding: 20,595
4. pseudo: 17,483
5. snoRNA: 1,201

### Cross-Database Links
- BRCA1 (672) links to:
  - OMIM: 113705
  - Ensembl: ENSG00000012048
  - HGNC: 1100

### Orthology
- INS has orthologs across mammals (mouse, rat, cattle, pig, dog, cat)
- Mouse uses "Ins2" symbol, while most other mammals use "INS"

## Question Opportunities by Category

### Precision Questions
- What is the NCBI Gene ID for human insulin (INS)?
- What chromosome is BRCA1 located on?
- What is the cytogenetic location of TP53?
- What is the gene type of NCBI Gene ID 7157?

### Completeness Questions
- How many protein-coding genes does human have in NCBI Gene?
- How many ncRNA genes are annotated for human?
- How many orthologs does the human INS gene have?

### Integration Questions
- What is the Ensembl ID for BRCA1 (NCBI Gene 672)?
- What OMIM ID is linked to BRCA1?
- What is the HGNC ID for gene 672?

### Specificity Questions
- Find all insulin-related genes in human
- What genes are located on chromosome 17q21?
- Find tumor suppressor genes in human

### Structured Query Questions
- List all orthologs of human insulin gene
- Find all protein-coding genes on chromosome 19
- Get genes with both Ensembl and HGNC cross-references

## Cross-Reference Mapping Analysis

### External Database Links (insdc:dblink)
- Links via identifiers.org URIs
- Common targets: Ensembl, HGNC, OMIM
- Format: http://identifiers.org/{database}/{id}

### Orthology (orth:hasOrtholog)
- Bidirectional orthology relationships
- ~40% of genes have orthologs
- Average ~150 orthologs per gene

## Notes
- Use `bif:contains` for text search on descriptions
- Always filter by `ncbio:taxid` for organism-specific queries (essential for 57M+ genes!)
- Label = gene symbol (INS), description = full name (insulin)
- Use `ncbi_esearch` for initial discovery, then SPARQL for detailed data
- Human taxonomy ID: 9606 (`http://identifiers.org/taxonomy/9606`)
- Gene IDs are integers, use full URI: `<http://identifiers.org/ncbigene/ID>`
- Always include `FROM <http://rdfportal.org/dataset/ncbigene>` clause
