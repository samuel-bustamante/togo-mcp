# TogoMCP Evaluation Questions Summary

## Overview
- **Total Questions**: 120
- **Files**: Q01.json through Q10.json (12 questions each)
- **Categories**: 6 categories × 20 questions each = 120 total
- **Created**: January 15, 2026
- **Revised**: January 15, 2026 (redundancy fixes applied)

## Redundancy Fixes Applied

The following changes were made to reduce redundancy:

| Original Question | Issue | Replacement |
|-------------------|-------|-------------|
| Q18: Ensembl→NCBI Gene for BRCA1 | BRCA1 overrepresented (7 questions) | Mouse annexin A1 gene ID conversion |
| Q50: BRCA1 chromosome location | BRCA1 overrepresented | TP53 Ensembl gene ID |
| Q56: SARS-CoV-2 pathway ID | Same info in Q8 | Autophagy pathway ID |
| Q65: BRCA1 HGNC ID | BRCA1 overrepresented | BRCA2 NCBI Gene ID conversion |
| Q103: Reactome human pathway count | Same info in Q28 | Ribosome structures in PDB |
| Q21: Pyrococcus temperature | Overlaps with Q95 | Pyrolobus fumarii temperature |

## Distribution by Category

Each file contains exactly 2 questions from each category:

| Category | Questions per File | Total Questions |
|----------|-------------------|-----------------|
| Precision | 2 | 20 |
| Completeness | 2 | 20 |
| Integration | 2 | 20 |
| Currency | 2 | 20 |
| Specificity | 2 | 20 |
| Structured Query | 2 | 20 |

## Database Coverage

### Primary Databases Used (Post-Redundancy Fix)
| Database | Questions | Key Topics |
|----------|-----------|------------|
| UniProt | 8 | Protein IDs, mass, cross-refs, reviewed count |
| PubChem | 8 | Compound IDs, molecular properties, FDA drugs, bioassays |
| PDB | 8 | Structures, resolution, methods, cross-refs, ribosome |
| GO | 6 | Ontology terms, descendants, hierarchy, namespaces |
| ChEMBL | 7 | Drug IDs, targets, bioactivities, phases |
| ClinVar | 6 | Variants, significance, submitters |
| MeSH | 6 | Descriptors, categories, tree numbers |
| NCBI Gene | 6 | Gene IDs, locations, types |
| Ensembl | 5 | Gene IDs (BRCA1, TP53, BRCA2), transcripts, coordinates |
| MONDO | 6 | Disease ontology, cross-refs |
| NANDO | 6 | Japanese rare diseases, mappings |
| Taxonomy | 5 | Taxa, species, lineage |
| Reactome | 5 | Pathways, autophagy, species |
| Rhea | 5 | Reactions, EC numbers, transport |
| ChEBI | 5 | Chemical entities, formulas, mass |
| BacDive | 5 | Bacterial strains, temperature (Pyrolobus), Gram stain |
| MediaDive | 4 | Culture media, pH, extremophiles |
| GlyCosmos | 5 | Glycoepitopes, glycoproteins, glycogenes |
| MedGen | 4 | Clinical concepts, CUI, cross-refs |
| AMR Portal | 4 | Resistance genes, methods, organisms |
| DDBJ | 4 | Sequences, locus tags, BioProject |
| PubMed | 3 | Literature, COVID-19 research |

## Gene Coverage (Post-Redundancy Fix)

To ensure diversity, gene-related questions now cover:
- **BRCA1**: 4 questions (reduced from 7)
- **BRCA2**: 1 question (new)
- **TP53**: 2 questions
- **INS (insulin)**: 2 questions
- **Cas9**: 2 questions
- **Annexin A1 (mouse)**: 1 question (new)
- **clpX (bacterial)**: 2 questions

## Entity vs. Relationship Count Clarification

Several questions involve cross-reference mappings. The questions and notes clearly specify:

- **Entity Count**: Unique entities that HAVE at least one mapping (COUNT DISTINCT)
- **Relationship Count**: Total number of mapping relationships (may be higher due to 1:N mappings)

Examples:
- Q63: NANDO diseases with MONDO mappings = 2,150 (entity count)
- Q54: PDB entries with UniProt refs = 189,655 (entity count), not 352,092 (relationship count)
- Q84: MONDO diseases with OMIM = 9,944 (entity count), not 10,039 (relationship count)

## Files

```
questions/
├── Q01.json  (ID 1-12)
├── Q02.json  (ID 13-24) - Updated: Q18, Q21
├── Q03.json  (ID 25-36)
├── Q04.json  (ID 37-48)
├── Q05.json  (ID 49-60) - Updated: Q50, Q56
├── Q06.json  (ID 61-72) - Updated: Q65
├── Q07.json  (ID 73-84)
├── Q08.json  (ID 85-96)
├── Q09.json  (ID 97-108) - Updated: Q103
├── Q10.json  (ID 109-120)
└── SUMMARY.md
```

## Validation Checklist

✅ All files are valid JSON arrays
✅ Each file has exactly 12 questions
✅ Each file has exactly 2 questions per category
✅ Sequential IDs from 1-120
✅ All required fields present (id, category, question, expected_answer, notes)
✅ Biological relevance verified
✅ No duplicate questions
✅ Redundancy reduced (BRCA1 from 7→4 questions)
✅ All 22 databases represented

---

**Generated**: January 15, 2026
**Source**: Database exploration reports in `/evaluation/exploration/`
**Redundancy Check**: Completed January 15, 2026
