# AMR Portal Exploration Report

## Database Overview
- **Purpose**: Integrates antimicrobial resistance (AMR) surveillance data from NCBI Pathogen Detection, PATRIC, and CABBAGE
- **Key data types**: Phenotypic antimicrobial susceptibility test (AST) results and genotypic AMR features from bacterial isolates
- **Scale**: 1.7M+ phenotypic measurements, 1.1M+ genotypic features, ~1.4M unique biosamples
- **Geographic coverage**: 150+ countries across all continents

## Schema Analysis (from MIE file)

### Main Entity Types
1. **PhenotypeMeasurement**: AST results with resistance phenotype
   - Properties: organism, species, genus, antibioticName, resistancePhenotype
   - Metadata: country, geographicalRegion, collectionYear, isolationSource, host
   - Method info: laboratoryTypingMethod, astStandard, measurementValue/Sign/Units

2. **GenotypeFeature**: AMR gene detections
   - Properties: amrClass, amrSubclass, amrElementSymbol, geneSymbol
   - Location: region, regionStart, regionEnd, strand
   - Evidence: evidenceType, evidenceAccession, evidenceDescription

### Important Relationships
- `amr:bioSample` links phenotype and genotype data from same isolate
- `obo:RO_0002162` links to NCBI Taxonomy
- `dct:references` links to PubMed literature
- `amr:antibioticOntologyId` links to ARO (Antibiotic Resistance Ontology)

### Query Patterns
- Use `bif:contains` for keyword searches on organism names
- Always specify `FROM <http://rdfportal.org/dataset/amrportal>`
- Filter by organism/antibiotic before aggregations to avoid timeouts

## Search Queries Performed

1. **Query**: Top organisms with phenotype data
   - Results: Salmonella enterica (443K), E. coli (364K), M. tuberculosis (331K), K. pneumoniae (133K), N. gonorrhoeae (95K)

2. **Query**: Antibiotic resistance in E. coli
   - Results: Ampicillin most common resistance (7,688), followed by tetracycline (3,524), ciprofloxacin (3,289)

3. **Query**: AMR gene class distribution
   - Results: BETA-LACTAM (243K), AMINOGLYCOSIDE (187K), EFFLUX (180K), TETRACYCLINE (89K), QUINOLONE (80K)

4. **Query**: Geographic distribution of ciprofloxacin-resistant E. coli
   - Results: USA (1,041), UK (790), Norway (313), Vietnam (101), Thailand (91)

5. **Query**: Common beta-lactam resistance genes
   - Results: penA (22K isolates), blaC (21K), bla_1 (19K), bla_2 (18.5K), ampC variants (16K each)

6. **Query**: Laboratory typing methods
   - Results: Broth dilution (959K, 56%), agar dilution (142K), disk diffusion (121K), E-test (34K)

## SPARQL Queries Tested

```sparql
# Query 1: Top organisms by phenotype count
PREFIX amr: <http://example.org/ebiamr#>
SELECT DISTINCT ?organism (COUNT(*) as ?count)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism ?organism .
}
GROUP BY ?organism
ORDER BY DESC(?count)
LIMIT 20
# Results: 20+ species, led by Salmonella (443K), E. coli (364K), M. tuberculosis (331K)
```

```sparql
# Query 2: AMR gene class prevalence
PREFIX amr: <http://example.org/ebiamr#>
SELECT ?amrClass (COUNT(*) as ?geneCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:GenotypeFeature .
  ?s amr:amrClass ?amrClass .
}
GROUP BY ?amrClass
ORDER BY DESC(?geneCount)
LIMIT 20
# Results: BETA-LACTAM (243K), AMINOGLYCOSIDE (187K), EFFLUX (180K)
```

```sparql
# Query 3: Temporal trend of ampicillin resistance in E. coli
PREFIX amr: <http://example.org/ebiamr#>
SELECT ?year (COUNT(*) as ?total) (SUM(?isResistant) as ?resistant)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism "Escherichia coli" .
  ?s amr:antibioticName "ampicillin" .
  ?s amr:collectionYear ?year .
  ?s amr:resistancePhenotype ?phenotype .
  BIND(IF(?phenotype = "resistant", 1, 0) as ?isResistant)
  FILTER(?year >= 2015 && ?year <= 2023)
}
GROUP BY ?year
ORDER BY ?year
# Results: Shows annual variation with 2020 having highest total tests (1,643)
```

```sparql
# Query 4: Geographic distribution of resistant isolates
PREFIX amr: <http://example.org/ebiamr#>
SELECT ?country ?region (COUNT(*) as ?resistantCount)
FROM <http://rdfportal.org/dataset/amrportal>
WHERE {
  ?s a amr:PhenotypeMeasurement .
  ?s amr:organism "Escherichia coli" .
  ?s amr:antibioticName "ciprofloxacin" .
  ?s amr:resistancePhenotype "resistant" .
  ?s amr:country ?country .
  ?s amr:geographicalRegion ?region .
}
GROUP BY ?country ?region
ORDER BY DESC(?resistantCount)
LIMIT 15
# Results: USA (1,041), UK (790), Norway (313), etc.
```

## Interesting Findings

### Specific Entities for Questions
- **Organisms**: Salmonella enterica, Escherichia coli, Mycobacterium tuberculosis, Klebsiella pneumoniae, Neisseria gonorrhoeae
- **Antibiotics**: ampicillin, ciprofloxacin, meropenem, trimethoprim-sulfamethoxazole
- **AMR genes**: penA, blaC, bla_1, ampC, blaZ
- **Gene classes**: BETA-LACTAM, AMINOGLYCOSIDE, EFFLUX, QUINOLONE

### Unique Properties
- Detailed geographic hierarchy (region → subregion → country → ISO code)
- Multiple AST methods tracked (broth dilution, disk diffusion, agar dilution, E-test)
- Quantitative MIC values available (~30% of records)
- Genotype-phenotype linkage via shared bioSample

### Cross-Database Connections
- BioSample (~1.4M samples)
- SRA (sequence data, ~870K accessions)
- INSDC/GenBank assemblies (~890K)
- PubMed literature references
- ARO ontology for antibiotic classification
- NCBI Taxonomy for organism classification

### Verifiable Facts
- Salmonella enterica has 443,249 phenotype measurements (most of any organism)
- 243,389 BETA-LACTAM class gene detections (most common AMR class)
- penA gene found in 22,039 distinct isolates (most common beta-lactam gene)
- Broth dilution is the dominant AST method (959,895 tests, 56%)
- 150+ countries represented with geographic data

## Question Opportunities by Category

### Precision
- "What is the most common AMR gene class detected in the AMR Portal database?" (Answer: BETA-LACTAM)
- "How many phenotype measurements exist for Salmonella enterica?" (Answer: 443,249)
- "What beta-lactam resistance gene is found in the most isolates?" (Answer: penA, 22,039 isolates)

### Completeness
- "How many distinct bacterial species have phenotypic AMR data in AMR Portal?" (Need query: 20+)
- "How many countries have AMR surveillance data?" (Answer: 150+)
- "What are all the AMR gene classes detected in the database?" (List of 20+ classes)

### Integration
- "Link AMR Portal genotype data to NCBI Taxonomy IDs" (via obo:RO_0002162)
- "Find PubMed references associated with AMR surveillance data" (via dct:references)

### Currency
- "What is the most recent collection year for AMR data?" (2023-2024)
- "How has ciprofloxacin resistance in E. coli changed from 2015-2023?"

### Specificity
- "What AMR genes are associated with carbapenem resistance in Klebsiella pneumoniae?"
- "Which countries in Asia have the most fluoroquinolone-resistant E. coli isolates?" (Vietnam, Thailand, Pakistan)

### Structured Query
- "Find isolates with resistance to both meropenem AND imipenem"
- "Find beta-lactam resistance genes in carbapenem-resistant Klebsiella pneumoniae"
- "List organisms with more than 100,000 phenotype measurements"

## Notes

### Limitations
- Large dataset can cause timeouts without proper filtering
- Inconsistent text capitalization in some fields (Stool vs stool)
- Not all biosamples have both phenotype and genotype data (~65% coverage)
- Geographic data incomplete for some records (~80% coverage)

### Best Practices
- Always use `FROM <http://rdfportal.org/dataset/amrportal>` clause
- Filter by organism or antibiotic before aggregations
- Use `LIMIT` clauses for exploratory queries
- Use `bif:contains` for flexible text matching
- Check data existence before complex joins
