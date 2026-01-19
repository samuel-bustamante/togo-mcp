# MeSH (Medical Subject Headings) Exploration Report

## Database Overview
- **Purpose**: National Library of Medicine's controlled vocabulary thesaurus for biomedical literature indexing
- **Scope**: ~30K topical descriptors, ~250K chemical records, ~2.5M total entities with hierarchical organization
- **Key entities**: TopicalDescriptor, SCR_Chemical, Concept, Term, Qualifier, TreeNumber
- **Cross-references**: OMIM, ChEBI, FDA SRS/UNII, SNOMED CT

## Schema Analysis (from MIE file)

### Main Properties Available
- **TopicalDescriptor**: rdfs:label, meshv:identifier (D-number), meshv:treeNumber, meshv:broaderDescriptor, meshv:annotation, meshv:allowableQualifier
- **SCR_Chemical**: rdfs:label, meshv:identifier (C-number), meshv:registryNumber (CAS)
- **Concept**: rdfs:label, meshv:preferredTerm
- **Term**: meshv:prefLabel

### Important Relationships
- **CRITICAL**: Use `meshv:broaderDescriptor` (NOT meshv:broader) for hierarchy
- **CRITICAL**: Use `meshv:annotation` (NOT meshv:scopeNote) for notes
- Tree numbers provide alphanumeric hierarchical codes (A-Z categories)
- Allowable qualifiers constrain valid descriptor-qualifier combinations

### Key Query Patterns
- Use bif:contains for keyword searches with relevance scoring
- Use meshv:broaderDescriptor+ for transitive hierarchy traversal
- Tree numbers useful for category-based queries
- FROM <http://id.nlm.nih.gov/mesh> required for all queries

## Search Queries Performed

1. **Query: Diabetes mellitus descriptors**
   - Results: D003920 (Diabetes Mellitus), D003922 (Type 1), D003924 (Type 2), D003923 (Lipoatrophic)
   - Tree numbers: C18.452.394.750, C19.246

2. **Query: Hierarchical parents of Type 2 Diabetes (D003924)**
   - Results: Diabetes Mellitus → Glucose Metabolism Disorders → Metabolic Diseases → Nutritional and Metabolic Diseases
   - broaderDescriptor+ transitive query works

3. **Query: Insulin chemicals**
   - Results: 15+ insulin variants including insulin combinations, modified insulins
   - SCR_Chemical class with registryNumbers

4. **Query: Erdheim-Chester Disease (rare disease)**
   - Results: D031249 with identifier confirmed
   - Good for specificity questions

5. **Query: Category distribution**
   - Results: D (Chemicals/Drugs): 10,541; C (Diseases): 5,032; B (Organisms): 3,964; E (Analytical/Diagnostic): 3,102

## SPARQL Queries Tested

```sparql
# Query 1: Search descriptors by keyword
PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?descriptor ?label ?identifier ?treeNumber
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  ?descriptor a meshv:TopicalDescriptor ;
    rdfs:label ?label ;
    meshv:identifier ?identifier .
  OPTIONAL { 
    ?descriptor meshv:treeNumber ?tree .
    ?tree rdfs:label ?treeNumber
  }
  ?label bif:contains "'diabetes mellitus'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 15
# Results: D003920 (Diabetes Mellitus), D003922 (Type 1), D003924 (Type 2)
```

```sparql
# Query 2: Hierarchical parent traversal
PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?parent ?parentLabel
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  mesh:D003924 meshv:broaderDescriptor+ ?parent .
  ?parent rdfs:label ?parentLabel .
}
# Results: Diabetes Mellitus → Glucose Metabolism Disorders → Metabolic Diseases
```

```sparql
# Query 3: Chemical records search
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>

SELECT ?chemical ?label ?registryNumber
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  ?chemical a meshv:SCR_Chemical ;
    rdfs:label ?label .
  OPTIONAL { ?chemical meshv:registryNumber ?registryNumber }
  ?label bif:contains "'insulin'" option (score ?sc)
}
ORDER BY DESC(?sc)
LIMIT 15
# Results: Insulin variants and combinations
```

```sparql
# Query 4: Category distribution
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>

SELECT ?category (COUNT(DISTINCT ?descriptor) as ?count)
FROM <http://id.nlm.nih.gov/mesh>
WHERE {
  ?descriptor a meshv:TopicalDescriptor ;
    meshv:treeNumber ?tree .
  ?tree rdfs:label ?treeLabel .
  BIND(SUBSTR(?treeLabel, 1, 1) as ?category)
}
GROUP BY ?category
ORDER BY ?category
# Results: D=10541, C=5032, B=3964, E=3102, G=2430, N=2002
```

## Interesting Findings

### Specific Entities for Questions
- **Diabetes Mellitus, Type 2**: D003924, tree C18.452.394.750.149
- **Erdheim-Chester Disease**: D031249 (rare disease)
- **Insulin Glargine**: C517652
- **Cardiovascular Diseases**: D002318

### Key Statistics
- Total entities: 2,456,909
- Topical descriptors: 30,248
- Terms: 869,536
- Chemical records: 250,445
- ~40% of descriptors have annotations
- ~95% have tree numbers

### Tree Category Codes
- A: Anatomy (1,904)
- B: Organisms (3,964)
- C: Diseases (5,032)
- D: Chemicals and Drugs (10,541)
- E: Analytical, Diagnostic, Therapeutic (3,102)
- F: Psychiatry and Psychology (1,227)
- G: Phenomena and Processes (2,430)
- N: Health Care (2,002)

### Cross-Database Connections
- OMIM: 12.5K links
- ChEBI: 2.5K links
- FDA SRS/UNII: 22.6K links
- SNOMED CT: 800+ links

### Verifiable Facts
- Diabetes Mellitus Type 2 has MeSH ID D003924
- D003924 has parent D003920 (Diabetes Mellitus)
- Erdheim-Chester Disease has MeSH ID D031249
- Category C (Diseases) has 5,032 descriptors

## Question Opportunities by Category

### Precision
- "What is the MeSH descriptor ID for Diabetes Mellitus, Type 2?" (Answer: D003924)
- "What is the MeSH ID for Erdheim-Chester Disease?" (Answer: D031249)
- "What tree number is assigned to Diabetes Mellitus?" (Answer: C18.452.394.750)

### Completeness
- "How many topical descriptors are in MeSH?" (Answer: 30,248)
- "How many descriptors are in the Diseases category (C tree)?" (Answer: 5,032)
- "List all broader descriptors of Diabetes Mellitus, Type 2"

### Integration
- "What OMIM entries are linked to MeSH descriptors?"
- "What ChEBI IDs correspond to MeSH chemical records?"
- "What CAS registry numbers are associated with insulin variants?"

### Currency
- "What are the most recently added MeSH descriptors?"
- "What rare diseases are classified in MeSH?"

### Specificity
- "What is the MeSH descriptor for the rare disease Erdheim-Chester?" (D031249)
- "What chemical supplementary records exist for insulin analogs?"
- "What is the tree path for a specific genetic disorder?"

### Structured Query
- "Find all MeSH descriptors under the Endocrine System Diseases hierarchy"
- "List all allowable qualifiers for the diabetes mellitus descriptor"
- "Find chemicals with CAS registry numbers containing 'insulin'"

## Notes

### Critical Property Names
- Use `meshv:broaderDescriptor` (NOT meshv:broader)
- Use `meshv:annotation` (NOT meshv:scopeNote)
- Terms use `meshv:prefLabel` (NOT rdfs:label for terms)

### Best Practices
- Always include FROM <http://id.nlm.nih.gov/mesh> clause
- Use bif:contains for keyword searches with option (score ?sc)
- Use OPTIONAL for annotation (only ~40% coverage)
- Use LIMIT for exploratory queries (2.5M+ entities)

### Search Tool
- search_mesh_entity: Good for initial term lookup
- Returns term IDs (T-numbers) which need conversion to descriptors

### Cross-Reference Patterns
- OMIM: via meshv:thesaurusID containing "OMIM"
- ChEBI: via meshv:thesaurusID containing "ChEBI"
- CAS: via meshv:registryNumber on SCR_Chemical
