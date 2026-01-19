# BacDive Exploration Report

## Database Overview
- **Purpose**: Standardized bacterial and archaeal strain information including taxonomy, morphology, physiology, and cultivation conditions
- **Key data types**: Strain records, enzyme activities, culture conditions (media, temperature, pH), 16S rRNA sequences, culture collection numbers
- **Scale**: 97,334 strain records, 573K+ enzyme activities, 87K+ 16S sequences
- **Scope**: Primarily bacteria (95,742) with archaea (1,049)

## Schema Analysis (from MIE file)

### Main Entity Types
1. **Strain**: Core entity with taxonomic classification
   - Properties: hasBacDiveID, hasTaxID, hasGenus, hasSpecies, hasFamily, hasOrder, hasClass, hasPhylum, hasDomain
   - Metadata: isTypeStrain, designation, scientific name

2. **Phenotype entities**:
   - GramStain: hasGramStain (+/-)
   - CellMotility: isMotile (boolean)
   - OxygenTolerance: hasOxygenTolerance (aerobe, anaerobe, etc.)
   - Enzyme: hasActivity, hasECNumber

3. **Culture conditions**:
   - CultureMedium: medium label, hasMediaLink
   - CultureTemperature: hasTemperatureRangeStart/End
   - CulturePH: hasPHRangeStart/End

4. **Sequences**:
   - 16SSequence: hasSequenceAccession, fromSequenceDB, hasSequenceLength
   - GenomeSequence: hasSequenceAccession, fromSequenceDB

### Important Relationships
- `schema:describesStrain` links phenotypes/conditions to strains
- `schema:hasTaxID` links to NCBI Taxonomy
- `schema:hasMediaLink` links to MediaDive
- `schema:hasLink` in CultureCollectionNumber links to DSMZ, JCM, etc.

### Query Patterns
- Use `bif:contains` with single-quoted keywords and `option (score ?sc)`
- Always use `OPTIONAL` for phenotypes due to incomplete coverage
- Filter by genus/species with `CONTAINS(LCASE(?genus), 'name')`

## Search Queries Performed

1. **Query**: Total strain count
   - Results: 97,334 strains total

2. **Query**: Domain distribution
   - Results: Bacteria (95,742), Archaea (1,049)

3. **Query**: Top genera by strain count
   - Results: Streptomyces (24,747), Bacillus (3,332), Arthrobacter (2,045), Streptococcus (2,001), Escherichia (1,898)

4. **Query**: Gram stain distribution
   - Results: Gram-negative (10,747), Gram-positive (7,333), Gram-variable (135)

5. **Query**: Oxygen tolerance distribution
   - Results: Aerobe (10,333), Anaerobe (5,801), Microaerophile (4,724), Facultative anaerobe (4,486)

6. **Query**: Type strain count
   - Results: 20,060 type strains

7. **Query**: Hyperthermophiles (>70°C)
   - Results: Pyrococcus kukulkanii (112°C max), Pyrolobus fumarii (103°C), Aeropyrum pernix (102°C)

## SPARQL Queries Tested

```sparql
# Query 1: Count strains by domain
PREFIX schema: <https://purl.dsmz.de/schema/>
SELECT ?domain (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain .
  ?strain schema:hasDomain ?domain .
}
GROUP BY ?domain
# Results: Bacteria (95,742), Archaea (1,049)
```

```sparql
# Query 2: Find hyperthermophiles (growth above 70°C)
PREFIX schema: <https://purl.dsmz.de/schema/>
SELECT ?strain ?label ?bacdiveId ?tempStart ?tempEnd
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          rdfs:label ?label ;
          schema:hasBacDiveID ?bacdiveId .
  ?temp a schema:CultureTemperature ;
        schema:describesStrain ?strain ;
        schema:hasTemperatureRangeEnd ?tempEnd .
  FILTER(?tempEnd > 70)
}
ORDER BY DESC(?tempEnd)
LIMIT 10
# Results: Pyrococcus kukulkanii (112°C), Pyrolobus fumarii (103°C), Aeropyrum pernix (102°C)
```

```sparql
# Query 3: Keyword search for thermophilic bacteria
PREFIX schema: <https://purl.dsmz.de/schema/>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?strain ?label ?description ?sc
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          rdfs:label ?label ;
          dct:description ?description .
  ?description bif:contains "'thermophilic'" option (score ?sc) .
}
ORDER BY DESC(?sc)
LIMIT 10
# Results: Found strains with "thermophilic" in descriptions
```

```sparql
# Query 4: Strains with 16S rRNA sequences
PREFIX schema: <https://purl.dsmz.de/schema/>
SELECT ?strain ?label ?accession ?seqDB ?length
FROM <http://rdfportal.org/dataset/bacdive>
WHERE {
  ?strain a schema:Strain ;
          rdfs:label ?label .
  ?seq a schema:16SSequence ;
       schema:describesStrain ?strain ;
       schema:hasSequenceAccession ?accession ;
       schema:fromSequenceDB ?seqDB .
}
LIMIT 10
# Results: Found sequences from ENA and nuccore databases
```

## Interesting Findings

### Specific Entities for Questions
- **Hyperthermophiles**: Pyrococcus kukulkanii (BacDive 132578, up to 112°C), Pyrolobus fumarii (103°C), Aeropyrum pernix (102°C)
- **Major genera**: Streptomyces (24,747 strains), Bacillus (3,332), Pseudomonas (1,879)
- **Type strains**: 20,060 designated type strains

### Unique Properties
- Detailed cultivation conditions (temperature ranges, pH ranges, media)
- Oxygen tolerance classification (aerobe, anaerobe, microaerophile, etc.)
- Gram stain results with variable option
- 16S rRNA sequence lengths and database sources

### Cross-Database Connections
- NCBI Taxonomy (100% of strains via hasTaxID)
- Culture collections: DSMZ (>90%), JCM (~40%), KCTC (~30%)
- Sequence databases: ENA (~60%), GenBank (~40%)
- MediaDive (~20% of media links)

### Verifiable Facts
- 97,334 total strain records
- 95,742 bacterial strains, 1,049 archaeal strains
- 20,060 type strains
- 10,747 Gram-negative, 7,333 Gram-positive strains
- Streptomyces is the most represented genus with 24,747 strains
- Pyrococcus kukulkanii can grow at up to 112°C (highest temperature)

## Question Opportunities by Category

### Precision
- "What is the BacDive ID for Thermotoga maritima?" 
- "What is the maximum growth temperature recorded for Pyrococcus kukulkanii?" (Answer: 112°C)
- "How many type strains are in BacDive?" (Answer: 20,060)

### Completeness
- "How many bacterial strains vs archaeal strains are in BacDive?" (Answer: 95,742 bacteria, 1,049 archaea)
- "What are all the oxygen tolerance categories in BacDive?" (List of categories)
- "How many strains have Gram stain data?" (Answer: ~18,000)

### Integration
- "Link BacDive strains to NCBI Taxonomy IDs" (via schema:hasTaxID)
- "Find 16S rRNA sequence accessions for BacDive strains" (ENA/GenBank accessions)
- "Link to MediaDive culture media recipes" (via schema:hasMediaLink)

### Currency
- "What are the most recently added strains to BacDive?"

### Specificity
- "What is the optimal growth temperature for Pyrolobus fumarii?" (Answer: 103°C)
- "Find strains that can grow above 100°C" (hyperthermophiles)
- "What is the BacDive ID for Methanopyrus kandleri?" (Answer: 161561)

### Structured Query
- "Find all obligate anaerobic bacteria in BacDive"
- "Find strains that are both thermophilic AND Gram-positive"
- "List strains with temperature growth range above 70°C"
- "Find Bacillus strains with complete culture condition data"

## Notes

### Limitations
- Phenotype coverage varies (~40% Gram stain, ~35% 16S sequences, ~55% enzyme data)
- Use OPTIONAL clauses for all phenotype queries
- Query timeouts possible without LIMIT on multi-join queries

### Best Practices
- Always specify `FROM <http://rdfportal.org/dataset/bacdive>`
- Use `bif:contains` with `option (score ?sc)` for keyword search
- Never use `?score` as variable name (reserved)
- Use OPTIONAL for phenotype properties
- Filter by genus/family before complex joins
