# Database Exploration Summary

## Overview
- **Total databases explored**: 22
- **Total exploration sessions**: 3 (plus verification session)
- **All databases have exploration reports** ✅

## All Explored Databases

| # | Database | Description | Key Entities |
|---|----------|-------------|--------------|
| 1 | amrportal | Antimicrobial resistance surveillance | Bacterial isolates, MIC values, AMR genes |
| 2 | bacdive | Bacterial/archaeal strain information | 97K+ strains, culture conditions |
| 3 | chebi | Chemical entities of biological interest | 217K+ compounds, molecular properties |
| 4 | chembl | Bioactive molecules with drug properties | 2.4M compounds, 20M bioactivities |
| 5 | clinvar | Genomic variants and clinical significance | 3.5M+ variants, pathogenicity |
| 6 | ddbj | Nucleotide sequence data (INSDC) | Sequences, genomic annotations |
| 7 | ensembl | Genome annotations for 100+ species | 87K human genes, transcripts |
| 8 | glycosmos | Glycoscience portal | 117K glycans, 153K glycoproteins |
| 9 | go | Gene Ontology | 48K terms across 3 domains |
| 10 | medgen | Medical genetics concepts | 234K clinical concepts |
| 11 | mediadive | Microbial culture media recipes | 3,289 media, 1,489 ingredients |
| 12 | mesh | Medical Subject Headings | 30K descriptors, 250K chemicals |
| 13 | mondo | Disease ontology | 30K+ disease classes |
| 14 | nando | Japanese rare diseases | 2,777 intractable diseases |
| 15 | ncbigene | Gene database | 57M+ gene entries |
| 16 | pdb | Protein 3D structures | 204K+ structures |
| 17 | pubchem | Chemical molecules | 119M compounds, 1.7M bioassays |
| 18 | pubmed | Biomedical literature | 37M+ citations |
| 19 | pubtator | Entity annotations from literature | Disease/Gene text mining |
| 20 | reactome | Biological pathways | 22K+ pathways, 30+ species |
| 21 | rhea | Biochemical reactions | 17K reactions, ChEBI-linked |
| 22 | taxonomy | NCBI taxonomic classification | 3M+ organisms |
| 23 | uniprot | Protein sequences and functions | 444M proteins (923K curated) |

## Database Coverage Plan for 120 Questions

### Recommended Distribution

| Database | Questions | Rationale |
|----------|-----------|-----------|
| uniprot | 12-15 | Rich content, essential protein database, many cross-refs |
| pubchem | 8-10 | Large chemical database, good search tools |
| pubmed | 8-10 | Literature database, metadata retrieval |
| go | 8-10 | Ontology hierarchy, descendant queries |
| chembl | 8-10 | Bioactivity data, drug discovery focus |
| pdb | 6-8 | Structural data, resolution metrics |
| clinvar | 6-8 | Clinical variants, medical genetics |
| mesh | 6-8 | Medical vocabulary, descriptor lookups |
| ncbigene | 5-7 | Gene database, cross-species coverage |
| ensembl | 5-7 | Genome annotations, multi-species |
| mondo | 5-6 | Disease ontology, rare disease integration |
| nando | 5-6 | Japanese rare diseases, specificity |
| taxonomy | 4-5 | Organism classification |
| chebi | 4-5 | Chemical ontology, biological roles |
| reactome | 4-5 | Pathway database |
| rhea | 4-5 | Biochemical reactions |
| bacdive | 3-4 | Bacterial strains, culture conditions |
| mediadive | 3-4 | Culture media recipes |
| glycosmos | 3-4 | Glycoscience specialization |
| medgen | 3-4 | Medical genetics concepts |
| pubtator | 3-4 | Entity annotations, co-occurrence |
| ddbj | 2-3 | Nucleotide sequences |
| amrportal | 2-3 | AMR surveillance data |

**Total: ~120 questions**

### Distribution by Category (Target: 20 per category)

| Category | Primary Databases | Question Types |
|----------|-------------------|----------------|
| **Precision** | UniProt, PubChem, PDB, MeSH | ID lookups, exact values, sequences |
| **Completeness** | GO, ClinVar, NCBI Gene, BacDive | Counts, hierarchies, complete lists |
| **Integration** | UniProt↔Gene, PubChem↔ChEBI, TogoID | ID conversions, cross-database links |
| **Currency** | ClinVar, PDB, Reactome, PubMed | Recent data, updated classifications |
| **Specificity** | NANDO, BacDive, MediaDive, MeSH | Rare diseases, niche organisms |
| **Structured Query** | ChEMBL, GO, Rhea, UniProt | Complex filters, multi-criteria |

## Cross-Database Integration Opportunities

### High-Value ID Conversion Pairs (TogoID)
1. **UniProt ↔ NCBI Gene** - Protein-gene mapping
2. **PubChem ↔ ChEBI** - Chemical compound linking
3. **ChEMBL ↔ UniProt** - Drug target relationships
4. **ClinVar ↔ MedGen** - Variant-disease connections
5. **Ensembl ↔ NCBI Gene** - Gene ID conversion
6. **MONDO ↔ NANDO** - Disease ontology mapping

### Cross-Graph Query Opportunities
1. **PubMed + PubTator** - Literature with entity annotations
2. **UniProt + PDB** - Protein sequences with structures
3. **ChEMBL + PubChem** - Bioactivity with compound data
4. **Reactome + UniProt** - Pathways with protein details

### Multi-Database Question Ideas
- "What is the NCBI Gene ID for UniProt protein [ID]?"
- "Which PubMed articles mention gene [ID] AND disease [MeSH]?"
- "Find MONDO disease mapped to NANDO rare disease [ID]"
- "What ChEBI compound corresponds to PubChem CID [ID]?"

## Database Characteristics

### Rich Content (Good for Multiple Questions)
- **UniProt**: 444M proteins, extensive cross-references, curated annotations
- **PubChem**: 119M compounds, molecular properties, bioassays
- **PubMed**: 37M citations, MeSH annotations, author metadata
- **ChEMBL**: 2.4M compounds, 20M bioactivities, drug-target relations
- **GO**: 48K terms, hierarchical structure, annotation counts

### Specialized Content (Good for Specificity Questions)
- **NANDO**: Japanese rare diseases (2,777 intractable diseases)
- **BacDive**: Bacterial strains with phenotypic data
- **MediaDive**: Culture media recipes (3,289 formulations)
- **GlyCosmos**: Glycoscience (glycans, glycoproteins, lectins)
- **AMRPortal**: Antimicrobial resistance surveillance

### Well-Connected (Good for Integration Questions)
- **UniProt**: Links to 200+ databases
- **ChEMBL**: UniProt, PDB, PubChem, DrugBank connections
- **ClinVar**: MedGen, OMIM, MeSH integration
- **Ensembl**: NCBI Gene, UniProt, HGNC cross-refs
- **PubMed**: MeSH annotations, PMC full-text

### Ontology/Hierarchy Databases (Good for Completeness Questions)
- **GO**: Biological process, molecular function, cellular component
- **MONDO**: Disease classification hierarchy
- **ChEBI**: Chemical entity classification
- **Taxonomy**: Organism classification tree
- **MeSH**: Medical vocabulary hierarchy

## Recommendations

### High-Priority Question Sources
1. **UniProt** - Most versatile, rich metadata, extensive cross-refs
2. **GO** - Excellent for hierarchy/descendant questions
3. **ChEMBL** - Strong for bioactivity/drug discovery questions
4. **NANDO/MONDO** - Good for rare disease specificity
5. **PubMed/PubTator** - Unique literature-based questions

### Question Design Tips
1. Use specific IDs (verified during exploration) for precision questions
2. Leverage TogoID for integration questions (verified routes)
3. Use rare/niche entities from specialized databases for specificity
4. Test SPARQL queries before creating questions
5. Document expected answers from exploration findings

### Databases That Pair Well
- **NANDO + MONDO**: Disease ontology integration
- **ChEMBL + UniProt**: Drug-target relationships
- **PubMed + PubTator**: Literature with entity extraction
- **BacDive + MediaDive**: Organism + culture conditions
- **ClinVar + MedGen**: Variants + clinical concepts

### Particularly Interesting Findings
1. **NANDO**: Unique Japanese rare disease coverage not elsewhere
2. **MediaDive**: Detailed culture recipes for microbiologists
3. **PubTator**: Gene-disease co-occurrence enables association discovery
4. **AMRPortal**: Antimicrobial resistance surveillance with genotype-phenotype
5. **GlyCosmos**: Specialized glycoscience with 100+ named graphs

## Technical Patterns Across Databases

### Common Query Patterns
- `bif:contains` for keyword search (all Virtuoso endpoints)
- `rdfs:seeAlso` for cross-references
- `rdfs:subClassOf` for ontology hierarchies
- `identifiers.org` namespace for standardized IDs
- FALDO ontology for genomic coordinates

### Performance Considerations
- Always use LIMIT on exploratory queries
- Filter specific entities before traversing relationships
- Use indexed keyword search (bif:contains) not REGEX
- Avoid COUNT on entire large datasets
- Use species/taxonomy filters for multi-species databases

### ID Format Patterns
- UniProt: 6-10 alphanumeric (P38398, Q99ZW2)
- PubChem CID: Numeric (2244, 5291)
- MeSH: D{6digits} for descriptors, C{6digits} for chemicals
- GO: GO:{7digits} (GO:0006914)
- NCBI Gene: Numeric (7157, 672)
- PDB: 4 alphanumeric (1A00, 2HHB)

---

**Last Updated**: January 15, 2026
**All 22 databases explored and documented**
**Ready for question generation phase (PROMPT 2)**
