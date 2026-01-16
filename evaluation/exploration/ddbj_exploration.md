# DDBJ (DNA Data Bank of Japan) Exploration Report

## Database Overview
- **Purpose**: DDBJ RDF provides nucleotide sequence data from the International Nucleotide Sequence Database Collaboration (INSDC)
- **Scope**: Contains genomic entries with annotations (genes, CDS, tRNA, rRNA) linked to organism metadata, taxonomic classification, and protein translations
- **Key data types**: Entries (sequence records), Genes, Coding Sequences (CDS), tRNA, rRNA, Source annotations
- **Cross-references**: BioProject, BioSample, NCBI Protein, NCBI Taxonomy

## Schema Analysis (from MIE file)

### Main Properties Available
- **Entry**: rdfs:label, dcterms:identifier, nuc:definition, nuc:organism, nuc:taxonomy, nuc:division, nuc:sequence, nuc:dblink, nuc:reference
- **Gene**: nuc:locus_tag, nuc:gene (symbol), faldo:location (genomic coordinates)
- **Coding Sequence (CDS)**: nuc:locus_tag, nuc:product, nuc:translation, nuc:codon_start, nuc:transl_table, rdfs:seeAlso (protein link)
- **tRNA/rRNA**: nuc:product, faldo:location

### Important Relationships
- Gene-CDS linked via `sio:SIO_010081` (case-sensitive!)
- Taxonomic links via `ro:0002162` (in taxon)
- External links via `rdfs:seeAlso` (NCBI Protein)
- Project links via `nuc:dblink` (BioProject, BioSample)

### Key Query Patterns
- Use `bif:contains` for organism search at entry level
- Always filter by entry ID (FILTER CONTAINS) before complex queries
- Use FALDO for genomic coordinates

## Search Queries Performed

1. **Query: E. coli entries with bif:contains**
   - Results: Found entries like AP026093.1, AP026094.1, AP026095.1 for Escherichia coli
   - Works well with relevance scoring

2. **Query: Streptococcus pyogenes entries**
   - Results: Found CP035433.1, CP035439.1 (complete genomes) and various gene-specific entries (AB002521.1, AB006751.1)
   - Good for pathogen research

3. **Query: Genes in entry CP036276.1**
   - Results: Found locus tags like Mal52_08030 (clpX), Mal52_08090 (afsK_1), Mal52_08160 (blaI_6) with coordinates
   - Symmachiella dynata complete genome

4. **Query: Protease/peptidase genes in CP036276.1**
   - Results: Found 50 protease/peptidase genes including ATP-dependent Clp protease, Lon protease, various peptidases
   - Good filter capabilities

5. **Query: RNA features (tRNA, rRNA)**
   - Results: Found tRNA-Ile, tRNA-Ala, tRNA-Gly, etc.
   - UNION query works for multiple feature types

## SPARQL Queries Tested

```sparql
# Query 1: Search entries by organism name
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>

SELECT ?entry ?organism ?relevance
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?entry a nuc:Entry ;
         nuc:organism ?organism .
  ?organism bif:contains "'escherichia' AND 'coli'" option (score ?relevance) .
}
ORDER BY DESC(?relevance)
LIMIT 10
# Results: 10 E. coli entries with relevance scores
```

```sparql
# Query 2: Gene annotations by locus tag
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>

SELECT ?gene ?gene_symbol ?product
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?gene a nuc:Gene ;
        nuc:locus_tag "Mal52_08030" .
  OPTIONAL { ?gene nuc:gene ?gene_symbol }
  OPTIONAL {
    ?cds nuc:locus_tag "Mal52_08030" ;
         nuc:product ?product .
  }
}
# Results: clpX gene encoding ATP-dependent Clp protease ATP-binding subunit ClpX
```

```sparql
# Query 3: Gene coordinates with FALDO
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>
PREFIX faldo: <http://biohackathon.org/resource/faldo#>

SELECT ?locus_tag ?gene_symbol ?start ?end
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?gene a nuc:Gene ;
        nuc:locus_tag ?locus_tag ;
        faldo:location ?region .
  ?region faldo:begin/faldo:position ?start ;
          faldo:end/faldo:position ?end .
  OPTIONAL { ?gene nuc:gene ?gene_symbol }
  FILTER(CONTAINS(STR(?gene), "CP036276.1"))
}
LIMIT 15
# Results: 15 genes with coordinates (e.g., clpX at 1001623-1002915)
```

```sparql
# Query 4: Gene-CDS-Protein integration
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>
PREFIX sio: <http://semanticscience.org/resource/>

SELECT ?locus_tag ?product ?protein_id
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?gene a nuc:Gene ;
        nuc:locus_tag ?locus_tag .
  ?cds sio:SIO_010081 ?gene ;
       nuc:product ?product ;
       rdfs:seeAlso ?protein_id .
  FILTER(CONTAINS(STR(?protein_id), "ncbiprotein"))
  FILTER(CONTAINS(STR(?gene), "CP036276.1"))
}
LIMIT 20
# Results: 20 genes linked to NCBI Protein IDs (e.g., Mal52_08030 → QDU42347.1)
```

```sparql
# Query 5: BioProject/BioSample links
PREFIX nuc: <http://ddbj.nig.ac.jp/ontologies/nucleotide/>

SELECT ?entry ?bioproject ?biosample
FROM <http://rdfportal.org/dataset/ddbj>
WHERE {
  ?entry a nuc:Entry ;
         nuc:dblink ?bioproject ;
         nuc:dblink ?biosample .
  FILTER(CONTAINS(STR(?bioproject), "bioproject"))
  FILTER(CONTAINS(STR(?biosample), "biosample"))
}
LIMIT 10
# Results: Entries linked to BioProject (e.g., PRJNA485700) and BioSample (e.g., SAMN10954015)
```

## Interesting Findings

### Specific Entities for Questions
- **Entry CP036276.1**: Symmachiella dynata complete genome with rich annotations
- **Locus tag Mal52_08030**: clpX gene with protein link QDU42347.1
- **Entry CP035433.1**: Streptococcus pyogenes strain emm65 complete genome
- **Specific products**: ATP-dependent Clp protease, Lon protease, BlaR1 peptidase

### Unique Properties
- Comprehensive genomic coordinates via FALDO
- Direct gene-CDS-protein linkage through sio:SIO_010081
- Cross-references to BioProject and BioSample for experimental context
- Supports bif:contains for fast organism search

### Cross-Database Connections
- DDBJ → NCBI Protein (via rdfs:seeAlso on CDS)
- DDBJ → BioProject/BioSample (via nuc:dblink)
- DDBJ → NCBI Taxonomy (via ro:0002162)

### Verifiable Facts
- Entry CP036276.1 contains genes from Symmachiella dynata
- Locus tag "Mal52_08030" encodes clpX gene (ATP-dependent Clp protease)
- Protein QDU42347.1 is linked to locus Mal52_08030
- Entry CP036276.1 is linked to BioProject PRJNA485700 and BioSample SAMN10954015

## Question Opportunities by Category

### Precision
- "What is the NCBI Protein ID linked to locus tag Mal52_08030 in DDBJ?" (Answer: QDU42347.1)
- "What gene symbol is associated with locus tag Mal52_08030?" (Answer: clpX)
- "What is the genomic position range for the clpX gene in entry CP036276.1?" (Answer: 1001623-1002915)

### Completeness
- "How many protease/peptidase genes are annotated in genome entry CP036276.1?"
- "List all tRNA genes in a specific bacterial genome"
- "How many genes have associated NCBI Protein IDs in entry X?"

### Integration
- "What BioProject ID is associated with DDBJ entry CP036276.1?" (Answer: PRJNA485700)
- "Convert DDBJ locus tag to NCBI Protein ID"
- "What BioSample is linked to entry CP036276.1?" (Answer: SAMN10954015)

### Currency
- "What are the most recent E. coli genome entries in DDBJ?"
- "What Streptococcus pyogenes genomes are available?"

### Specificity
- "What organism is represented by DDBJ entry CP036276.1?" (Answer: Symmachiella dynata)
- "What is the definition of entry AB002521.1?" (16S rRNA from Streptococcus pyogenes)
- "What regulatory proteins are encoded in Streptococcus pyogenes genomes?"

### Structured Query
- "Find all genes in CP036276.1 that encode proteases and have NCBI Protein links"
- "Find genes within genomic position range 1000000-1050000 in entry CP036276.1"
- "List genes with both gene symbols and protein products in a specific entry"

## Notes

### Limitations
- Mostly prokaryotic data (bacteria, archaea)
- Complex queries require entry ID filtering to avoid timeout
- ~60% genes have gene symbols, but >99% have locus tags (use locus tags for reliability)
- Aggregation queries (COUNT) without filtering cause timeout

### Best Practices
- Always filter by entry ID before complex joins or FALDO queries
- Use bif:contains for organism search (fast, relevance-scored)
- Use sio:SIO_010081 (uppercase!) for Gene-CDS relationships
- Must include FROM clause with graph URI

### Performance Notes
- Entry-specific queries are fast
- Product searches require entry filtering
- Avoid Cartesian products from unfiltered joins
