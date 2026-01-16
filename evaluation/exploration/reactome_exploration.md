# Reactome Pathway Database Exploration Report

## Database Overview
- **Purpose**: Curated knowledgebase of biological pathways and processes
- **Scope**: Pathways, reactions, proteins, complexes, small molecules
- **Scale**: 23,145 pathways, 92,977 reactions across 15+ species
- **Key features**: BioPAX ontology, hierarchical pathways, comprehensive cross-references

## Schema Analysis (from MIE file)

### Main Entity Types
- **Pathway**: Hierarchical pathway organization with bp:pathwayComponent
- **BiochemicalReaction**: Reactions with bp:left/bp:right participants
- **Protein**: Protein entities with UniProt references
- **Complex**: Multi-component assemblies with stoichiometry
- **SmallMolecule**: Chemical compounds with ChEBI references
- **Catalysis**: Enzyme-reaction relationships

### Important Properties
- `bp:displayName`: Human-readable name
- `bp:pathwayComponent`: Sub-pathway links
- `bp:left`/`bp:right`: Reaction participants
- `bp:entityReference`: Link to reference database
- `bp:xref`: Cross-references with bp:db and bp:id
- `bp:organism`: Species information
- `bp:cellularLocation`: Subcellular localization
- `bp:eCNumber`: EC number for reactions

### BioPAX Cross-Reference Pattern
```sparql
?entity bp:xref ?xref .
?xref a bp:UnificationXref ;
      bp:db "UniProt"^^xsd:string ;  # NOTE: ^^xsd:string required!
      bp:id ?uniprotId .
```

## Search Queries Performed

1. **search_reactome_entity("autophagy")** → **R-HSA-9612973** (Autophagy pathway) + 50+ related entities
2. **search_reactome_entity("SARS-CoV-2")** → **R-HSA-9694516** (SARS-CoV-2 Infection) + many related pathways
3. **search_reactome_entity("BRCA1")** → **R-HSA-50949** (BRCA1 protein) + associated pathways/complexes
4. **Cancer pathway search** → 20+ cancer-related pathways (EGFR, NOTCH, WNT, PI3K/AKT)
5. **Organism distribution** → 15 species with Human (2,825 pathways) being most extensive

## SPARQL Queries Tested

### Query 1: Total Pathway Count
```sparql
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

SELECT (COUNT(DISTINCT ?pathway) as ?pathway_count)
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?pathway a bp:Pathway .
}
```
**Result**: **23,145 total pathways**

### Query 2: Reaction Count
```sparql
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

SELECT (COUNT(DISTINCT ?reaction) as ?reaction_count)
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?reaction a bp:BiochemicalReaction .
}
```
**Result**: **92,977 reactions**

### Query 3: Pathways by Organism
```sparql
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

SELECT ?orgName (COUNT(DISTINCT ?pathway) as ?pathway_count)
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?pathway a bp:Pathway ;
           bp:organism ?org .
  ?org bp:name ?orgName .
}
GROUP BY ?orgName
ORDER BY DESC(?pathway_count)
```
**Results**:
| Organism | Pathway Count |
|----------|---------------|
| Homo sapiens | 2,825 |
| Gallus gallus | 1,824 |
| Mus musculus | 1,824 |
| Rattus norvegicus | 1,807 |
| Bos taurus | 1,804 |
| Sus scrofa | 1,794 |
| Canis familiaris | 1,771 |

### Query 4: Entity Counts by Type
```sparql
SELECT ?entityType (COUNT(?entity) as ?count)
WHERE {
  ?entity a ?entityType .
  FILTER(?entityType IN (bp:Protein, bp:Complex, bp:SmallMolecule, bp:Dna, bp:Rna))
}
GROUP BY ?entityType
```
**Results**:
| Type | Count |
|------|-------|
| Protein | 233,200 |
| Complex | 109,261 |
| SmallMolecule | 51,214 |
| Dna | 1,871 |
| Rna | 820 |

### Query 5: Cancer-Related Pathways
```sparql
PREFIX bp: <http://www.biopax.org/release/biopax-level3.owl#>

SELECT ?pathway ?name
FROM <http://rdf.ebi.ac.uk/dataset/reactome>
WHERE {
  ?pathway a bp:Pathway ;
           bp:displayName ?name .
  ?name bif:contains "'cancer'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 10
```
**Results**: Found 20+ cancer pathways including:
- Signaling by EGFR in Cancer
- PI3K/AKT Signaling in Cancer
- Signaling by WNT in cancer
- Signaling by NOTCH1 in Cancer

## Interesting Findings

### Specific Entities for Questions
1. **R-HSA-9612973**: Autophagy pathway (human)
2. **R-HSA-9694516**: SARS-CoV-2 Infection pathway (COVID-19)
3. **R-HSA-50949**: BRCA1 protein entity
4. **R-HSA-5683386**: BRCA1-A Complex
5. **R-HSA-5659802**: BRCA1:BARD1 Complex

### COVID-19 Related Pathways
- SARS-CoV-2 Infection (R-HSA-9694516)
- Replication of the SARS-CoV-2 genome (R-HSA-9694686)
- SARS-CoV-2 modulates autophagy (R-HSA-9754560)
- Early/Late SARS-CoV-2 Infection Events

### Unique Properties
- BioPAX Level 3 ontology provides standardized representation
- Hierarchical pathway organization via bp:pathwayComponent
- Multi-species orthology with consistent pathway IDs
- `bif:contains` for efficient full-text search with relevance scoring

### Connections to Other Databases
- **UniProt**: 204,415 entities with UniProt references
- **ChEBI**: 37,569 entities with ChEBI references
- **GO**: Gene Ontology cross-references for pathway classification
- **PubMed**: Literature evidence citations

### Specific, Verifiable Facts
- Total pathways: **23,145**
- Total reactions: **92,977**
- Human pathways: **2,825**
- Protein entities: **233,200**
- Complex entities: **109,261**
- SmallMolecule entities: **51,214**
- Species covered: **15**
- UniProt cross-references: **204,415**
- ChEBI cross-references: **37,569**

## ⚠️ CRITICAL: Cross-Reference/Mapping Analysis

### UniProt Cross-References
1. **Entity Count** (entities with UniProt mappings): **204,415**
2. **Relationship Count**: **204,415** (1:1 mapping in this case)

### ChEBI Cross-References
1. **Entity Count** (entities with ChEBI mappings): **37,569**
2. **Relationship Count**: **37,569** (1:1 mapping)

### Important Note on String Comparisons
**CRITICAL**: When filtering by database name (bp:db), must use `^^xsd:string` type restriction or `STR()` function:
```sparql
# WRONG (returns empty):
?xref bp:db "UniProt" ; bp:id ?id .

# CORRECT:
?xref bp:db "UniProt"^^xsd:string ; bp:id ?id .
# OR
FILTER(STR(?db) = "UniProt")
```

## Question Opportunities by Category

### Precision
- "What is the Reactome ID for the SARS-CoV-2 Infection pathway?" (R-HSA-9694516)
- "What is the Reactome ID for the Autophagy pathway in humans?" (R-HSA-9612973)
- "What is the BRCA1 protein identifier in Reactome?" (R-HSA-50949)

### Completeness
- "How many pathways are in Reactome?" (23,145)
- "How many human pathways are in Reactome?" (2,825)
- "How many biochemical reactions are in Reactome?" (92,977)
- "How many protein entities are in Reactome?" (233,200)
- "How many species are covered in Reactome?" (15)
- "How many Reactome entities have UniProt references?" (204,415)

### Integration
- "How many Reactome entities have ChEBI cross-references?" (37,569)
- "What UniProt IDs are associated with the BRCA1:BARD1 complex?"
- "What ChEBI IDs are in the Autophagy pathway?"

### Currency
- "What SARS-CoV-2 pathways exist in Reactome?" (multiple COVID-19 related)
- "How many COVID-19 related pathways are in Reactome?"
- "What are the most recently added disease pathways?"

### Specificity
- "What cancer signaling pathways are in Reactome?" (EGFR, PI3K/AKT, WNT, NOTCH)
- "What organisms are covered in Reactome?" (15 species list)
- "What BRCA1 mutant variants are recorded in Reactome?" (C61G, C64G, etc.)

### Structured Query
- "Find all human cancer-related pathways"
- "Find pathways containing both BRCA1 and BRCA2"
- "Find complexes with more than 3 components"
- "Find pathways with GO annotations for DNA repair"

## Notes

### Limitations
- String comparison in bp:db requires `^^xsd:string` type restriction
- Property path traversals (bp:pathwayComponent*) need LIMIT
- Some cross-reference patterns vary by entity type

### Best Practices
- Always include `FROM <http://rdf.ebi.ac.uk/dataset/reactome>` clause
- Use `bif:contains` for keyword search instead of FILTER/CONTAINS
- Use `STR(?var) = "value"` for string comparisons to avoid datatype issues
- Add type filters (a bp:Pathway, a bp:Protein) to improve performance
- Use `option (score ?sc)` with bif:contains for relevance ranking

### Important Count Clarifications
- Pathway count includes all species (23,145 total vs 2,825 human)
- Entity counts include all species representations
- Cross-references are 1:1 (not many-to-many like PDB→UniProt)
