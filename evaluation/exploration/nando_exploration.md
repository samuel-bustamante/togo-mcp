# NANDO (Nanbyo Data) Exploration Report

## Database Overview
- **Purpose**: Comprehensive ontology for Japanese intractable (rare) diseases maintained by Japanese government
- **Scope**: 2,777 disease classes focusing on designated intractable diseases eligible for government support
- **Key data types**: Disease classes with multilingual labels (English, Japanese kanji, hiragana), notification numbers, MONDO cross-references

## Schema Analysis (from MIE file)

### Main Entity Types
- **owl:Class** - Disease class with trilingual labels and metadata

### Key Properties
- `dct:identifier` - NANDO identifier (e.g., "NANDO:1200010")
- `rdfs:label` - Multilingual labels (@en, @ja, @ja-hira)
- `skos:prefLabel` - Preferred Japanese label
- `nando:hasNotificationNumber` - Government notification number (1-340+)
- `skos:closeMatch` - Cross-references to MONDO
- `rdfs:seeAlso` - External links (KEGG, government docs)
- `dct:source` - Source documentation URLs
- `skos:altLabel` - Alternative names/synonyms
- `rdfs:subClassOf` - Hierarchical parent relationship

### ID Structure
- `NANDO:11xxxxx` - Disease categories
- `NANDO:12xxxxx` - Specific designated diseases  
- `NANDO:22xxxxx` - Additional diseases

## Search Queries Performed

1. **Parkinson search** → Found 3 entries: Parkinson's disease (NANDO:1200010), Rapid-onset dystonia-parkinsonism, MSA Parkinsonian type

2. **Disease categories** → Found 15 categories (Neuromuscular, Metabolic, Cardiovascular, etc.)

3. **Diseases per category** → Neuromuscular leads with 84 diseases

4. **First 10 notification numbers** → Spinal and bulbar muscular atrophy (notif 1), ALS (notif 2), etc.

5. **MONDO cross-reference analysis** → 2,150 diseases with MONDO mappings, 2,341 total relationships

## SPARQL Queries Tested

```sparql
# Query 1: Count MONDO mappings (entity vs relationship counts)
SELECT 
  (COUNT(DISTINCT ?with_mondo) as ?diseases_with_mondo)
  (COUNT(?mondo) as ?total_mondo_refs)
FROM <http://nanbyodata.jp/ontology/nando>
WHERE {
  ?with_mondo a owl:Class ;
              skos:closeMatch ?mondo .
  FILTER(STRSTARTS(STR(?mondo), "http://purl.obolibrary.org/obo/MONDO_"))
}
# Results: 2,150 diseases with MONDO, 2,341 total MONDO references
```

```sparql
# Query 2: Analyze MONDO mapping distribution
SELECT ?mapping_count (COUNT(?disease) as ?num_diseases)
WHERE {
  {
    SELECT ?disease (COUNT(?mondo) as ?mapping_count)
    WHERE {
      ?disease a owl:Class ;
               skos:closeMatch ?mondo .
      FILTER(STRSTARTS(STR(?mondo), "http://purl.obolibrary.org/obo/MONDO_"))
    }
    GROUP BY ?disease
  }
}
GROUP BY ?mapping_count
ORDER BY ?mapping_count
# Results: 1,976 (1 MONDO), 157 (2 MONDO), 17 (3 MONDO)
```

```sparql
# Query 3: Get Parkinson's disease profile
SELECT ?identifier ?en_label ?ja_label ?prefLabel ?notif_num ?mondo_id ?kegg
FROM <http://nanbyodata.jp/ontology/nando>
WHERE {
  nando:1200010 a owl:Class ;
                dct:identifier ?identifier .
  OPTIONAL { nando:1200010 rdfs:label ?en_label . FILTER(LANG(?en_label) = "en") }
  OPTIONAL { nando:1200010 rdfs:label ?ja_label . FILTER(LANG(?ja_label) = "ja") }
  OPTIONAL { nando:1200010 skos:prefLabel ?prefLabel }
  OPTIONAL { nando:1200010 nando:hasNotificationNumber ?notif_num }
  OPTIONAL { nando:1200010 skos:closeMatch ?mondo_id . FILTER(STRSTARTS(...)) }
}
# Results: NANDO:1200010, "Parkinson's disease", "パーキンソン病", notif=6, MONDO:0005180
```

```sparql
# Query 4: List disease categories with counts
SELECT ?category_label (COUNT(DISTINCT ?disease) as ?count)
FROM <http://nanbyodata.jp/ontology/nando>
WHERE {
  ?category rdfs:subClassOf nando:1000001 ;
            rdfs:label ?category_label .
  ?disease rdfs:subClassOf ?category .
  FILTER(LANG(?category_label) = "en")
}
GROUP BY ?category_label
ORDER BY DESC(?count)
# Results: Neuromuscular (84), Metabolic (45), Chromosome (42), etc.
```

## Interesting Findings

### Specific Verifiable Facts
- Parkinson's disease = NANDO:1200010 = notification number 6 = MONDO:0005180
- Huntington's disease = NANDO:1200012 = notification number 8 = MONDO:0007739
- Spinal and bulbar muscular atrophy = NANDO:1200001 = notification number 1
- ALS = NANDO:1200002 = notification number 2 = MONDO:0004976
- 2,454 diseases have notification numbers (88%)

### Disease Categories (15 total)
1. Neuromuscular disease (84) - 神経・筋疾患
2. Metabolic disease (45) - 代謝系疾患
3. Chromosome abnormality (42) - 染色体または遺伝子に変化を伴う症候群
4. Immune system disease (27) - 免疫系疾患
5. Cardiovascular disease (21) - 循環器系疾患

### Multilingual Labels
- All diseases have English, Japanese kanji, and Japanese hiragana labels
- Hiragana labels can be identified with regex: `^[ぁ-ん]+$`

## Cross-Reference Mapping Analysis

### ⚠️ MONDO Mappings (Critical for integration)
- **Entity count**: 2,150 diseases have at least one MONDO mapping
- **Relationship count**: 2,341 total MONDO cross-references
- **Mapping Distribution**:
  - 1,976 diseases → 1 MONDO ID
  - 157 diseases → 2 MONDO IDs  
  - 17 diseases → 3 MONDO IDs
- **Average**: 1.09 MONDO mappings per mapped disease

### External Links
- KEGG Disease: ~500 diseases
- Government documents (MHLW): ~2,397 diseases
- Patient resources (nanbyou.or.jp): Official PDFs

## Question Opportunities by Category

### Precision Questions
- What is the NANDO ID for Parkinson's disease?
- What notification number is assigned to Huntington's disease in NANDO?
- What is the Japanese name (kanji) for ALS in NANDO?
- What MONDO ID maps to NANDO:1200010?

### Completeness Questions
- How many diseases in NANDO have notification numbers?
- How many NANDO diseases have MONDO cross-references? (Entity count: 2,150)
- How many total NANDO→MONDO mapping relationships exist? (Relationship count: 2,341)
- How many diseases in NANDO belong to the Neuromuscular disease category?

### Integration Questions
- Convert NANDO:1200012 (Huntington's disease) to MONDO ID
- Which NANDO diseases map to multiple MONDO IDs?
- Find the KEGG Disease link for Parkinson's disease

### Specificity Questions
- What Japanese rare diseases have notification number 1?
- Which NANDO diseases are in the Metabolic disease category?
- Find diseases with notification numbers 1-10

### Structured Query Questions
- List all neuromuscular diseases with their MONDO mappings
- Find diseases that have both KEGG and MONDO cross-references
- Retrieve diseases with multiple MONDO mappings (one-to-many)

## Notes
- Use `bif:contains` for keyword search (Virtuoso backend)
- Language filtering essential: FILTER(LANG(?label) = "en")
- Hiragana vs kanji: Use regex `^[ぁ-ん]+$` to distinguish
- Notification numbers indicate official government designation order
- Some diseases have multiple MONDO mappings (valid for disease variants)
- Cross-reference to MONDO enables international disease harmonization
- NANDO is the authoritative source for Japanese rare disease policy
