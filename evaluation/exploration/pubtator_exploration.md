# PubTator Central RDF Exploration Report

## Database Overview
- **Purpose**: Biomedical entity annotations extracted from PubMed literature using text mining and manual curation
- **Key data types**: Disease and Gene annotations linked to PubMed articles, with annotation counts indicating mention frequency
- **Data sources**: PubTator3 (automated), ClinVar (curated), dbSNP
- **Update frequency**: Regularly updated
- **License**: Public Domain (NCBI)

## Schema Analysis (from MIE file)

### Main Properties Available
- `oa:Annotation` - Web Annotation Ontology base class
- `dcterms:subject` - Entity type ("Disease" or "Gene")
- `oa:hasBody` - External identifier (MeSH for diseases, NCBI Gene for genes)
- `oa:hasTarget` - PubMed article URI
- `pubtator:annotation_count` - Number of mentions in article
- `dcterms:source` - Provenance (PubTator3, ClinVar, dbSNP) - optional (~50% coverage)

### Important Relationships
- **Disease → MeSH**: `oa:hasBody` → `http://identifiers.org/mesh/D{id}`
- **Gene → NCBI Gene**: `oa:hasBody` → `http://identifiers.org/ncbigene/{id}`
- **Annotation → PubMed**: `oa:hasTarget` → `http://rdf.ncbi.nlm.nih.gov/pubmed/{pmid}`

### Entity Types
- **Disease**: Linked to MeSH vocabulary (D-prefix descriptors)
- **Gene**: Linked to NCBI Gene identifiers
- Note: Other entity types (Chemical, Species, Mutation) have limited or no coverage

### Query Patterns Observed
- Filter by `dcterms:subject` for entity type ("Disease" or "Gene")
- Use identifiers.org namespace for external IDs
- Cross-graph queries with PubMed graph for article metadata
- Gene-disease co-occurrence queries for association discovery

## Search Queries Performed

### Query 1: Diseases in Specific Article (PMID 18935173)
- **Query**: Diseases annotated in PubMed article 18935173
- **Results**: 3 disease annotations
  - D001724 (Birth Weight)
  - D001835 (Body Weight)
  - D003920 (Diabetes Mellitus)
- **Observation**: Multiple disease concepts extracted per article

### Query 2: Gene Identifiers Sample
- **Query**: Sample of gene annotations
- **Results**: 30 distinct NCBI Gene IDs retrieved, including:
  - 11820, 12359, 1233, 20299, 207, 2185, 21943, 25819, 5594, 6367...
- **Observation**: Broad gene coverage across literature

### Query 3: Diabetes Mellitus (D003920) Articles
- **Query**: Articles mentioning Diabetes Mellitus
- **Results**: 20 articles with D003920 annotation
- **Observation**: Disease-article associations enable disease-centric literature retrieval

### Query 4: Gene-Disease Co-occurrences
- **Query**: Articles with both gene AND disease annotations
- **Results**: Multiple co-occurrence pairs found:
  - PMID 16821116: Genes 11820, 12359 + Diseases D000544, D003072
  - PMID 16821125: 9 genes + 4 diseases (D001847, D001859, D008175)
- **Observation**: Enables gene-disease association network construction

### Query 5: High Annotation Count Diseases
- **Query**: Disease annotations mentioned >2 times in articles
- **Results**: 30 annotations with count=3:
  - Various disease terms (D010195, D007022, D004415, etc.)
  - Articles where diseases are prominently discussed
- **Observation**: Annotation count indicates entity prominence in article

### Query 6: Cancer Articles with Disease Annotations
- **Query**: Cross-graph query integrating PubTator + PubMed for cancer articles
- **Results**: 20 disease annotations from cancer-related articles:
  - Colorectal cancer (D015179), Breast neoplasms (D001943), Lung neoplasms (D008175)
  - Cross-database integration works well
- **Observation**: Effective integration with PubMed for keyword-based filtering

## SPARQL Queries Tested

### Query 1: Find Diseases in Specific Article
```sparql
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?disease ?diseaseId
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?disease a oa:Annotation ;
           dcterms:subject "Disease" ;
           oa:hasBody ?diseaseId ;
           oa:hasTarget <http://rdf.ncbi.nlm.nih.gov/pubmed/18935173> .
}
```
**Results**: 3 disease annotations (MeSH D001724, D001835, D003920) successfully retrieved.

### Query 2: List Gene Annotations
```sparql
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?geneId
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?ann a oa:Annotation ;
       dcterms:subject "Gene" ;
       oa:hasBody ?geneId .
}
LIMIT 30
```
**Results**: 30 distinct NCBI Gene identifiers retrieved, demonstrating gene annotation coverage.

### Query 3: Find Articles for Specific Disease (D003920)
```sparql
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?ann ?target
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?ann a oa:Annotation ;
       dcterms:subject "Disease" ;
       oa:hasBody <http://identifiers.org/mesh/D003920> ;
       oa:hasTarget ?target .
}
LIMIT 20
```
**Results**: 20 PubMed articles annotated with Diabetes Mellitus (D003920).

### Query 4: Gene-Disease Co-occurrence Discovery
```sparql
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT DISTINCT ?article ?geneId ?diseaseId
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?geneAnn a oa:Annotation ;
           dcterms:subject "Gene" ;
           oa:hasBody ?geneId ;
           oa:hasTarget ?article .
  ?diseaseAnn a oa:Annotation ;
              dcterms:subject "Disease" ;
              oa:hasBody ?diseaseId ;
              oa:hasTarget ?article .
}
LIMIT 30
```
**Results**: 30 gene-disease co-occurrence pairs across articles, enabling association analysis.

### Query 5: Annotations with Multiple Mentions
```sparql
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX pubtator: <http://purl.jp/bio/10/pubtator-central/ontology#>

SELECT ?ann ?diseaseId ?target ?count
FROM <http://rdfportal.org/dataset/pubtator_central>
WHERE {
  ?ann a oa:Annotation ;
       dcterms:subject "Disease" ;
       oa:hasBody ?diseaseId ;
       oa:hasTarget ?target ;
       pubtator:annotation_count ?count .
  FILTER(?count > 2)
}
LIMIT 30
```
**Results**: 30 disease annotations with count=3, indicating entities mentioned multiple times.

### Query 6: Cross-Graph Integration with PubMed
```sparql
PREFIX oa: <http://www.w3.org/ns/oa#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?ann ?diseaseId ?article ?title
FROM <http://rdfportal.org/dataset/pubtator_central>
FROM <http://rdfportal.org/dataset/pubmed>
WHERE {
  ?ann a oa:Annotation ;
       dcterms:subject "Disease" ;
       oa:hasBody ?diseaseId ;
       oa:hasTarget ?article .
  ?article bibo:pmid ?pmid ;
           dct:title ?title .
  ?title bif:contains "'cancer'" .
}
LIMIT 20
```
**Results**: Successfully retrieved disease annotations from cancer-related articles with titles.

## Interesting Findings

### Specific Entities for Questions:
- **Disease D003920**: Diabetes Mellitus - commonly annotated disease
- **Disease D000544**: Alzheimer Disease - well-represented in annotations
- **Gene 7157**: TP53 (known from other explorations) - gene annotation candidate
- **PMID 16821116**: Article with multiple gene-disease co-occurrences

### Unique Properties/Patterns:
1. **Web Annotation Ontology**: Uses standard oa: namespace for annotation modeling
2. **identifiers.org URIs**: Standardized external database links
3. **Annotation Count**: pubtator:annotation_count tracks entity prominence
4. **Provenance**: dcterms:source indicates data origin (PubTator3, ClinVar, dbSNP)

### Connections to Other Databases:
- **PubMed**: Direct integration via same SPARQL endpoint (different graphs)
- **MeSH**: Disease identifiers link to MeSH vocabulary
- **NCBI Gene**: Gene identifiers link to NCBI Gene database
- **ClinVar/dbSNP**: Curated annotations from variant databases

### Data Quality Notes:
- Provenance (dcterms:source) available for ~50% of annotations
- Gene annotations less frequent than disease annotations
- Annotation count typically 1-3, occasionally higher
- Entity types limited to Disease and Gene

## Cross-Reference/Mapping Analysis

### Entity-to-Database Mapping
PubTator Central provides entity-article linkage rather than database-to-database mapping:

1. **Disease Entities → MeSH**
   - All disease annotations use MeSH identifiers
   - Format: `http://identifiers.org/mesh/D{descriptor_id}`
   - Example: D003920 = Diabetes Mellitus

2. **Gene Entities → NCBI Gene**
   - All gene annotations use NCBI Gene identifiers
   - Format: `http://identifiers.org/ncbigene/{gene_id}`
   - Example: 11820, 12359, etc.

3. **Annotations → PubMed**
   - All annotations target PubMed article URIs
   - Format: `http://rdf.ncbi.nlm.nih.gov/pubmed/{pmid}`

### Cardinality Notes:
- **Many-to-Many**: Articles have multiple entity annotations; entities appear in multiple articles
- **Annotation Counts**: Track within-article mention frequency (not cross-article)
- **Co-occurrence**: Gene-disease pairs co-occurring in same article enable association discovery

## Question Opportunities by Category

### Precision
- "What is the MeSH identifier for diseases annotated in PubMed article [PMID]?"
- "How many times is [disease] mentioned in article [PMID]?" (annotation_count)
- "What is the entity type (Disease/Gene) for PubTator annotation [ID]?"

### Completeness
- "How many disease annotations are associated with PubMed article [PMID]?"
- "List all NCBI Gene IDs annotated with [disease MeSH ID]"
- "How many articles mention [specific gene ID]?"

### Integration
- "Which genes co-occur with Alzheimer Disease (D000544) in literature?"
- "Find articles where both [gene] and [disease] are annotated"
- "What MeSH diseases are annotated in cancer-related PubMed articles?"

### Currency
- "What are the most recently annotated articles mentioning [disease]?"
- Note: PubTator data is regularly updated with new annotations

### Specificity
- "Find articles annotated with rare disease [MeSH ID]"
- "Which genes are specifically associated with [niche disease] in literature?"
- "What disease annotations have high annotation counts (>3 mentions)?"

### Structured Query
- "Find gene-disease co-occurrences where annotation count > 2"
- "List articles with both specific gene AND disease annotations"
- "Find disease annotations in articles containing specific keywords (cross-graph)"

## Notes

### Limitations/Challenges:
1. **Entity Type Coverage**: Only Disease and Gene types well-represented
2. **Provenance Gaps**: ~50% of annotations lack source attribution
3. **Aggregation Performance**: Large aggregations require LIMIT to avoid timeout
4. **Cross-Database Queries**: Complex joins with PubMed can be slow

### Best Practices:
1. Always filter by `dcterms:subject` for specific entity types
2. Use LIMIT for exploratory queries
3. Use identifiers.org format for external IDs
4. Cross-graph queries work well but need selective filters
5. Use OPTIONAL for dcterms:source (not always present)

### Important Clarifications:
- PubTator Central provides text-mined entity mentions, not assertions
- Co-occurrence ≠ biological relationship (just co-mentioned in text)
- Annotation count is within-article frequency, not corpus-wide
- Database focuses on Disease and Gene entities primarily
