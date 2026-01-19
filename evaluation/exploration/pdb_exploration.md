# Protein Data Bank (PDB) Exploration Report

## Database Overview
- **Purpose**: Repository of 3D structural data for biological macromolecules
- **Scope**: Proteins, nucleic acids (DNA/RNA), and their complexes
- **Scale**: 245,833+ entries (current count from query)
- **Data types**: X-ray crystallography (71%), cryo-EM (6%), NMR (6%), other methods
- **Key features**: Resolution data, R-factors, sequences, experimental methods, cross-references

## Schema Analysis (from MIE file)

### Main Entity Types
- **Datablock**: Root entry for each PDB structure
- **Entity**: Individual molecules (polymer, non-polymer, water, branched)
- **EntityPoly**: Polymer sequence information
- **Refine**: Refinement statistics (resolution, R-factors)
- **Exptl**: Experimental method details
- **StructRef**: Cross-references to sequence databases (UniProt, GenBank)
- **Database2**: External database links (EMDB, BMRB)
- **Citation**: Publication metadata (DOI, PubMed)
- **Cell/Symmetry**: Crystallographic parameters

### Important Properties
- `pdbx:refine.ls_d_res_high`: Resolution (Å)
- `pdbx:refine.ls_R_factor_R_work`: R-work value
- `pdbx:refine.ls_R_factor_R_free`: R-free value
- `pdbx:exptl.method`: Experimental technique
- `pdbx:struct_ref.db_name`: Cross-reference database type
- `pdbx:struct_ref.pdbx_db_accession`: External accession
- `pdbx:struct.title`: Structure title
- `pdbx:struct_keywords.pdbx_keywords`: Classification keywords

### Key Patterns
- Category-based design: datablock → has_*Category → has_* items
- Resolution/R-factor comparisons require `xsd:decimal()` casting
- Keyword searches best on `struct_keywords` field

## Search Queries Performed

1. **Query: "insulin"** → **5,265 structures** including insulin analogs, receptor complexes
2. **Query: "CRISPR Cas9"** → **473 structures** of Cas9 variants and complexes
3. **Query: "ribosome"** → **9,054 structures** including complete ribosomes and subunits
4. **Query: "antibody COVID-19 spike"** → **802 structures** of SARS-CoV-2 antibody complexes
5. **Query: "hemoglobin"** → **1,301 structures** of hemoglobin variants
6. **Query (CC): "heme"** → **25 chemical components** including HEM (protoporphyrin IX)

## SPARQL Queries Tested

### Query 1: Total PDB Entries Count
```sparql
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>

SELECT (COUNT(DISTINCT ?entry) as ?total_entries)
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
}
```
**Results**: 245,833 total entries

### Query 2: Structures by Experimental Method
```sparql
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>

SELECT ?method (COUNT(?entry) as ?count)
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
  ?entry pdbx:has_exptlCategory/pdbx:has_exptl ?exptl .
  ?exptl pdbx:exptl.method ?method .
}
GROUP BY ?method
ORDER BY DESC(?count)
```
**Results**:
| Method | Count |
|--------|-------|
| X-RAY DIFFRACTION | 174,904 |
| ELECTRON MICROSCOPY | 15,032 |
| SOLUTION NMR | 13,902 |
| ELECTRON CRYSTALLOGRAPHY | 226 |
| NEUTRON DIFFRACTION | 212 |
| SOLID-STATE NMR | 162 |

### Query 3: Highest Resolution Structures
```sparql
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?entry_id ?resolution ?r_work
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
  BIND(STRAFTER(str(?entry), "http://rdf.wwpdb.org/pdb/") AS ?entry_id)
  ?entry pdbx:has_refineCategory/pdbx:has_refine ?refine .
  ?refine pdbx:refine.ls_d_res_high ?resolution .
  OPTIONAL { ?refine pdbx:refine.ls_R_factor_R_work ?r_work }
  FILTER(xsd:decimal(?resolution) > 0)
}
ORDER BY xsd:decimal(?resolution)
LIMIT 10
```
**Results**:
| PDB ID | Resolution (Å) | R-work |
|--------|----------------|--------|
| 5D8V | 0.48 | 0.072 |
| 3NIR | 0.48 | 0.127 |
| 1EJG | 0.54 | 0.09 |
| 3P4J | 0.55 | 0.078 |
| 5NW3 | 0.59 | 0.135 |

### Query 4: Highest Resolution Cryo-EM Structures
```sparql
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>

SELECT ?entry_id ?title ?resolution ?method
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
  BIND(STRAFTER(str(?entry), "http://rdf.wwpdb.org/pdb/") AS ?entry_id)
  ?entry pdbx:has_structCategory/pdbx:has_struct ?struct ;
         pdbx:has_refineCategory/pdbx:has_refine ?refine ;
         pdbx:has_exptlCategory/pdbx:has_exptl ?exptl .
  ?struct pdbx:struct.title ?title .
  ?refine pdbx:refine.ls_d_res_high ?resolution .
  ?exptl pdbx:exptl.method ?method .
  FILTER(?method = "ELECTRON MICROSCOPY")
  FILTER(xsd:decimal(?resolution) > 0)
}
ORDER BY xsd:decimal(?resolution)
LIMIT 5
```
**Results**:
| PDB ID | Resolution (Å) | Title |
|--------|----------------|-------|
| 7A4M | 1.22 | Mouse heavy-chain apoferritin |
| 7R5O | 1.60 | Human apoferritin |
| 8A3D | 1.67 | Human ribosome large subunit |

### Query 5: UniProt Cross-Reference Analysis
```sparql
PREFIX pdbx: <http://rdf.wwpdb.org/schema/pdbx-v50.owl#>

SELECT (COUNT(DISTINCT ?entry) as ?entries_with_uniprot) 
       (COUNT(?accession) as ?total_uniprot_refs)
FROM <http://rdfportal.org/dataset/pdbj>
WHERE {
  ?entry a pdbx:datablock .
  ?entry pdbx:has_struct_refCategory/pdbx:has_struct_ref ?ref .
  ?ref pdbx:struct_ref.db_name "UNP" ;
       pdbx:struct_ref.pdbx_db_accession ?accession .
}
```
**Results**: 
- **Entity count**: 189,655 PDB entries have UniProt references
- **Relationship count**: 352,092 total UniProt references
- **Average**: ~1.86 UniProt refs per entry (multi-chain structures)

## Interesting Findings

### Specific Entities for Questions
1. **3NIR**: Crambin at 0.48 Å resolution - world's highest resolution X-ray structure
2. **5D8V**: Also 0.48 Å - tied for highest resolution
3. **7A4M**: 1.22 Å - highest resolution cryo-EM structure (apoferritin)
4. **PHENIX**: Most popular refinement software (72,381 uses)
5. **P 21 21 21**: Most common space group (39,753 structures)

### Unique Properties
- Resolution records: 0.48 Å for X-ray, 1.22 Å for cryo-EM
- Entity types: 418,171 polymers, 367,744 non-polymers, 162,843 waters, 18,329 branched
- Method diversity: 13 different experimental methods recorded

### Connections to Other Databases
- **UniProt**: 189,655 entries (77% of PDB) with cross-references
- **EMDB**: 13,974 entries linked to electron microscopy maps
- **DOI/PubMed**: ~75%/73% have publication references

### Specific, Verifiable Facts
- Total PDB entries: 245,833
- X-ray structures: 174,904
- Cryo-EM structures: 15,032
- NMR structures: 13,902
- Structures with UniProt refs: 189,655
- Total UniProt cross-references: 352,092

## ⚠️ CRITICAL: Cross-Reference/Mapping Analysis

### UniProt Cross-References
1. **Entity Count** (unique PDB entries with UniProt mappings): **189,655**
2. **Relationship Count** (total UniProt reference relationships): **352,092**
3. **Average Mappings**: 1.86 UniProt refs per PDB entry
4. **Why difference**: Multi-chain protein structures have one reference per chain

### EMDB Cross-References
1. **Entity Count** (PDB entries with EMDB links): **13,974**
2. **Relationship Count**: **13,974** (1:1 mapping, no duplicates)

## Question Opportunities by Category

### Precision
- "What is the PDB ID for the highest resolution protein structure?" (3NIR or 5D8V, 0.48 Å)
- "What is the resolution of PDB entry 3NIR?" (0.48 Å)
- "What is the title of PDB entry 3NIR?" (Crystal structure of small protein crambin)
- "What protein is in the highest resolution cryo-EM structure 7A4M?" (apoferritin)

### Completeness
- "How many structures are in the PDB?" (245,833)
- "How many X-ray crystallography structures are in PDB?" (174,904)
- "How many cryo-EM structures are in PDB?" (15,032)
- "How many PDB entries contain insulin structures?" (5,265)
- "How many SARS-CoV-2 antibody structures are in PDB?" (~802)
- "How many PDB entries have UniProt cross-references?" (189,655 entries)

### Integration
- "What is the EMDB ID associated with PDB 7A4M?" (requires query)
- "Which UniProt accessions are linked to PDB entry 16PK?" (P07378)
- "How many PDB entries have both UniProt and EMDB references?"

### Currency
- "What is the current total number of PDB structures?" (245,833+)
- "What recent CRISPR-Cas9 structures were deposited in 2023?" (list)
- "What is the highest resolution cryo-EM structure to date?" (7A4M at 1.22 Å)

### Specificity
- "What is the most common crystallographic space group in PDB?" (P 21 21 21)
- "What is the most used refinement software in PDB?" (PHENIX with 72,381 uses)
- "What is the R-work value for PDB entry 3NIR?" (0.127)

### Structured Query
- "Find PDB structures with resolution better than 1.0 Å"
- "Find cryo-EM structures with resolution better than 2.0 Å"
- "Find kinase structures determined by X-ray with resolution < 2.0 Å from 2023"
- "Find all tetrameric assemblies in PDB"

## Notes

### Limitations
- Year comparisons require `xsd:integer()` casting
- Resolution comparisons require `xsd:decimal()` casting
- NMR structures don't have resolution data
- Some cryo-EM structures lack R-factor data

### Best Practices
- Always include `FROM <http://rdfportal.org/dataset/pdbj>` clause
- Use `?entry a pdbx:datablock` to filter to PDB entries
- Extract entry_id with `STRAFTER(str(?entry), "http://rdf.wwpdb.org/pdb/")`
- Use category path pattern: `has_*Category/has_*`
- Filter numerics with `xsd:decimal()` or `xsd:integer()`

### Important Count Clarifications
- **"PDB entries with UniProt"** = 189,655 (entity count)
- **"Total UniProt references in PDB"** = 352,092 (relationship count)
- Difference due to multi-chain structures having multiple UniProt refs
