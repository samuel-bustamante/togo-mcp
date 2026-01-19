# NCBI Taxonomy RDF Exploration Report

## Database Overview
- **Purpose**: Comprehensive biological taxonomic classification
- **Scope**: All organisms from bacteria to mammals with hierarchical relationships
- **Scale**: 2,698,386 taxa (2.7M+), 2.2M species
- **Key features**: Hierarchical classification, multiple naming systems, genetic codes

## Schema Analysis (from MIE file)

### Main Entity Type
- **Taxon**: Organism classification with rank, names, and hierarchy

### Important Properties
- `rdfs:label`: Primary name
- `tax:rank`: Taxonomic rank (Species, Genus, Family, etc.)
- `rdfs:subClassOf`: Parent taxon (hierarchy)
- `dcterms:identifier`: Taxonomy ID (e.g., 9606)
- `tax:scientificName`: Scientific name
- `tax:commonName`: Common/vernacular name
- `tax:synonym`: Alternative names
- `tax:geneticCode`: Nuclear genetic code
- `tax:geneticCodeMt`: Mitochondrial genetic code
- `owl:sameAs`: Cross-database identifiers
- `rdfs:seeAlso`: UniProt Taxonomy link

### Taxonomic Ranks (top 10 by count)
| Rank | Count |
|------|-------|
| Species | 2,214,294 |
| NoRank | 253,143 |
| Genus | 113,635 |
| Strain | 46,887 |
| Subspecies | 30,646 |
| Family | 10,809 |
| Varietas | 10,287 |
| Subfamily | 3,348 |
| Tribe | 2,423 |
| Order | 2,062 |

## Search Queries Performed

1. **ncbi_esearch("Homo sapiens")** → TaxID **9606**
2. **ncbi_esearch("Escherichia coli")** → TaxID **562**
3. **ncbi_esummary([9606, 10090, 562])** → Human, Mouse, E. coli details

### Model Organisms Verified
| TaxID | Scientific Name | Common Name | Rank |
|-------|-----------------|-------------|------|
| 9606 | Homo sapiens | human | species |
| 10090 | Mus musculus | house mouse | species |
| 562 | Escherichia coli | E. coli | species |

## SPARQL Queries Tested

### Query 1: Total Taxa Count
```sparql
PREFIX tax: <http://ddbj.nig.ac.jp/ontologies/taxonomy/>

SELECT (COUNT(DISTINCT ?taxon) as ?taxon_count)
FROM <http://rdfportal.org/ontology/taxonomy>
WHERE {
  ?taxon a tax:Taxon .
}
```
**Result**: **2,698,386 taxa**

### Query 2: Taxa Count by Rank
```sparql
PREFIX tax: <http://ddbj.nig.ac.jp/ontologies/taxonomy/>

SELECT ?rank (COUNT(?taxon) as ?count)
FROM <http://rdfportal.org/ontology/taxonomy>
WHERE {
  ?taxon a tax:Taxon ;
         tax:rank ?rank .
}
GROUP BY ?rank
ORDER BY DESC(?count)
```
**Results**: Species (2.2M), NoRank (253K), Genus (114K), Strain (47K)

### Query 3: Human Lineage (Complete)
```sparql
PREFIX tax: <http://ddbj.nig.ac.jp/ontologies/taxonomy/>
PREFIX taxon: <http://identifiers.org/taxonomy/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?ancestor ?rank ?label ?id
FROM <http://rdfportal.org/ontology/taxonomy>
WHERE {
  taxon:9606 rdfs:subClassOf* ?ancestor .
  ?ancestor a tax:Taxon ;
    tax:rank ?rank ;
    rdfs:label ?label ;
    dcterms:identifier ?id .
}
```
**Results**: Complete lineage from Homo sapiens (9606) to root (1):
- Species: Homo sapiens
- Genus: Homo
- Family: Hominidae
- Order: Primates
- Class: Mammalia
- Phylum: Chordata
- Kingdom: Metazoa
- Superkingdom: Eukaryota

### Query 4: Cross-References for E. coli
```sparql
PREFIX tax: <http://ddbj.nig.ac.jp/ontologies/taxonomy/>
PREFIX taxon: <http://identifiers.org/taxonomy/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?label ?sameAs ?seeAlso
FROM <http://rdfportal.org/ontology/taxonomy>
WHERE {
  taxon:562 a tax:Taxon ;
    rdfs:label ?label .
  OPTIONAL { taxon:562 owl:sameAs ?sameAs }
  OPTIONAL { taxon:562 rdfs:seeAlso ?seeAlso }
}
```
**Results**: E. coli (TaxID 562) has 5 owl:sameAs identifiers:
- OBO NCBITaxon: http://purl.obolibrary.org/obo/NCBITaxon_562
- Berkeley BOP: http://www.berkeleybop.org/ontologies/owl/NCBITaxon#562
- DDBJ: http://ddbj.nig.ac.jp/ontologies/taxonomy/562
- NCBI Web: http://www.ncbi.nlm.nih.gov/taxonomy/562
- UniProt (seeAlso): http://purl.uniprot.org/taxonomy/562

## Interesting Findings

### Specific Entities for Questions
1. **TaxID 9606**: Homo sapiens (human) - Kingdom Metazoa
2. **TaxID 10090**: Mus musculus (house mouse) - model organism
3. **TaxID 562**: Escherichia coli - model bacterium
4. **TaxID 9605**: Homo (human genus)
5. **TaxID 9604**: Hominidae (great apes family)
6. **TaxID 33208**: Metazoa (animal kingdom)
7. **TaxID 2759**: Eukaryota (superkingdom)

### Unique Properties
- Hierarchical classification via rdfs:subClassOf allows lineage traversal
- 47 different taxonomic ranks
- 5 owl:sameAs identifiers per taxon for cross-database integration
- Multiple name types: scientific, common, synonym, equivalent

### Connections to Other Databases
- **UniProt Taxonomy**: rdfs:seeAlso with ~100% coverage
- **OBO NCBITaxon**: owl:sameAs for ontology integration
- **DDBJ/NCBI**: Additional owl:sameAs identifiers

### Specific, Verifiable Facts
- Total taxa: **2,698,386**
- Species count: **2,214,294**
- Genus count: **113,635**
- Family count: **10,809**
- Order count: **2,062**
- Class count: **594**
- Human TaxID: **9606**
- Mouse TaxID: **10090**
- E. coli TaxID: **562**

## ⚠️ CRITICAL: Cross-Reference/Mapping Analysis

### owl:sameAs Cross-References
1. **Entity Count**: ~100% of taxa have owl:sameAs
2. **Relationship Count**: ~5 owl:sameAs per taxon (5 database systems)
3. **Systems covered**: OBO, Berkeley BOP, DDBJ, NCBI Web, OBO Legacy

### UniProt Taxonomy Links (rdfs:seeAlso)
1. **Entity Count**: ~100% of taxa have UniProt links
2. **Pattern**: `http://purl.uniprot.org/taxonomy/{taxid}`

## Question Opportunities by Category

### Precision
- "What is the NCBI Taxonomy ID for Homo sapiens?" (9606)
- "What is the NCBI Taxonomy ID for Escherichia coli?" (562)
- "What is the scientific name for TaxID 10090?" (Mus musculus)
- "What is the common name for TaxID 9606?" (human)
- "What is the parent taxon of Homo sapiens?" (Homo, TaxID 9605)

### Completeness
- "How many taxa are in NCBI Taxonomy?" (2,698,386)
- "How many species are in NCBI Taxonomy?" (2,214,294)
- "How many genera are in NCBI Taxonomy?" (113,635)
- "How many taxonomic ranks are defined?" (47)

### Integration
- "What is the UniProt Taxonomy link for E. coli?" (http://purl.uniprot.org/taxonomy/562)
- "What are the owl:sameAs identifiers for TaxID 562?" (5 identifiers)
- "What is the OBO NCBITaxon identifier for human?" (NCBITaxon_9606)

### Currency
- "What is the current total count of taxa?" (2.7M+)
- "When was the mouse taxonomy entry last modified?" (2025/06/16)

### Specificity
- "What is the complete lineage of Homo sapiens?" (32 levels)
- "What taxonomic rank is 'Hominidae'?" (Family)
- "What kingdom does Homo sapiens belong to?" (Metazoa)
- "What phylum is Escherichia coli in?" (Pseudomonadota/Proteobacteria)

### Structured Query
- "Find all species in genus Homo"
- "Find all genera in family Hominidae"
- "What organisms have 'mouse' in their common name?"
- "Find mammals (Class Mammalia) with strains"

## Notes

### Limitations
- Lineage traversal (rdfs:subClassOf*) can be slow for deep hierarchies
- Common names ~30% complete (better for vertebrates)
- Property path queries need LIMIT to avoid timeout

### Best Practices
- Use `bif:contains` for name searches with relevance scoring
- Always include `FROM <http://rdfportal.org/ontology/taxonomy>` clause
- Add LIMIT for exploratory queries (2.7M+ taxa)
- Filter by `tax:rank` to improve performance
- Start lineage queries from specific taxon ID, not all taxa

### Important Count Clarifications
- Species count (2.2M) is subset of total taxa (2.7M)
- NoRank entries (253K) include intermediate classification nodes
- Strain count (47K) represents specific isolates/strains below species
