# PubMed Exploration Report

## Database Overview
- **Purpose**: Comprehensive biomedical literature database containing bibliographic information from MEDLINE, life science journals, and online books
- **Key data types**: 37+ million citations with article metadata (titles, abstracts, authors, affiliations, journals), MeSH term annotations, publication details
- **Update frequency**: Daily updates
- **License**: Public Domain

## Schema Analysis (from MIE file)

### Main Properties Available
- `bibo:pmid` - PubMed ID (primary identifier)
- `dct:title` - Article title
- `bibo:abstract` - Article abstract (~85% coverage)
- `dct:issued` - Publication date
- `dct:creator` - Author list (ordered via OLO)
- `prism:doi` - DOI (~70% coverage)
- `prism:publicationName` - Journal name
- `bibo:volume`, `bibo:issue` - Volume/issue numbers
- `prism:startingPage`, `prism:endingPage` - Page range
- `fabio:hasSubjectTerm`, `fabio:hasPrimarySubjectTerm` - MeSH annotations
- `rdfs:seeAlso` - Cross-references to MeSH terms

### Important Relationships
- Articles linked to ordered author lists via `dct:creator` → OLO
- MeSH term annotations via `fabio:hasSubjectTerm` and `rdfs:seeAlso`
- Journal metadata via PRISM and FaBIO vocabularies
- Author affiliations via `org:memberOf`

### Query Patterns Observed
- Full-text keyword search using `bif:contains` (essential for performance)
- Date filtering using `STRSTARTS(STR(?issued), "2024")` pattern
- MeSH term filtering via URI patterns `http://id.nlm.nih.gov/mesh/`
- Author traversal via OLO ordered list structure

## Search Queries Performed

### Query 1: BRCA1 breast cancer
- **Search**: `BRCA1 breast cancer`
- **Results**: 16,065 articles
- **Sample PMIDs**: 41530754, 41530261, 41528496...
- **Observation**: Strong biomedical literature coverage for major cancer research topics

### Query 2: COVID-19 vaccine mRNA
- **Search**: `COVID-19 vaccine mRNA`
- **Results**: 11,226 articles
- **Observation**: Comprehensive coverage of pandemic-related research

### Query 3: CRISPR gene editing therapy
- **Search**: `CRISPR gene editing therapy`
- **Results**: 7,747 articles
- **Observation**: Good coverage of cutting-edge gene editing research

### Query 4: Alzheimer amyloid beta
- **Search**: `Alzheimer amyloid beta`
- **Results**: 68,106 articles
- **Observation**: Extensive neurodegenerative disease literature

### Query 5: Microbiome gut brain axis
- **Search**: `microbiome gut brain axis`
- **Results**: 8,098 articles
- **Observation**: Growing research area with substantial literature

### Query 6: Rare disease treatment clinical trial
- **Search**: `rare disease treatment clinical trial`
- **Results**: 9,487 articles
- **Observation**: Good coverage for rare disease research

## SPARQL Queries Tested

### Query 1: Retrieve Complete Article by PMID
```sparql
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX prism: <http://prismstandard.org/namespeces/1.2/basic/>
PREFIX fabio: <http://purl.org/spar/fabio/>

SELECT ?title ?abstract ?doi ?journal ?issued
FROM <http://rdfportal.org/dataset/pubmed>
WHERE {
  ?article bibo:pmid "31558841" ;
           dct:title ?title ;
           bibo:abstract ?abstract ;
           prism:doi ?doi ;
           prism:publicationName ?journal ;
           dct:issued ?issued .
}
```
**Results**: Successfully retrieved full metadata including title "Functional variants in ADH1B and ALDH2 are non-additively associated with all-cause mortality in Japanese population", abstract, DOI 10.1038/s41431-019-0518-y, journal "European journal of human genetics : EJHG", published 2020-03.

### Query 2: Get Authors and Affiliations
```sparql
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX olo: <http://purl.org/ontology/olo/core#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX org: <http://www.w3.org/ns/org#>

SELECT ?pmid ?index ?author_name ?affiliation
FROM <http://rdfportal.org/dataset/pubmed>
WHERE {
  ?article bibo:pmid ?pmid ;
           dct:creator ?creator .
  ?creator olo:slot ?slot .
  ?slot olo:index ?index ;
        olo:item ?author .
  ?author foaf:name ?author_name .
  OPTIONAL { ?author org:memberOf ?affiliation }
  FILTER(?pmid = "31558841")
}
ORDER BY ?index
```
**Results**: Retrieved 8 authors in order: Sakaue S, Akiyama M, Hirata M, Matsuda K, Murakami Y, Kubo M, Kamatani Y, Okada Y - all with institutional affiliations (RIKEN, University of Tokyo, Osaka University, Kyushu University)

### Query 3: Search Articles by Keyword (bif:contains)
```sparql
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?pmid ?title
FROM <http://rdfportal.org/dataset/pubmed>
WHERE {
  ?article bibo:pmid ?pmid ;
           dct:title ?title .
  ?title bif:contains "'cancer' AND 'screening'" .
}
LIMIT 20
```
**Results**: 20 articles about cancer screening retrieved efficiently, spanning colorectal, breast, cervical, lung cancer screening research

### Query 4: Find Articles with MeSH Terms by Keyword
```sparql
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?pmid ?mesh_term
FROM <http://rdfportal.org/dataset/pubmed>
WHERE {
  ?article bibo:pmid ?pmid ;
           dct:title ?title ;
           rdfs:seeAlso ?mesh_term .
  ?title bif:contains "'Alzheimer'" .
  FILTER(STRSTARTS(STR(?mesh_term), "http://id.nlm.nih.gov/mesh/"))
}
LIMIT 20
```
**Results**: Retrieved MeSH term associations for Alzheimer's articles, including D016428 (Alzheimer Disease), D003072 (Cognitive Dysfunction), D000544, etc.

### Query 5: Search COVID-19 Articles from Recent Years
```sparql
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX prism: <http://prismstandard.org/namespeces/1.2/basic/>

SELECT ?pmid ?title ?journal ?issued
FROM <http://rdfportal.org/dataset/pubmed>
WHERE {
  ?article bibo:pmid ?pmid ;
           dct:title ?title ;
           dct:issued ?issued ;
           prism:publicationName ?journal .
  ?title bif:contains "'COVID-19' OR 'SARS-CoV-2'" .
  FILTER(STRSTARTS(STR(?issued), "2024") || STRSTARTS(STR(?issued), "2025"))
}
ORDER BY DESC(?issued)
LIMIT 20
```
**Results**: Retrieved recent COVID-19 articles from journals like Pulmonology, Emerging Microbes & Infections, Annals of Medicine. Note: Some articles show future dates (2025-12-31) for ahead-of-print/in-press articles.

## Tool-based Exploration

### PubMed MCP Tools Tested:
1. **ncbi_esearch**: Effective keyword search with query translation showing MeSH expansion
2. **get_article_metadata**: Full article metadata including authors, affiliations, MeSH terms, DOI
3. **search_articles**: Flexible search with date filtering capability
4. **convert_article_ids**: PMID ↔ PMCID ↔ DOI conversion (31558841 → PMC7028931)
5. **get_full_text_article**: Full text retrieval from PMC for open access articles
6. **find_related_articles**: Similar article discovery via pubmed_pubmed links

## Interesting Findings

### Specific Entities for Questions:
- **PMID 31558841**: ADH1B/ALDH2 alcohol metabolism variant study - good for metadata retrieval questions
- **MeSH D016428**: Alzheimer Disease descriptor - well-indexed in literature
- **MeSH D003920**: Diabetes Mellitus - common disease term
- COVID-19/SARS-CoV-2 articles: Large volume of recent research (11,000+ mRNA vaccine papers)

### Unique Properties/Patterns:
1. **Ordered Author Lists**: Uses OLO (Ordered List Ontology) for author ordering
2. **MeSH Descriptor-Qualifier Pairs**: Format {descriptor}Q{qualifier} (e.g., D009026Q000639)
3. **Date Variability**: Mixed formats (gYearMonth, date, string) - use string comparison
4. **Abstract Coverage**: ~85% of articles have abstracts
5. **DOI Coverage**: ~70% of articles have DOIs

### Connections to Other Databases:
- **MeSH**: Direct linking via rdfs:seeAlso to http://id.nlm.nih.gov/mesh/
- **PMC**: Full text available for ~6M articles via PMCID
- **PubTator Central**: Entity annotations in same SPARQL endpoint (different graph)
- **NLM Catalog**: Journal metadata

### Data Quality Notes:
- Count queries on entire dataset timeout - use LIMIT/sampling
- Use `bif:contains` instead of REGEX for keyword search (much faster)
- Filter by article first before traversing author lists
- Some articles have future publication dates (ahead of print)

## Cross-Reference/Mapping Analysis

⚠️ **Not Applicable**: PubMed's primary cross-references are to MeSH terms (vocabulary terms, not entity mappings in the TogoID sense). The links are:
- **Article → MeSH**: Via rdfs:seeAlso and fabio:hasSubjectTerm (subject indexing, not ID conversion)
- **Article → Journal**: Via journal identifiers (ISSN, NLM ID)
- **Article → PMC**: Via PMCID for full-text availability

## Question Opportunities by Category

### Precision
- "What is the DOI for PubMed article [PMID]?" → Tests specific metadata retrieval
- "Who is the first author of PubMed article [PMID]?" → Tests author list navigation
- "In which journal was PubMed article [PMID] published?" → Tests publication metadata

### Completeness
- "How many PubMed articles have 'CRISPR' in their title?" → Tests keyword search with counting
- "List the MeSH terms assigned to PubMed article [PMID]" → Tests MeSH annotation retrieval
- "How many authors are listed for article [PMID]?" → Tests author enumeration

### Integration
- "What is the PMCID for PubMed article [PMID]?" → Tests ID conversion
- "What MeSH descriptors are assigned to articles about [topic]?" → Tests PubMed-MeSH linking
- "Which PubMed articles cite genes annotated in PubTator Central?" → Tests cross-graph queries

### Currency
- "How many COVID-19 vaccine articles were published in 2024?" → Tests recent literature counts
- "What is the most recent article about [topic]?" → Tests recency queries
- "When was article [PMID] published?" → Tests date retrieval

### Specificity
- "Find PubMed articles about [rare disease name]" → Tests niche topic search
- "What articles in [specific journal] discuss [topic]?" → Tests journal filtering
- "List articles by author [name] in [year]" → Tests specific author search

### Structured Query
- "Find articles published in Nature journals about neuroscience" → Tests journal + keyword filtering
- "List PubMed articles with both gene and disease annotations" → Tests multi-criteria filtering
- "Find articles about Alzheimer's with MeSH term D016428" → Tests keyword + MeSH combination

## Notes

### Limitations/Challenges:
1. **Performance**: Count queries and aggregations timeout without LIMIT
2. **Date Formats**: Inconsistent date representations require string-based filtering
3. **MeSH Queries**: Direct MeSH URI queries can fail; better to search by keyword first
4. **Abstract Availability**: ~15% of articles lack abstracts

### Best Practices:
1. Always use `bif:contains` for keyword search (not REGEX or CONTAINS)
2. Filter by PMID before traversing author relationships
3. Use LIMIT on all exploratory queries
4. For date ranges, use `STRSTARTS(STR(?issued), "2024")` pattern
5. Check for optional abstract before requiring it

### Important Clarifications:
- The PubMed database is for bibliographic metadata, not full-text content
- Full text available for subset via PMC (~6M articles)
- MeSH annotations added/revised post-publication (constantly updated)
