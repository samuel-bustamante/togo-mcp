# GlyCosmos Exploration Report

## Database Overview
- **Purpose**: Comprehensive glycoscience portal integrating glycan structures, glycoproteins, glycosylation sites, glycogenes, glycoepitopes, and lectin-glycan interactions
- **Scope**: Multi-species glycobiology research and biomarker discovery
- **Key entities**: Saccharide (glycans), Glycoprotein, Glycosylation_Site, Glycogene, Glycan_epitope, Lectin
- **Cross-references**: ChEBI, PubChem, UniProt, NCBI Gene, KEGG, PDB

## Schema Analysis (from MIE file)

### Main Properties Available
- **Saccharide (Glycan)**: glytoucan:has_primary_id (GlyTouCan ID), glycan:has_Resource_entry (external DB)
- **Glycoprotein**: rdfs:label, glycan:has_taxon, glycoconjugate:glycosylated_at
- **Glycosylation_Site**: sio:SIO_000772 (protein reference), faldo:location (position)
- **Glycogene**: rdfs:label (symbol), dcterms:description, glycan:has_taxon, rdfs:seeAlso
- **Glycan_epitope**: rdfs:label, skos:altLabel, glycoepitope:has_antibody, glycoepitope:organism, glycoepitope:tissue

### Important Relationships
- Glycoprotein → Glycosylation_Site via `glycoconjugate:glycosylated_at`
- Glycosylation_Site → Protein via `sio:SIO_000772`
- Glycosylation_Site → Position via `faldo:location/faldo:position`
- External links via `glycan:has_Resource_entry` and `rdfs:seeAlso`

### Key Query Patterns
- Must specify FROM clause with graph URI (100+ graphs)
- Use `bif:contains` for label searches in epitopes
- Filter by taxonomy for species-specific queries
- Always use LIMIT for large datasets (414K+ sites)

## Search Queries Performed

1. **Query: Lewis epitopes**
   - Results: 20 Lewis-related epitopes (Lewis a, Lewis b, Lewis x, Lewis y, Sialyl Lewis variants)
   - EP0007 = Lewis a, EP0011 = Lewis x, EP0012 = Sialyl Lewis x

2. **Query: Total glycan epitopes**
   - Results: 173 epitopes total
   - Manageable dataset for complete enumeration

3. **Query: Glycoproteins by species**
   - Results: Human (9606): 16,604; Mouse (10090): 10,713; Rat (10116): 2,576; Arabidopsis (3702): 2,251
   - Multi-species coverage

4. **Query: Human glycosylation sites with positions**
   - Results: Found sites with specific positions (e.g., HLA class I at position 110, Platelet glycoprotein at 65, 66, 83)
   - P15529 (Membrane cofactor protein) has many sites at position 83

5. **Query: Glycogenes with "transferase" function**
   - Results: FUT1, FUT2, FUT3 (fucosyltransferases), B4GALNT2, A4GALT (galactosyltransferases), ABO blood group gene

## SPARQL Queries Tested

```sparql
# Query 1: Search Lewis epitopes
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?epitope ?label
FROM <http://rdf.glycoinfo.org/glycoepitope>
WHERE {
  ?epitope a glycan:Glycan_epitope ;
    rdfs:label ?label .
  ?label bif:contains "'Lewis'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 20
# Results: 20 Lewis-family epitopes (Lewis a, x, b, y, sialyl variants)
```

```sparql
# Query 2: Count glycoproteins by species
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>

SELECT ?taxon (COUNT(DISTINCT ?protein) as ?count)
FROM <http://rdf.glycosmos.org/glycoprotein>
WHERE {
  ?protein a glycan:Glycoprotein ;
    glycan:has_taxon ?taxon .
}
GROUP BY ?taxon
ORDER BY DESC(?count)
LIMIT 10
# Results: Human 16,604; Mouse 10,713; Rat 2,576
```

```sparql
# Query 3: Human glycosylation sites with positions
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX glycoconjugate: <http://purl.jp/bio/12/glyco/conjugate#>
PREFIX faldo: <http://biohackathon.org/resource/faldo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?protein ?label ?site ?position
FROM <http://rdf.glycosmos.org/glycoprotein>
WHERE {
  ?protein a glycan:Glycoprotein ;
    rdfs:label ?label ;
    glycan:has_taxon <http://identifiers.org/taxonomy/9606> ;
    glycoconjugate:glycosylated_at ?site .
  ?site faldo:location/faldo:position ?position .
}
LIMIT 30
# Results: HLA class I (position 110), Platelet glycoprotein (65, 66, 83), Membrane cofactor protein (83)
```

```sparql
# Query 4: Glycogenes encoding transferases
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?gene ?symbol ?description
FROM <http://rdf.glycosmos.org/glycogenes>
WHERE {
  ?gene a glycan:Glycogene ;
    rdfs:label ?symbol ;
    dcterms:description ?description .
  FILTER(CONTAINS(LCASE(?description), "transferase"))
}
LIMIT 20
# Results: FUT1, FUT2, FUT3 (fucosyltransferases), ABO blood group, galactosyltransferases
```

```sparql
# Query 5: GlyTouCan glycan entries
PREFIX glycan: <http://purl.jp/bio/12/glyco/glycan#>
PREFIX glytoucan: <http://www.glytoucan.org/glyco/owl/glytoucan#>

SELECT (COUNT(DISTINCT ?glycan) as ?total)
FROM <http://rdf.glytoucan.org/core>
WHERE {
  ?glycan glytoucan:has_primary_id ?glycanId .
}
# Results: 117,571 glycan structures
```

## Interesting Findings

### Specific Entities for Questions
- **Lewis a epitope**: EP0007 - well-known blood group antigen
- **Sialyl Lewis x**: EP0012 - important cancer biomarker
- **FUT1/FUT2/FUT3**: Fucosyltransferases involved in blood group synthesis
- **ABO gene**: Blood group determination (alpha-galactosyltransferase)
- **P13224**: Platelet glycoprotein Ib beta chain with glycosylation at positions 65, 66, 83

### Key Statistics
- Glycans: 117,571 structures in GlyTouCan
- Glycoproteins: 153,178 total (16,604 human)
- Glycosylation sites: 414,798 total
- Glycogenes: 423,164 entries
- Glycoepitopes: 173 defined epitopes
- Lectins: 739 entries

### Cross-Database Connections
- Glycans → ChEBI, PubChem, KEGG, PDB
- Glycoproteins → UniProt
- Glycogenes → NCBI Gene, KEGG Genes, HGNC

### Verifiable Facts
- Total glycan epitopes: 173
- Total GlyTouCan glycans: 117,571
- Human glycoproteins: 16,604
- Lewis a epitope ID: EP0007
- FUT3 gene ID: 2525 (Lewis blood group fucosyltransferase)

## Question Opportunities by Category

### Precision
- "What is the GlycoEpitope identifier for Lewis a antigen?" (Answer: EP0007)
- "What is the GlyCosmos glycogene ID for the FUT3 fucosyltransferase?" (Answer: 2525)
- "What position is the glycosylation site on human platelet glycoprotein Ib beta chain (P13224)?" (Answer: 65, 66, 83)

### Completeness
- "How many glycan epitopes are defined in GlycoEpitope?" (Answer: 173)
- "How many glycan structures are in GlyTouCan?" (Answer: ~117,571)
- "How many human glycoproteins are in GlyCosmos?" (Answer: 16,604)
- "List all Lewis family glycan epitopes" (Lewis a, b, x, y, sialyl variants)

### Integration
- "What is the NCBI Gene ID for the FUT1 fucosyltransferase glycogene?" (Answer: 2523)
- "Which UniProt proteins are annotated as glycoproteins in GlyCosmos?"
- "What ChEBI IDs correspond to glycans in GlyTouCan?"

### Currency
- "What recent glycan structures have been added to GlyTouCan?"
- "What new glycosylation sites have been identified for cancer biomarkers?"

### Specificity
- "What is the glycosylation site pattern for HLA class I histocompatibility antigens?"
- "Which glycogenes encode sialyltransferases?"
- "What epitopes contain sulfated Lewis structures?"

### Structured Query
- "Find all human glycoproteins with more than 3 glycosylation sites"
- "List all fucosyltransferase glycogenes (FUT family)"
- "Find glycan epitopes with associated antibodies and tissue annotations"

## Notes

### Limitations
- Glycan labels rarely populated (<1%) - use GlyTouCan IDs
- Multi-graph architecture requires explicit FROM clauses
- 414K+ glycosylation sites require pagination/filtering
- bif:contains only optimized for rdfs:label, not descriptions

### Best Practices
- Always specify FROM clause with appropriate graph
- Use bif:contains for epitope label searches
- Filter by taxonomy for species-specific queries
- Use FILTER(CONTAINS()) for description searches
- Add LIMIT for large result sets

### Important Graphs
- `http://rdf.glytoucan.org/core` - Glycan structures
- `http://rdf.glycosmos.org/glycoprotein` - Glycoproteins and sites
- `http://rdf.glycosmos.org/glycogenes` - Glycogenes
- `http://rdf.glycoinfo.org/glycoepitope` - Glycan epitopes
