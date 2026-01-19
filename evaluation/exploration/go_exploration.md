# Gene Ontology (GO) Exploration Report

## Database Overview
- **Purpose**: Controlled vocabulary for describing gene and gene product attributes across all organisms
- **Key data types**: GO terms organized into three namespaces (biological_process, molecular_function, cellular_component)
- **Scale**: 48,165 GO terms (30,804 biological_process, 12,793 molecular_function, 4,568 cellular_component)
- **Structure**: Hierarchical ontology with parent-child relationships (directed acyclic graph)

## Schema Analysis (from MIE file)

### Main Entity Type
**GOTermShape (owl:Class)**:
- Properties: oboinowl:id, rdfs:label, obo:IAO_0000115 (definition)
- Namespace: oboinowl:hasOBONamespace
- Hierarchy: rdfs:subClassOf
- Synonyms: hasExactSynonym, hasRelatedSynonym, hasNarrowSynonym, hasBroadSynonym
- Cross-refs: hasDbXref
- Status: owl:deprecated

### Query Patterns
- CRITICAL: Always use `FROM <http://rdfportal.org/ontology/go>`
- Use `bif:contains` for keyword search
- Use `STR()` for namespace comparisons
- Filter by `STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_")` to get only GO terms
- Use DISTINCT to remove duplicates

## Search Queries Performed

1. **Query**: OLS4 getDescendants for GO:0006914 (autophagy)
   - Results: 25 descendant terms including macroautophagy, microautophagy, mitophagy, pexophagy, etc.

2. **Query**: Terms by namespace distribution
   - Results: biological_process (30,804), molecular_function (12,793), cellular_component (4,568)

3. **Query**: Autophagy-related terms hierarchy
   - Results: macroautophagy (GO:0016236), microautophagy (GO:0016237), mitophagy (GO:0000423), etc.

## SPARQL Queries Tested

```sparql
# Query 1: Count terms by namespace
PREFIX oboinowl: <http://www.geneontology.org/formats/oboInOwl#>
SELECT ?namespace (COUNT(DISTINCT ?go) as ?count)
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?go oboinowl:hasOBONamespace ?namespace .
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
GROUP BY ?namespace
ORDER BY DESC(?count)
# Results: biological_process (30,804), molecular_function (12,793), cellular_component (4,568)
```

```sparql
# Query 2: Search terms by keyword
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?go ?label
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?go rdfs:label ?label .
  ?label bif:contains "'apoptosis'" .
  FILTER(STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_"))
}
LIMIT 20
# Results: Multiple apoptosis-related terms
```

```sparql
# Query 3: Find parent terms of a specific term
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?child ?childLabel ?parent ?parentLabel
FROM <http://rdfportal.org/ontology/go>
WHERE {
  ?child rdfs:subClassOf ?parent .
  ?child rdfs:label ?childLabel .
  ?parent rdfs:label ?parentLabel .
  FILTER(?child = obo:GO_0006338)
  FILTER(STRSTARTS(STR(?parent), "http://purl.obolibrary.org/obo/GO_"))
}
# Results: Parent relationships for chromatin remodeling
```

## Interesting Findings

### Specific Entities for Questions
- **GO:0006914 (autophagy)**: Has 25 descendant terms including macroautophagy, microautophagy, mitophagy
- **GO:0016236 (macroautophagy)**: Child of autophagy
- **GO:0005634 (nucleus)**: Cellular component term with extensive synonyms
- **GO:0004672 (protein kinase activity)**: Molecular function term

### Autophagy Hierarchy (25 descendants)
- macroautophagy (GO:0016236)
- microautophagy (GO:0016237)
- chaperone-mediated autophagy (GO:0061684)
- mitophagy (GO:0000423) - degradation of mitochondria
- pexophagy (GO:0000425) - degradation of peroxisomes
- reticulophagy (GO:0061709) - ER degradation
- lipophagy (GO:0061724) - lipid droplet degradation
- ribophagy (GO:0034517) - ribosome degradation
- aggrephagy (GO:0035973) - protein aggregate degradation
- xenophagy (GO:0098792) - pathogen degradation

### Cross-Database Connections
- Wikipedia (extensive coverage)
- Reactome (biochemical pathways)
- KEGG_REACTION (metabolic reactions)
- EC (enzyme classification)
- MeSH (medical subject headings)
- NIF_Subcellular (subcellular structures)

### Verifiable Facts
- 48,165 total GO terms
- 30,804 biological_process terms
- 12,793 molecular_function terms
- 4,568 cellular_component terms
- GO:0006914 (autophagy) has exactly 25 descendant terms
- ~100% of terms have definitions
- ~80% of terms have synonyms
- ~52% of terms have cross-references

## Question Opportunities by Category

### Precision
- "What is the GO ID for autophagy?" (Answer: GO:0006914)
- "What is the GO ID for the nucleus cellular component?" (Answer: GO:0005634)
- "What is the definition of GO:0004672 (protein kinase activity)?"

### Completeness
- "How many descendant terms does GO:0006914 (autophagy) have?" (Answer: 25)
- "How many biological_process terms are in GO?" (Answer: 30,804)
- "What are all the direct children of GO:0006914 (autophagy)?" (List of ~6 children)

### Integration
- "What Wikipedia articles are linked to GO terms?" (via hasDbXref)
- "Find GO terms linked to Reactome pathways"

### Currency
- "What new GO terms have been added recently?"

### Specificity
- "What is the GO ID for mitophagy (selective autophagy of mitochondria)?" (Answer: GO:0000423)
- "Find GO terms related to protein kinase activity"
- "What GO terms contain 'CRISPR' in their label or definition?"

### Structured Query
- "Find all molecular_function terms containing 'kinase'"
- "Find biological_process terms with both 'DNA' AND 'repair' keywords"
- "List GO terms in the goslim_generic subset"
- "Find deprecated GO terms and their replacements"

## Notes

### Limitations
- Aggregation queries may timeout without LIMIT
- Duplicate rows common (use DISTINCT)
- Graph may contain other OBO ontology terms (filter by GO_ prefix)

### Best Practices
- CRITICAL: Always use `FROM <http://rdfportal.org/ontology/go>`
- Use `bif:contains` instead of REGEX for keyword search
- Use `STR()` for namespace comparisons
- Filter by `STRSTARTS(STR(?go), "http://purl.obolibrary.org/obo/GO_")`
- Use DISTINCT in SELECT queries
- Use LIMIT to prevent timeout

### OLS4 Tools
- OLS4:searchClasses - for keyword-based term search
- OLS4:getDescendants - for finding all child terms
- OLS4:getAncestors - for finding all parent terms
- OLS4:fetch - for getting details of a specific term
