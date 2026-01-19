# Ensembl Exploration Report

## Database Overview
- **Purpose**: Comprehensive genomics database providing genome annotations for 100+ species
- **Scope**: Contains genes, transcripts, proteins, and exons with genomic locations
- **Key entities**: EnsemblGene, EnsemblTranscript, EnsemblProtein, EnsemblExon, OrderedExon
- **Cross-references**: UniProt, HGNC, NCBI Gene, Reactome, OMIM

## Schema Analysis (from MIE file)

### Main Properties Available
- **EnsemblGene**: rdfs:label (symbol), dcterms:identifier (ENSG ID), dcterms:description, terms:has_biotype, so:part_of (chromosome), faldo:location
- **EnsemblTranscript**: dcterms:identifier (ENST ID), terms:has_biotype, terms:has_transcript_flag, so:transcribed_from (gene), so:translates_to (protein)
- **EnsemblProtein**: dcterms:identifier (ENSP ID), so:translation_of, rdfs:seeAlso (UniProt)
- **EnsemblExon**: dcterms:identifier (ENSE ID), faldo:location

### Important Relationships
- Gene → Transcript via `so:transcribed_from` (inverse relationship)
- Transcript → Protein via `so:translates_to`
- Protein → UniProt via `rdfs:seeAlso`
- Gene → Chromosome via `so:part_of`
- Gene → Species via `obo:RO_0002162` (in taxon)
- Gene → HGNC via `rdfs:seeAlso`

### Key Query Patterns
- Use `bif:contains` with wildcards (e.g., "'BRCA*'") for gene symbol searches
- Always filter by species (taxonomy ID) to avoid mixed results
- Use FALDO for genomic coordinates
- Strand is encoded in position type (ForwardStrandPosition/ReverseStrandPosition)

## Search Queries Performed

1. **Query: BRCA genes with wildcard search**
   - Results: Found BRCA1 (ENSG00000012048), BRCA2 (ENSG00000139618), BRCA1P1 pseudogene
   - bif:contains with wildcards works well

2. **Query: BRCA1 genomic coordinates**
   - Results: Chromosome 17, position 43044295-43170245, reverse strand
   - FALDO coordinates properly retrieved

3. **Query: BRCA1 transcripts and proteins**
   - Results: 20+ transcripts (ENST00000352993, ENST00000357654, etc.) with UniProt links (P38398)
   - Multiple isoforms and UniProt IDs per gene

4. **Query: Kinase receptor genes by description**
   - Results: ROR1, ROR2 (receptor tyrosine kinases), RIPK3, IRAK genes, DDR2, AXL
   - Boolean AND search in descriptions works

5. **Query: Species gene counts**
   - Results: Mouse (10090): 744,820; Sheep (9940): 633,869; Pig (9823): 624,705; Human (9606): 87,688
   - Multi-species database with good coverage

## SPARQL Queries Tested

```sparql
# Query 1: Search genes by symbol with wildcard
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT ?gene ?id ?label ?description
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        dcterms:identifier ?id ;
        rdfs:label ?label ;
        dcterms:description ?description ;
        obo:RO_0002162 taxonomy:9606 .
  ?label bif:contains "'BRCA*'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 10
# Results: BRCA1, BRCA2, BRCA1P1 with scores
```

```sparql
# Query 2: Gene genomic coordinates with FALDO
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX faldo: <http://biohackathon.org/resource/faldo#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX so: <http://purl.obolibrary.org/obo/so#>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT DISTINCT ?gene ?id ?label ?start ?end ?strand ?chr
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        dcterms:identifier ?id ;
        rdfs:label ?label ;
        faldo:location ?loc ;
        so:part_of ?chr ;
        obo:RO_0002162 taxonomy:9606 .
  ?loc faldo:begin/faldo:position ?start ;
       faldo:end/faldo:position ?end ;
       faldo:begin/rdf:type ?strand_type .
  BIND(IF(?strand_type = faldo:ForwardStrandPosition, "+", "-") AS ?strand)
  FILTER(?id = "ENSG00000012048")
}
# Results: BRCA1 on chr17:43044295-43170245, reverse strand
```

```sparql
# Query 3: Gene-Transcript-Protein-UniProt mapping
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX so: <http://purl.obolibrary.org/obo/so#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX taxonomy: <http://identifiers.org/taxonomy/>

SELECT ?gene_id ?gene_label ?transcript_id ?protein_id ?uniprot
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        dcterms:identifier ?gene_id ;
        rdfs:label ?gene_label ;
        obo:RO_0002162 taxonomy:9606 .
  ?transcript so:transcribed_from ?gene ;
              dcterms:identifier ?transcript_id ;
              so:translates_to ?protein .
  ?protein dcterms:identifier ?protein_id ;
           rdfs:seeAlso ?uniprot .
  FILTER(STRSTARTS(STR(?uniprot), "http://purl.uniprot.org/uniprot/"))
  FILTER(?gene_label = "BRCA1")
}
LIMIT 20
# Results: 20+ BRCA1 transcripts with UniProt mappings (P38398, H0Y850, etc.)
```

```sparql
# Query 4: Ordered exons for a transcript
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX faldo: <http://biohackathon.org/resource/faldo#>

SELECT ?transcript_id ?exon_id ?order ?start ?end
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?transcript a terms:EnsemblTranscript ;
              dcterms:identifier ?transcript_id ;
              sio:SIO_000974 ?ordered_exon .
  ?ordered_exon sio:SIO_000628 ?exon ;
                sio:SIO_000300 ?order .
  ?exon dcterms:identifier ?exon_id ;
        faldo:location/faldo:begin/faldo:position ?start ;
        faldo:location/faldo:end/faldo:position ?end .
  FILTER(?transcript_id = "ENST00000357654")
}
ORDER BY ?order
LIMIT 25
# Results: 23 exons in order with coordinates for BRCA1 canonical transcript
```

```sparql
# Query 5: Species gene distribution
PREFIX terms: <http://rdf.ebi.ac.uk/terms/ensembl/>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT ?taxonomy (COUNT(?gene) as ?gene_count)
FROM <http://rdfportal.org/dataset/ensembl>
WHERE {
  ?gene a terms:EnsemblGene ;
        obo:RO_0002162 ?taxonomy .
}
GROUP BY ?taxonomy
ORDER BY DESC(?gene_count)
LIMIT 20
# Results: Mouse 744K, Sheep 634K, Pig 625K, Human 87K genes
```

## Interesting Findings

### Specific Entities for Questions
- **BRCA1 gene**: ENSG00000012048, chr17:43044295-43170245, reverse strand
- **BRCA1 canonical transcript**: ENST00000357654 with 23 exons
- **BRCA1 protein**: ENSP00000350283 linked to UniProt P38398
- **HGNC cross-reference**: HGNC:1100 for BRCA1
- **Receptor kinases**: ROR1 (ENSG00000185483), ROR2 (ENSG00000169071)

### Cross-Database Connections
- Ensembl → UniProt (via rdfs:seeAlso on proteins): P38398 for BRCA1
- Ensembl → HGNC (via rdfs:seeAlso on genes): HGNC:1100
- Ensembl → NCBI Gene via TogoID: ENSG00000012048 → 672 (BRCA1)

### Key Statistics
- Human genes: 87,688
- Mouse genes: 744,820
- Total genes: ~3,000,000
- Total transcripts: ~4,000,000
- Total proteins: ~2,000,000
- 100+ vertebrate species

### Verifiable Facts
- ENSG00000012048 encodes BRCA1 at chr17:43044295-43170245 (reverse strand)
- ENST00000357654 (BRCA1 canonical) has 23 exons
- BRCA1 maps to UniProt P38398 and HGNC:1100
- Human genome has 87,688 genes in Ensembl

## Question Opportunities by Category

### Precision
- "What is the Ensembl gene ID for human BRCA1?" (Answer: ENSG00000012048)
- "What chromosome is BRCA1 located on in the GRCh38 assembly?" (Answer: chromosome 17)
- "What is the genomic position of BRCA1 in GRCh38?" (Answer: 43044295-43170245)
- "What strand is BRCA1 located on?" (Answer: reverse/minus strand)

### Completeness
- "How many exons does the BRCA1 canonical transcript ENST00000357654 have?" (Answer: 23)
- "How many human genes are annotated in Ensembl?" (Answer: 87,688)
- "How many transcripts encode proteins for BRCA1?" (List of ENST IDs)
- "How many species are represented in Ensembl?" (100+)

### Integration
- "What is the NCBI Gene ID corresponding to Ensembl gene ENSG00000012048?" (Answer: 672)
- "What UniProt ID is linked to Ensembl protein ENSP00000350283?" (Answer: P38398)
- "What is the HGNC ID for BRCA1?" (Answer: HGNC:1100)
- "Convert Ensembl gene ENSG00000139618 to NCBI Gene ID" (BRCA2)

### Currency
- "What are the latest receptor tyrosine kinase genes annotated in Ensembl for humans?"
- "What biotypes are assigned to non-coding RNA genes?"
- "What transcript quality flags (MANE Select, APPRIS) are available for BRCA1?"

### Specificity
- "What is the Ensembl gene ID for the receptor tyrosine kinase ROR1?" (Answer: ENSG00000185483)
- "What is the first exon ID of BRCA1 transcript ENST00000357654?" (Answer: ENSE00001852567)
- "What microRNA genes are annotated in Ensembl?" (MIR6723 = ENSG00000266085)

### Structured Query
- "Find all human kinase receptor genes with description containing both 'kinase' and 'receptor'"
- "List all protein-coding genes on human chromosome X"
- "Find all exons of transcript ENST00000357654 with coordinates between 43050000 and 43100000"

## Notes

### Limitations
- Not all transcripts encode proteins (non-coding RNAs exist)
- Transcript quality varies (check MANE, APPRIS, TSL flags)
- FALDO positions may have duplicate entries (use DISTINCT)
- Query timeout risk on broad species-wide queries without filters

### Best Practices
- Always filter by species taxonomy ID (9606 for human, 10090 for mouse)
- Use bif:contains for text searches with wildcards
- Use DISTINCT with FALDO location queries
- Check biotype before expecting protein products
- Use OPTIONAL for so:translates_to (some transcripts don't encode proteins)

### Cross-Reference Patterns
- UniProt: `http://purl.uniprot.org/uniprot/`
- HGNC: `http://identifiers.org/hgnc/`
- Taxonomy: `http://identifiers.org/taxonomy/`
