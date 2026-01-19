# ClinVar Exploration Report

## Database Overview
- **Purpose**: Aggregates genomic variation and its relationship to human health
- **Key data types**: Variant records, clinical interpretations, gene associations, disease conditions
- **Scale**: 3.59M+ variant records, ~20K genes with cross-references
- **Scope**: Human clinical genetics and variant interpretation

## Schema Analysis (from MIE file)

### Main Entity Types
1. **VariationArchiveType**: Central variant entity
   - Properties: accession (VCV), variation_id, variation_name, variation_type
   - Status: record_status, date_created, date_last_updated
   - Metrics: number_of_submitters

2. **Gene**: Gene entity
   - Properties: gene_id, symbol, full_name, cytogenetic_location
   - Cross-refs: hgnc_id, omim
   - Location: FALDO ontology for coordinates

3. **ClassifiedRecord**: Clinical assertions
   - Contains: germline_classification with description
   - Link to genes via sio:SIO_000628

4. **ClinAsserTraitType**: Disease/phenotype association
   - Properties: type, id
   - Cross-ref via dct:references to MedGen, OMIM, MeSH

### Query Patterns
- Use `bif:contains` on rdfs:label for keyword search
- Access clinical significance via blank node path: classified_record/classifications/germline_classification/description
- Always specify `FROM <http://rdfportal.org/dataset/clinvar>`

## Search Queries Performed

1. **Query**: Total variant count
   - Results: 3,588,969 variants

2. **Query**: Variation types distribution
   - Results: SNV (3.24M), Deletion (161K), Duplication (73K), Microsatellite (36K)

3. **Query**: Clinical significance distribution
   - Results: Uncertain significance (1.82M), Likely benign (993K), Benign (214K), Pathogenic (200K)

4. **Query**: Pathogenic BRCA1 variants
   - Results: Multiple variants including c.2244dup, c.2691_2692insSVAelement, etc.

5. **Query**: Most well-studied variants (>10 submitters)
   - Results: GJB2 c.35del (80 submitters), BRCA1 c.68_69del (78), BRCA1 c.5266dup (78)

6. **Query**: Genes with HGNC and OMIM identifiers
   - Results: Found genes with both cross-references (e.g., SLCO1B1, SLC7A9)

## SPARQL Queries Tested

```sparql
# Query 1: Variation type distribution
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>
SELECT ?variation_type (COUNT(?variant) as ?count)
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?variant a cvo:VariationArchiveType ;
           cvo:variation_type ?variation_type ;
           cvo:record_status "current" .
}
GROUP BY ?variation_type
ORDER BY DESC(?count)
# Results: SNV (3.24M), Deletion (161K), Duplication (73K)
```

```sparql
# Query 2: Clinical significance distribution
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>
SELECT ?significance (COUNT(?variant) as ?count)
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?variant a cvo:VariationArchiveType ;
           cvo:classified_record ?classrec .
  ?classrec cvo:classifications/cvo:germline_classification/cvo:description ?significance .
}
GROUP BY ?significance
ORDER BY DESC(?count)
# Results: VUS (1.82M), Likely benign (993K), Pathogenic (200K)
```

```sparql
# Query 3: BRCA1 pathogenic variants
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>
SELECT ?variant ?label ?type ?significance
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?variant a cvo:VariationArchiveType ;
           rdfs:label ?label ;
           cvo:variation_type ?type ;
           cvo:classified_record ?classrec .
  ?classrec cvo:classifications/cvo:germline_classification/cvo:description ?significance .
  ?label bif:contains "'BRCA1'" .
  FILTER(?significance = "Pathogenic")
}
LIMIT 10
# Results: Multiple BRCA1 pathogenic variants found
```

```sparql
# Query 4: Well-studied variants (multiple submitters)
PREFIX cvo: <http://purl.jp/bio/10/clinvar/>
SELECT ?variant ?label ?last_updated ?num_submitters
FROM <http://rdfportal.org/dataset/clinvar>
WHERE {
  ?variant a cvo:VariationArchiveType ;
           rdfs:label ?label ;
           cvo:number_of_submitters ?num_submitters ;
           cvo:date_last_updated ?last_updated .
  FILTER(?num_submitters >= 10)
}
ORDER BY DESC(?num_submitters)
LIMIT 10
# Results: GJB2:c.35del (80), BRCA1:c.68_69del (78), etc.
```

## Interesting Findings

### Specific Entities for Questions
- **GJB2 c.35del**: 80 submitters, most submissions in ClinVar (variation ID 17004)
- **BRCA1 c.68_69del**: 78 submitters (variation ID 17662)
- **BRCA1 c.5266dup**: 78 submitters (variation ID 17677)
- **CFTR c.1521_1523del (F508del)**: 78 submitters, most common CF variant (variation ID 7105)

### Variant Type Statistics
- Single nucleotide variants: 3,236,823 (90.2%)
- Deletions: 160,620 (4.5%)
- Duplications: 73,448 (2.0%)
- Microsatellites: 36,328 (1.0%)

### Clinical Significance Statistics
- Uncertain significance (VUS): 1,821,577 (50.8%)
- Likely benign: 993,150 (27.7%)
- Benign: 213,802 (6.0%)
- Pathogenic: 200,004 (5.6%)
- Likely pathogenic: 107,204 (3.0%)

### Cross-Database Connections
- MedGen (~95% of disease annotations)
- OMIM (~40% of disease annotations)
- MeSH (~30% of disease annotations)
- HGNC (~100% of human genes)

### Verifiable Facts
- 3,588,969 total variant records
- 3,236,823 single nucleotide variants
- 200,004 pathogenic variants
- GJB2 c.35del has 80 submitters (most in ClinVar)
- CFTR F508del (c.1521_1523del) is one of most submitted variants

## Question Opportunities by Category

### Precision
- "What is the ClinVar accession for the BRCA1 c.5266dup variant?" (Answer: VCV000017677)
- "What is the clinical significance of ClinVar variation VCV000017004?" (Answer: Pathogenic)
- "What is the HGNC ID for the SLCO1B1 gene in ClinVar?" (Answer: HGNC:10959)

### Completeness
- "How many single nucleotide variants are recorded in ClinVar?" (Answer: 3,236,823)
- "How many pathogenic variants are in ClinVar?" (Answer: 200,004)
- "What are all the variation types in ClinVar?" (List of ~20 types)
- "How many variants are classified as 'Uncertain significance'?" (Answer: 1,821,577)

### Integration
- "What MedGen concept is associated with ClinVar variant X?" (via dct:references)
- "What OMIM ID is associated with gene Y in ClinVar?" (via cvo:omim)
- "Link ClinVar genes to HGNC identifiers" (via cvo:hgnc_id)

### Currency
- "When was ClinVar variant VCV000017677 last updated?" (Answer: 2025-05-25)
- "What BRCA1 variants were updated in 2025?"

### Specificity
- "What is the variant with the most submitters in ClinVar?" (Answer: GJB2 c.35del with 80)
- "Find pathogenic BRCA1 frameshift variants"
- "What are the clinical traits associated with CFTR F508del?"

### Structured Query
- "Find pathogenic variants in BRCA1 with more than 5 submitters"
- "List variants classified as 'Likely pathogenic' AND updated in 2025"
- "Find genes with both HGNC AND OMIM cross-references"
- "Find deletion variants associated with 'Hereditary cancer'"

## Notes

### Limitations
- Clinical significance accessed via blank node chains (can be slow)
- Some variants lack disease associations
- Date datatypes mixed (xsd:date and xsd:string)
- Complex disease associations require multiple joins

### Best Practices
- Use `FROM <http://rdfportal.org/dataset/clinvar>` clause
- Use `bif:contains` for gene symbol searches on rdfs:label
- Filter by record_status="current" to exclude deprecated entries
- Use OPTIONAL for blank node chains to avoid filtering out missing data
- Use LIMIT on aggregation queries
- Number of submitters indicates evidence strength

### Clinical Significance Path
```
variant -> cvo:classified_record -> cvo:classifications -> 
          cvo:germline_classification -> cvo:description
```
