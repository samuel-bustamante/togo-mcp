# MONDO (Monarch Disease Ontology) Exploration Report

## Database Overview
- **Purpose**: Comprehensive disease ontology integrating multiple disease databases into unified classification
- **Scope**: 30,304 disease classes covering genetic disorders, infectious diseases, cancers, and rare diseases
- **Key data types**: Disease classes, synonyms, definitions, hierarchical relationships, cross-references

## Schema Analysis (from MIE file)

### Main Entity Types
- **owl:Class** - Disease class definitions
- Each disease has: label, MONDO ID, definition, synonyms, parent classes, cross-references

### Key Properties
- `rdfs:label` - Primary disease name
- `oboInOwl:id` - MONDO identifier (e.g., "MONDO:0007739")
- `IAO:0000115` - Definition/description
- `oboInOwl:hasExactSynonym` - Exact synonyms
- `oboInOwl:hasDbXref` - Cross-references to external databases
- `rdfs:subClassOf` - Hierarchical parent relationship
- `owl:deprecated` - Mark obsolete terms

### Cross-Reference Coverage (Entity vs Relationship Counts)
| Database | Entity Count | Relationship Count | Notes |
|----------|--------------|-------------------|-------|
| UMLS | 21,372 | 21,372 | 1:1 mapping |
| MEDGEN | 21,372 | 21,372 | 1:1 mapping |
| DOID | 11,698 | 11,866 | Slight 1:N mapping |
| GARD | 10,730 | 10,730 | 1:1 mapping |
| Orphanet | 10,246 | 10,344 | Slight 1:N mapping |
| OMIM | 9,944 | 10,039 | ~1.01 avg mappings |
| SCTID | 9,052 | 9,279 | SNOMED CT |
| MESH | 8,253 | 8,378 | MeSH |
| NCIT | 7,425 | 7,549 | NCI Thesaurus |
| ICD9 | 4,417 | 5,734 | Multiple ICD9 per disease |
| NANDO | 1,572 | 2,345 | ~1.5 avg (Japanese rare diseases) |

## Search Queries Performed

1. **Diabetes search** → Found 20 diabetes-related diseases including type 1, type 2, gestational, neonatal variants

2. **Leukemia search (OLS4)** → Found 334 leukemia-related entries with hierarchy

3. **Progeria search** → Found 5 progeria variants including Hutchinson-Gilford progeria syndrome

4. **NANDO cross-references** → Found 1,572 diseases with NANDO links (Japanese rare diseases)

5. **OMIM cross-references** → 9,944 diseases have OMIM references (10,039 total refs)

## SPARQL Queries Tested

```sparql
# Query 1: Search diseases by keyword with relevance scoring
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT ?disease ?mondoId ?label
FROM <http://rdfportal.org/ontology/mondo>
WHERE {
  ?disease a owl:Class ;
    rdfs:label ?label ;
    oboInOwl:id ?mondoId .
  ?label bif:contains "'diabetes'" option (score ?sc)
  FILTER NOT EXISTS { ?disease owl:deprecated true }
}
ORDER BY DESC(?sc)
# Results: Type 2 diabetes (MONDO:0005148), multiple diabetes subtypes
```

```sparql
# Query 2: Count cross-references by database prefix
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>

SELECT ?prefix (COUNT(DISTINCT ?disease) as ?entity_count) (COUNT(?xref) as ?relationship_count)
FROM <http://rdfportal.org/ontology/mondo>
WHERE {
  ?disease a owl:Class ;
    oboInOwl:hasDbXref ?xref .
  BIND(STRBEFORE(?xref, ":") AS ?prefix)
}
GROUP BY ?prefix
# Results: UMLS (21,372), MEDGEN (21,372), DOID (11,698), etc.
```

```sparql
# Query 3: Get complete profile for Huntington disease
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
PREFIX IAO: <http://purl.obolibrary.org/obo/IAO_>

SELECT ?label ?definition ?synonym ?xref ?parentLabel
FROM <http://rdfportal.org/ontology/mondo>
WHERE {
  obo:MONDO_0007739 rdfs:label ?label .
  OPTIONAL { obo:MONDO_0007739 IAO:0000115 ?definition }
  OPTIONAL { obo:MONDO_0007739 oboInOwl:hasExactSynonym ?synonym }
  OPTIONAL { obo:MONDO_0007739 oboInOwl:hasDbXref ?xref }
  OPTIONAL { 
    obo:MONDO_0007739 rdfs:subClassOf ?parent .
    ?parent rdfs:label ?parentLabel .
    FILTER(isIRI(?parent))
  }
}
# Results: Huntington disease with 16 cross-references (OMIM:143100, Orphanet:399, NANDO:1200012, etc.)
```

```sparql
# Query 4: Find diseases with NANDO cross-references
SELECT ?disease ?mondoId ?label ?nandoRef
FROM <http://rdfportal.org/ontology/mondo>
WHERE {
  ?disease a owl:Class ;
    rdfs:label ?label ;
    oboInOwl:id ?mondoId ;
    oboInOwl:hasDbXref ?nandoRef .
  FILTER(STRSTARTS(?nandoRef, "NANDO:"))
}
# Results: Found 1,572 diseases with NANDO refs (Crohn disease, Duchenne MD, etc.)
```

## Interesting Findings

### Cross-Database Integration
- MONDO serves as a **disease hub** connecting 30+ databases
- Highest coverage: UMLS and MEDGEN (70%)
- Japanese rare diseases via NANDO (5%)
- Clinical coding via ICD-9, ICD-10, ICD-11

### Specific Verifiable Facts
- Huntington disease = MONDO:0007739 = OMIM:143100 = Orphanet:399 = NANDO:1200012
- Type 2 diabetes mellitus = MONDO:0005148
- Hutchinson-Gilford progeria syndrome = MONDO:0008310
- 26,371 active (non-deprecated) disease classes
- 3,933 deprecated terms

### Rich Annotation Data
- 75% of diseases have definitions
- 85% have synonyms (avg 2.8 per disease)
- 90% have cross-references (avg 6.5 per disease)

## Question Opportunities by Category

### Precision Questions
- What is the MONDO ID for Huntington disease?
- What is the OMIM cross-reference for achondroplasia (MONDO:0000003)?
- What is the ICD-10 code for Huntington disease in MONDO?

### Completeness Questions
- How many disease classes are in MONDO?
- How many MONDO diseases have OMIM cross-references? (Entity count: 9,944)
- How many total OMIM cross-reference relationships exist? (Relationship count: 10,039)
- How many deprecated disease classes are in MONDO?

### Integration Questions
- What NANDO ID corresponds to MONDO:0007739 (Huntington disease)?
- Convert Orphanet:399 to MONDO ID
- Find all MONDO diseases with both OMIM and Orphanet references

### Specificity Questions
- What rare diseases in MONDO have NANDO cross-references?
- Find all progeria-related diseases in MONDO
- What diseases are classified under "hereditary disease" (MONDO:0003847)?

### Structured Query Questions
- Find all leukemia subtypes in MONDO with their parent classes
- List diseases with more than 10 cross-references
- Find diseases with both ICD-10 and MESH cross-references

## Cross-Reference Mapping Analysis

### NANDO Mappings (Important for Japanese rare diseases)
- **Entity count**: 1,572 MONDO diseases have NANDO mappings
- **Relationship count**: 2,345 total NANDO cross-references
- **Average**: 1.49 NANDO refs per mapped disease
- **Distribution**: Some diseases map to multiple NANDO IDs (e.g., Crohn disease → 3 NANDO IDs)

### OMIM Mappings
- **Entity count**: 9,944 diseases with OMIM
- **Relationship count**: 10,039 total refs
- **Average**: 1.01 OMIM per disease (mostly 1:1)

## Notes
- Use `bif:contains` for full-text search with relevance scoring
- Add `FILTER(isIRI(?parent))` to exclude OWL restrictions in hierarchy queries
- Use `STRSTARTS(?xref, "PREFIX:")` for efficient cross-reference filtering
- Deprecated terms marked with `owl:deprecated true` - filter these for current data
- OLS4 API provides alternative search with hierarchy information
- MONDO is central hub for disease data integration across databases
