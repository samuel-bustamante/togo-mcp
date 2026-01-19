# MediaDive Exploration Report

## Database Overview
- **Purpose**: Comprehensive culture media database from DSMZ (German Collection of Microorganisms and Cell Cultures)
- **Scope**: Standardized recipes for cultivating bacteria, archaea, fungi, yeast, microalgae, and phages
- **Key data types**: Culture media (3,289), Ingredients (1,489), Strains (45,685), Growth conditions

## Schema Analysis (from MIE file)

### Main Entities
1. **CultureMedium** - Media recipes with pH ranges and complexity classification
2. **Ingredient** - Chemical components with cross-references (ChEBI, KEGG, CAS, PubChem)
3. **Strain** - Microbial strains with DSM numbers and species information
4. **GrowthCondition** - Temperature, pH, oxygen requirements for cultivation
5. **MediumComposition** - Links media to ingredients with concentrations
6. **SolutionRecipe** - Hierarchical recipe structure

### Key Properties
- `schema:hasFinalPH`, `schema:hasMinPH`, `schema:hasMaxPH` - pH specifications
- `schema:growthTemperature` - Integer temperature in °C
- `schema:hasOxygenRequirement` - "aerobic"/"anaerobic"
- `schema:belongsTaxGroup` - Taxonomic classification
- `schema:gramsPerLiter` - Concentration units

### Cross-References
- ChEBI: 687 ingredients (46%)
- CAS: 872 ingredients (59%)
- PubChem: 616 ingredients (41%)
- KEGG: 285 ingredients (19%)
- GMO: 870 ingredients (58%)
- BacDive: 33,226 strains (73%)

## Search Queries Performed

1. **Marine media search** → Found 20+ marine media (e.g., "BACTO MARINE BROTH", "MARINE AGAR", "MARINE THERMOCOCCUS MEDIUM")

2. **Anaerobic media search** → Found media for anaerobic cultivation

3. **Taxonomic group analysis** → Distribution across 12 groups:
   - Bacterium: 32,662 strains
   - Fungus: 5,079 strains
   - Yeast: 3,125 strains
   - Microalgae: 1,289 strains
   - Archaeon: 952 strains
   - Phage: 602 strains

4. **Ingredient cross-reference search** → Many ingredients linked to ChEBI/KEGG (e.g., glucose, amino acids, vitamins)

5. **pH filtering** → Found extreme pH media from 0.8 to 11.5

## SPARQL Queries Tested

```sparql
# Query 1: Find hyperthermophilic growth conditions (>70°C)
PREFIX schema: <https://purl.dsmz.de/schema/>
SELECT ?strain ?species ?temp ?mediumLabel
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?growth schema:growthTemperature ?temp ;
          schema:relatedToStrain ?strain ;
          schema:partOfMedium ?medium .
  ?strain schema:hasSpecies ?species .
  ?medium rdfs:label ?mediumLabel .
  FILTER(?temp > 70)
}
ORDER BY DESC(?temp)
LIMIT 20
# Results: Pyrolobus fumarii at 103°C, Pyrococcus kukulkanii at 100°C, Hyperthermus butylicus at 99°C
```

```sparql
# Query 2: Get medium composition with concentrations
PREFIX schema: <https://purl.dsmz.de/schema/>
SELECT ?ingredientLabel ?gPerL ?formula
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?composition schema:partOfMedium <https://purl.dsmz.de/mediadive/medium/1118> ;
               schema:containsIngredient ?ingredient ;
               schema:gramsPerLiter ?gPerL .
  ?ingredient rdfs:label ?ingredientLabel .
  OPTIONAL { ?ingredient schema:hasFormula ?formula }
}
ORDER BY DESC(?gPerL)
# Results: Casitone (3.0 g/L), MgSO4 (2.0 g/L), trace elements (µg/L levels)
```

```sparql
# Query 3: Find psychrophilic organisms (cold-loving)
PREFIX schema: <https://purl.dsmz.de/schema/>
SELECT ?strain ?species ?temp ?mediumLabel
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?growth schema:growthTemperature ?temp ;
          schema:relatedToStrain ?strain ;
          schema:partOfMedium ?medium .
  ?strain schema:hasSpecies ?species .
  ?medium rdfs:label ?mediumLabel .
  FILTER(?temp <= 10)
}
ORDER BY ?temp
# Results: Neisseria zalophi at 0°C, Streptosporangium carneum at 2°C, various Antarctic bacteria at 4°C
```

```sparql
# Query 4: Find extreme pH media
PREFIX schema: <https://purl.dsmz.de/schema/>
SELECT ?medium ?label ?minPH ?maxPH
FROM <http://rdfportal.org/dataset/mediadive>
WHERE {
  ?medium a schema:CultureMedium ; rdfs:label ?label .
  { ?medium schema:hasMinPH ?minPH . FILTER(?minPH < 4) }
  UNION
  { ?medium schema:hasMaxPH ?maxPH . FILTER(?maxPH > 10) }
}
# Results: ACIDIANUS SP. JP7 MEDIUM (pH 0.8), MJ/YTCT MEDIUM (pH 11.5)
```

## Interesting Findings

### Extremophile Cultivation Data
- **Hyperthermophiles**: Pyrolobus fumarii grows at 103°C - highest recorded temperature
- **Psychrophiles**: Neisseria zalophi grows at 0°C
- **Acidophiles**: ACIDIANUS SP. JP7 MEDIUM at pH 0.8
- **Alkaliphiles**: MJ/YTCT MEDIUM at pH 11.5

### Specific Verifiable Facts
- DSM strain 5869 (Pyrolobus fumarii) requires 103°C cultivation temperature
- Medium 1118 (MD1-MEDIUM) contains 13 ingredients including trace elements
- 33,226 strains (73%) have BacDive database links
- 602 phage strains are catalogued

### Taxonomic Distribution
- 12 distinct taxonomic groups covered
- Bacteria dominate (71%), followed by fungi (11%)
- Archaea represent 2% but include most extremophiles

### Cross-Database Integration
- BacDive links enable phenotypic data integration
- ChEBI/KEGG links enable metabolic pathway context
- GMO links provide standardized vocabulary

## Question Opportunities by Category

### Precision Questions
- What is the optimal growth temperature for Pyrolobus fumarii (DSM 5869)?
- What is the ChEBI ID for glucose in MediaDive?
- What pH range is specified for ACIDIANUS BRIERLEYI MEDIUM (medium/150)?

### Completeness Questions
- How many culture media recipes are in MediaDive?
- How many strains in MediaDive belong to the Archaeon taxonomic group?
- How many ingredients have ChEBI cross-references?

### Integration Questions
- Which MediaDive ingredients link to ChEBI ID 17234 (glucose)?
- What is the BacDive ID for DSM strain 5869?
- Find MediaDive strains that have both BacDive and DSM identifiers

### Specificity Questions
- What organisms in MediaDive can grow above 100°C?
- Which media are designed for cultivation below pH 2?
- What media support phage propagation?

### Structured Query Questions
- List ingredients in PYROCOCCUS MEDIUM with their concentrations
- Find all media supporting thermophilic (>50°C) anaerobic growth
- Which archaeal strains have growth data in MediaDive?

## Cross-Reference Mapping Analysis

### BacDive Mappings
- **Entity count**: 33,226 strains have BacDive IDs (73% of 45,685)
- **Relationship count**: Same (1:1 mapping)
- One-to-one mapping confirmed

### Chemical Cross-References
- **Ingredients with any cross-ref**: ~90%
- **Coverage varies**: ChEBI 46%, CAS 59%, GMO 58%
- Some ingredients have multiple database links

## Notes
- Use `bif:contains` for keyword searches (Virtuoso backend)
- pH can be string ("7.0-7.2") or numeric (hasMinPH/hasMaxPH)
- Growth conditions link strains to media via separate entities
- Hierarchical recipe structure: medium → solution → solution_recipe → ingredient
- Excellent for questions about extremophile cultivation
- Good integration with BacDive for expanded phenotypic data
