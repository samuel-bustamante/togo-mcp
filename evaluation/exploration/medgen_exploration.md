# MedGen (Medical Genetics) Exploration Report

## Database Overview
- **Purpose**: NCBI's portal for information about medical conditions with a genetic component
- **Scope**: 233,000+ clinical concepts (ConceptID entities) covering diseases, phenotypes, and clinical findings
- **Key entities**: ConceptID (clinical concepts), MGREL (relationships), MGSAT (attributes), MGCONSO (terminology mappings)
- **Cross-references**: OMIM, Orphanet, HPO, MONDO, MeSH, SNOMED CT, ICD-10

## Schema Analysis (from MIE file)

### Main Properties Available
- **ConceptID**: dct:identifier (CUI), rdfs:label, mo:sty (semantic type), skos:definition
- **MGREL**: mo:cui1, mo:cui2, mo:rela (relationship type), dct:source
- **MGSAT**: mo:atn (attribute name), mo:atv (attribute value), dct:source
- **MGCONSO**: rdfs:seeAlso (external database links), mo:aui, dct:source

### Important Relationships
- **CRITICAL**: Relationships are stored in MGREL entities, NOT as direct properties on ConceptID
- Relationship types: isa, inverse_isa, has_manifestation, manifestation_of, disease_may_have_finding
- External links via mo:mgconso blank nodes containing rdfs:seeAlso
- Semantic types from UMLS classify concepts

### Key Query Patterns
- Use MGREL to find concept relationships
- Access external references via mo:mgconso → rdfs:seeAlso
- Use bif:contains for keyword search
- Always use DISTINCT for cross-reference queries (many duplicates)

## Search Queries Performed

1. **Query: Concept C0023467 (Acute myeloid leukemia)**
   - Results: Found with definition, semantic type T191 (Neoplastic Process)
   - Has complete metadata

2. **Query: Diabetes-related concepts**
   - Results: 20+ concepts including Gestational diabetes (C0085207), Nephrogenic diabetes insipidus (C0162283), Lipoatrophic diabetes (C0011859)
   - bif:contains search works well

3. **Query: External references for Diabetes mellitus (C0011849)**
   - Results: HPO (HP_0000819), MONDO (0005015), MeSH (D003920), NCI (C2985), OMIM, SNOMED CT
   - Multiple external mappings

4. **Query: Relationships for Diabetes mellitus**
   - Results: has_manifestation (Kearns-Sayre, Werner syndrome, MELAS), isa relationships (subtypes)
   - MGREL contains relationship network

5. **Query: Fabry disease via ncbi_esearch**
   - Results: Found Fabry disease (CUI C0002986, MedGen UID 8083)
   - MONDO:0010526, OMIM:301500, MeSH:D000795
   - X-linked inheritance, GLA gene association

## SPARQL Queries Tested

```sparql
# Query 1: Find concept by identifier
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?concept ?identifier ?label ?sty ?definition
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?concept a mo:ConceptID ;
      dct:identifier "C0023467" ;
      rdfs:label ?label ;
      mo:sty ?sty .
  OPTIONAL { ?concept skos:definition ?definition }
}
# Results: Acute myeloid leukemia with definition
```

```sparql
# Query 2: Keyword search with bif:contains
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?concept ?identifier ?label
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?concept a mo:ConceptID ;
      rdfs:label ?label ;
      dct:identifier ?identifier .
  ?label bif:contains "'diabetes'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 20
# Results: 20 diabetes-related concepts
```

```sparql
# Query 3: External database cross-references
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT DISTINCT ?concept ?identifier ?external_db
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?concept a mo:ConceptID ;
      dct:identifier "C0011849" ;
      mo:mgconso ?bn .
  ?bn rdfs:seeAlso ?external_db .
}
# Results: HPO, MONDO, MeSH, NCI, OMIM, SNOMED CT mappings
```

```sparql
# Query 4: Concept relationships via MGREL
PREFIX mo: <http://med2rdf/ontology/medgen#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?disease ?disease_label ?related ?related_label ?rel_type
FROM <http://rdfportal.org/dataset/medgen>
WHERE {
  ?disease a mo:ConceptID ;
      dct:identifier "C0011849" ;
      rdfs:label ?disease_label .
  ?rel a mo:MGREL ;
      mo:cui1 ?disease ;
      mo:cui2 ?related ;
      mo:rela ?rel_type .
  ?related rdfs:label ?related_label .
}
LIMIT 30
# Results: Manifestations (Werner, MELAS, Kearns-Sayre), subtypes (gestational, lipoatrophic)
```

## Interesting Findings

### Specific Entities for Questions
- **Fabry disease**: CUI C0002986, MedGen UID 8083, MONDO:0010526, OMIM:301500
- **Acute myeloid leukemia**: CUI C0023467
- **Diabetes mellitus**: CUI C0011849, MONDO:0005015, MeSH:D003920
- **Gestational diabetes**: CUI C0085207

### Key Statistics
- Total concepts: 233,939
- Total relationships: 1,130,420
- Total attributes: 1,117,180
- Definition coverage: ~34%
- External mapping coverage: ~90%

### Cross-Database Mappings
- MONDO coverage: ~70%
- MeSH coverage: ~80%
- HPO coverage: ~40%
- OMIM coverage: ~30%
- Orphanet coverage: ~20% (rare diseases)
- SNOMED CT coverage: ~60%

### Verifiable Facts
- Fabry disease has CUI C0002986 and maps to MONDO:0010526
- Fabry disease is associated with GLA gene on chromosome X
- Diabetes mellitus (C0011849) has has_manifestation relationships with MELAS, Werner, Kearns-Sayre
- Semantic type T047 = Disease or Syndrome

## Question Opportunities by Category

### Precision
- "What is the MedGen CUI for Fabry disease?" (Answer: C0002986)
- "What MONDO ID maps to MedGen concept C0002986?" (Answer: MONDO:0010526)
- "What OMIM number is associated with Fabry disease in MedGen?" (Answer: 301500)
- "What gene is associated with Fabry disease?" (Answer: GLA)

### Completeness
- "How many clinical concepts are in MedGen?" (Answer: 233,939)
- "List all diseases that are manifestations of Diabetes mellitus (C0011849)"
- "How many concepts have MONDO cross-references?"
- "What syndromes have diabetes as a manifestation?"

### Integration
- "What HPO term corresponds to MedGen C0011849?" (Answer: HP:0000819)
- "What MeSH descriptor ID maps to MedGen diabetes mellitus?" (Answer: D003920)
- "Convert MedGen CUI C0002986 to OMIM number" (Answer: 301500)

### Currency
- "What are the recently added rare disease concepts in MedGen?"
- "What clinical features are documented for Fabry disease?"

### Specificity
- "What is the inheritance pattern for Fabry disease?" (Answer: X-linked)
- "What chromosome is the GLA gene located on for Fabry disease?" (Answer: X, Xq22.1)
- "What clinical features are associated with Fabry disease?"

### Structured Query
- "Find all MedGen concepts with has_manifestation relationship to diabetes mellitus"
- "Find all diseases classified as T047 (Disease or Syndrome) with OMIM cross-references"
- "Find concepts that have both HPO and MONDO mappings"

## Notes

### Critical Limitations
- **Relationships are in MGREL, not direct properties** - Do NOT query mo:disease_has_associated_gene on ConceptID
- Only ~34% of concepts have definitions
- Always use DISTINCT for cross-reference queries

### Best Practices
- Use ncbi_esearch for initial concept discovery
- Use ncbi_esummary for detailed concept information
- Use SPARQL with MGREL for relationship traversal
- Always specify FROM <http://rdfportal.org/dataset/medgen>
- Use LIMIT when querying MGREL, MGSAT (>1M records each)

### Search Tool Usage
- ncbi_esearch: Good for initial concept lookup by name
- ncbi_esummary: Get detailed metadata including clinical features, inheritance, genes
- SPARQL: Navigate relationships and cross-references

### External Database URI Patterns
- MONDO: `http://purl.obolibrary.org/obo/MONDO_xxxxxxx`
- HPO: `http://purl.obolibrary.org/obo/HP_xxxxxxx`
- MeSH: `http://id.nlm.nih.gov/mesh/Dxxxxxx`
- OMIM: `http://identifiers.org/mim/xxxxxx`
- SNOMED CT: `http://purl.bioontology.org/ontology/SNOMEDCT/xxxxxxxxx`
