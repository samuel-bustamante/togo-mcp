# ChEBI (Chemical Entities of Biological Interest) Exploration Report

## Database Overview
- **Purpose**: Ontology database of chemical entities of biological interest
- **Key data types**: Small molecules, atoms, ions, functional groups, macromolecules with hierarchical classification
- **Scale**: 223,078 chemical entities (217K+ originally reported, growing), 192,688 with molecular formulas
- **Structure**: OWL ontology with rdfs:subClassOf hierarchy

## Schema Analysis (from MIE file)

### Main Entity Types
1. **ChemicalEntity (owl:Class)**: Core entity
   - Properties: rdfs:label, oboInOwl:id, formula, mass, charge, smiles, inchi, inchikey
   - Hierarchy: rdfs:subClassOf
   - Synonyms: hasRelatedSynonym, hasExactSynonym
   - Cross-refs: hasDbXref

### Important Relationships
- `rdfs:subClassOf` for ontology hierarchy
- Chemical relationships via OWL restrictions:
  - `chebi#is_conjugate_acid_of`
  - `chebi#is_conjugate_base_of`
  - `chebi#is_tautomer_of`
  - `chebi#is_enantiomer_of`
- Biological roles via `obo:RO_0000087`

### Query Patterns
- CRITICAL: Two namespaces - `chebi/` for data properties, `chebi#` for relationship properties
- Use OLS4:searchClasses for keyword-based entity search
- Use `bif:contains` for SPARQL full-text search
- Filter by `CHEBI_` URI prefix to exclude non-entity classes

## Search Queries Performed

1. **Query**: OLS4 search for "aspirin"
   - Results: 19 matches including aspirin-based probe, aspirin-triggered resolvins, acetylsalicylic acid

2. **Query**: OLS4 search for "rapamycin"
   - Results: 15 matches including sirolimus (CHEBI:9168), various rapamycin derivatives

3. **Query**: Total chemical entities count
   - Results: 223,078 entities

4. **Query**: Entities with molecular formulas
   - Results: 192,688 entities (~86%)

5. **Query**: Molecular properties of aspirin (CHEBI:15365)
   - Results: Formula C9H8O4, mass 180.15740, SMILES CC(=O)Oc1ccccc1C(O)=O

6. **Query**: ATP(4-) properties (CHEBI:30616)
   - Results: Formula C10H12N5O13P3, mass 503.14946

## SPARQL Queries Tested

```sparql
# Query 1: Get molecular properties of aspirin
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX chebi: <http://purl.obolibrary.org/obo/chebi/>
SELECT ?label ?formula ?mass ?smiles ?inchikey
FROM <http://rdf.ebi.ac.uk/dataset/chebi>
WHERE {
  obo:CHEBI_15365 rdfs:label ?label .
  OPTIONAL { obo:CHEBI_15365 chebi:formula ?formula }
  OPTIONAL { obo:CHEBI_15365 chebi:mass ?mass }
  OPTIONAL { obo:CHEBI_15365 chebi:smiles ?smiles }
  OPTIONAL { obo:CHEBI_15365 chebi:inchikey ?inchikey }
}
# Results: acetylsalicylic acid, C9H8O4, 180.15740, CC(=O)Oc1ccccc1C(O)=O
```

```sparql
# Query 2: Count total ChEBI entities
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT (COUNT(?entity) as ?totalEntities)
FROM <http://rdf.ebi.ac.uk/dataset/chebi>
WHERE {
  ?entity a owl:Class .
  FILTER(STRSTARTS(STR(?entity), "http://purl.obolibrary.org/obo/CHEBI_"))
}
# Results: 223,078 entities
```

```sparql
# Query 3: Count entities with molecular formulas
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX chebi: <http://purl.obolibrary.org/obo/chebi/>
SELECT (COUNT(DISTINCT ?entity) as ?entitiesWithFormula)
FROM <http://rdf.ebi.ac.uk/dataset/chebi>
WHERE {
  ?entity a owl:Class .
  ?entity chebi:formula ?formula .
  FILTER(STRSTARTS(STR(?entity), "http://purl.obolibrary.org/obo/CHEBI_"))
}
# Results: 192,688 entities
```

## Interesting Findings

### Specific Entities for Questions
- **Aspirin**: CHEBI:15365 (acetylsalicylic acid), formula C9H8O4, mass 180.15740
- **ATP**: CHEBI:30616 (ATP(4-)), formula C10H12N5O13P3
- **Sirolimus/Rapamycin**: CHEBI:9168, a macrolide lactam immunosuppressant
- **Water**: CHEBI:15377, H2O, mass 18.01530
- **L-proline**: CHEBI:17203, C5H9NO2, mass 115.13050

### Unique Properties
- Hierarchical classification via rdfs:subClassOf
- Chemical relationships (conjugate acid/base, tautomers, enantiomers) via OWL restrictions
- Biological roles encoded through RO_0000087
- Comprehensive structural identifiers: SMILES, InChI, InChIKey

### Cross-Database Connections
- KEGG compound IDs
- DrugBank IDs
- PubChem IDs
- HMDB (Human Metabolome Database)
- CAS registry numbers
- Wikipedia links
- PubMed IDs

### Verifiable Facts
- 223,078 total ChEBI entities
- 192,688 entities have molecular formulas (~86%)
- Aspirin (CHEBI:15365) has molecular formula C9H8O4 and mass 180.15740
- ATP(4-) (CHEBI:30616) has formula C10H12N5O13P3
- Sirolimus (rapamycin) is CHEBI:9168

## Question Opportunities by Category

### Precision
- "What is the ChEBI ID for aspirin?" (Answer: CHEBI:15365)
- "What is the molecular formula of ATP according to ChEBI?" (Answer: C10H12N5O13P3)
- "What is the molecular weight of acetylsalicylic acid in ChEBI?" (Answer: 180.15740)
- "What is the InChIKey for water in ChEBI?" (Answer: XLYOFNOQVPJJNP-UHFFFAOYSA-N)

### Completeness
- "How many chemical entities are in ChEBI?" (Answer: 223,078)
- "How many ChEBI entities have molecular formula data?" (Answer: 192,688)
- "What are the parent classes of L-proline in ChEBI?"

### Integration
- "What DrugBank ID is linked to sirolimus in ChEBI?" (via hasDbXref)
- "What KEGG compound ID corresponds to ATP?" (KEGG:C00002)
- "Find ChEBI entries cross-referenced to PubChem"

### Currency
- "What new chemical entities have been added to ChEBI recently?"

### Specificity
- "What is the ChEBI ID for the immunosuppressant rapamycin?" (Answer: CHEBI:9168)
- "What are the aspirin-triggered resolvins in ChEBI?" (Multiple IDs)
- "Find macrolide lactam compounds in ChEBI"

### Structured Query
- "Find all ChEBI entities with molecular mass greater than 500"
- "Find compounds that are conjugate acids of another compound"
- "List ChEBI entities classified as antibiotics with DrugBank cross-references"

## Notes

### Limitations
- Not all entities have complete molecular properties
- Abstract chemical classes lack molecular data
- Chemical relationships encoded as OWL restrictions require specific query patterns

### Best Practices
- Always use correct namespace: `chebi/` for data properties, `chebi#` for relationships
- Filter by `CHEBI_` URI prefix to get only chemical entities
- Use OLS4:searchClasses for keyword-based searches
- Use `bif:contains` for advanced SPARQL text search
- Use OPTIONAL for molecular properties (not all entities have all data)
- Check owl:deprecated status for deprecated entries

### Important Namespace Notes
```
# Data properties (formula, mass, smiles, etc.)
PREFIX chebi: <http://purl.obolibrary.org/obo/chebi/>

# Relationship properties (is_conjugate_acid_of, etc.)
PREFIX chebi_rel: <http://purl.obolibrary.org/obo/chebi#>
```
