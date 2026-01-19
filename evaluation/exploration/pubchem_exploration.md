# PubChem RDF Exploration Report

## Database Overview
- **Purpose**: Comprehensive public database of chemical molecules and biological activities
- **Scope**: Small molecules, drugs, bioassays, genes, proteins, pathways
- **Scale**: 119M+ compounds, 339M substances, 1.7M bioassays, 167K genes, 249K proteins, 81K pathways
- **Key features**: Molecular descriptors, FDA drug classification, ontology integration, patent links

## Schema Analysis (from MIE file)

### Main Entity Types
- **Compound**: Chemical entities with molecular descriptors
- **Substance**: Chemical substances (can standardize to compounds)
- **BioAssay**: Experimental assays measuring biological activity
- **Gene**: Gene entities linked to compounds/assays
- **Protein**: Protein entities with PDB and conserved domain links
- **Pathway**: Biological pathways

### Important Properties
- `sio:SIO_000008`: Links compound to descriptors
- `sio:SIO_000300`: Descriptor value
- `sio:CHEMINF_000335`: Molecular formula
- `sio:CHEMINF_000334`: Molecular weight
- `sio:CHEMINF_000376`: Canonical SMILES
- `sio:CHEMINF_000396`: IUPAC InChI
- `obo:RO_0000087`: Biological role (e.g., FDAApprovedDrugs)
- `cheminf:CHEMINF_000455`: Stereoisomer relationship

### Named Graphs
- `http://rdf.ncbi.nlm.nih.gov/pubchem/compound` - Compounds
- `http://rdf.ncbi.nlm.nih.gov/pubchem/descriptor/compound` - Descriptors
- `http://rdf.ncbi.nlm.nih.gov/pubchem/bioassay` - BioAssays
- `http://rdf.ncbi.nlm.nih.gov/pubchem/gene` - Genes
- `http://rdf.ncbi.nlm.nih.gov/pubchem/protein` - Proteins
- `http://rdf.ncbi.nlm.nih.gov/pubchem/pathway` - Pathways

## Search Queries Performed

1. **get_pubchem_compound_id("aspirin")** → CID **2244**
2. **get_pubchem_compound_id("caffeine")** → CID **2519**
3. **get_pubchem_compound_id("imatinib")** → CID **5291**
4. **ncbi_esearch("penicillin")** → **304 compounds** found
5. **get_compound_attributes(CID2244)** → Formula C9H8O4, MW 180.16, SMILES CC(=O)OC1=CC=CC=C1C(=O)O

### Specific Compound Details Retrieved
| Compound | CID | Formula | MW (g/mol) |
|----------|-----|---------|------------|
| Aspirin | 2244 | C9H8O4 | 180.16 |
| Caffeine | 2519 | C8H10N4O2 | 194.19 |
| Imatinib | 5291 | C29H31N7O | 493.6 |

## SPARQL Queries Tested

### Query 1: Count FDA-Approved Drugs
```sparql
PREFIX vocab: <http://rdf.ncbi.nlm.nih.gov/pubchem/vocabulary#>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT (COUNT(DISTINCT ?compound) as ?fda_drugs_count)
WHERE {
  ?compound a vocab:Compound ;
            obo:RO_0000087 vocab:FDAApprovedDrugs .
}
```
**Result**: **17,367 FDA-approved drugs**

### Query 2: Count BioAssays
```sparql
PREFIX vocab: <http://rdf.ncbi.nlm.nih.gov/pubchem/vocabulary#>

SELECT (COUNT(DISTINCT ?bioassay) as ?bioassay_count)
FROM <http://rdf.ncbi.nlm.nih.gov/pubchem/bioassay>
WHERE {
  ?bioassay a vocab:BioAssay .
}
```
**Result**: **1,768,183 bioassays**

### Query 3: BioAssays by Source
```sparql
PREFIX vocab: <http://rdf.ncbi.nlm.nih.gov/pubchem/vocabulary#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?source (COUNT(?bioassay) as ?count)
FROM <http://rdf.ncbi.nlm.nih.gov/pubchem/bioassay>
WHERE {
  ?bioassay a vocab:BioAssay ;
            dcterms:source ?source .
}
GROUP BY ?source
ORDER BY DESC(?count)
LIMIT 5
```
**Results**:
| Source | Count |
|--------|-------|
| ChEMBL | 1,742,984 |
| BindingDB | 14,168 |
| IUPHAR_DB | 1,917 |
| NCGC | 1,760 |
| Scripps | 1,638 |

### Query 4: Entity Counts by Type
```sparql
SELECT (COUNT(DISTINCT ?gene) as ?gene_count) FROM gene graph
SELECT (COUNT(DISTINCT ?protein) as ?protein_count) FROM protein graph
SELECT (COUNT(DISTINCT ?pathway) as ?pathway_count) FROM pathway graph
```
**Results**:
- Genes: **167,172**
- Proteins: **248,623**
- Pathways: **80,739**

### Query 5: Aspirin Ontology Classifications
```sparql
PREFIX compound: <http://rdf.ncbi.nlm.nih.gov/pubchem/compound/>

SELECT ?type
WHERE {
  compound:CID2244 a ?type .
}
```
**Results**: Aspirin (CID2244) is classified as:
- SNOMED CT: 387458008, 426365001, 60526005, 7947003
- NCI Thesaurus: C287
- ChEBI: 15365
- NDFRT: N0000006582

## Interesting Findings

### Specific Entities for Questions
1. **Aspirin (CID2244)**: FDA-approved, ChEBI 15365, MW 180.16
2. **Caffeine (CID2519)**: MW 194.19, formula C8H10N4O2
3. **Imatinib (CID5291)**: Cancer drug, MW 493.6, formula C29H31N7O
4. ChEMBL provides the vast majority (98.6%) of bioassay data

### Unique Properties
- Multi-ontology integration: ChEBI, SNOMED CT, NCI, NDFRT for drug classification
- SIO ontology for descriptor access pattern
- Patent references via `cito:isDiscussedBy`

### Connections to Other Databases
- **ChEBI**: Ontology classification for compounds
- **PDB**: Protein-structure links from protein graph
- **NCBI Gene**: Gene links
- **ChEMBL**: 98.6% of bioassay data comes from ChEMBL
- **BindingDB, IUPHAR**: Additional bioassay sources

### Specific, Verifiable Facts
- Total FDA-approved drugs: **17,367**
- Total bioassays: **1,768,183**
- Total genes: **167,172**
- Total proteins: **248,623**
- Total pathways: **80,739**
- ChEMBL-sourced bioassays: **1,742,984** (98.6%)
- Aspirin CID: 2244
- Caffeine CID: 2519
- Imatinib CID: 5291

## ⚠️ CRITICAL: Cross-Reference/Mapping Analysis

### Protein-PDB Relationships
From sample query, proteins can link to multiple PDB structures:
- Example: ACC10GS_A (Glutathione S-transferase P1-1) links to 4 PDB IDs (10GS, 2GSS, 3GSS, 3GUS)
- Example: ACC1A07_B (C-SRC Tyrosine Kinase) links to 7+ PDB IDs

This is a one-to-many relationship (one protein → many PDB structures)

### Compound-Ontology Classifications
Aspirin (CID2244) has 7+ ontology type classifications from:
- SNOMED CT: 4 classifications
- NCI Thesaurus: 1 classification  
- ChEBI: 1 classification
- NDFRT: 1 classification

## Question Opportunities by Category

### Precision
- "What is the PubChem CID for aspirin?" (2244)
- "What is the molecular weight of caffeine?" (194.19 g/mol)
- "What is the molecular formula of imatinib?" (C29H31N7O)
- "What is the canonical SMILES for aspirin?" (CC(=O)OC1=CC=CC=C1C(=O)O)
- "What is the ChEBI identifier mapped to aspirin in PubChem?" (CHEBI:15365)

### Completeness
- "How many FDA-approved drugs are in PubChem?" (17,367)
- "How many bioassays are in PubChem?" (1,768,183)
- "How many genes are recorded in PubChem?" (167,172)
- "How many proteins are in PubChem?" (248,623)
- "How many pathways are in PubChem?" (80,739)

### Integration
- "What is the ChEBI ID mapped to PubChem CID 2244?" (CHEBI:15365)
- "Which PDB structures are linked to Glutathione S-transferase P1-1 in PubChem?"
- "What ontology systems classify aspirin in PubChem?" (SNOMED CT, NCI, ChEBI, NDFRT)

### Currency
- "How many bioassays are currently in PubChem?" (changes continuously)
- "What is the current count of FDA-approved compounds?" (17,367+)

### Specificity
- "What is the InChI for imatinib?" (detailed InChI string)
- "What SNOMED CT codes are associated with aspirin in PubChem?"
- "What is the primary source of bioassay data in PubChem?" (ChEMBL)

### Structured Query
- "Find FDA-approved drugs with molecular weight between 150-200 g/mol"
- "Find all compounds classified as CHEBI analgesics"
- "Find proteins with PDB structure links containing 'kinase' in their label"

## Notes

### Limitations
- Different named graphs require specific FROM clauses
- Descriptor values have mixed types (string/double)
- Not all compounds have complete descriptor sets
- Cross-graph joins can be slow without entity IDs

### Best Practices
- Use `FROM <graph_uri>` for entity-specific queries (bioassay, gene, protein, pathway)
- Filter by specific descriptor types using `sio:CHEMINF_*` classes
- Add LIMIT 50-100 for exploratory aggregation queries
- Use `get_pubchem_compound_id()` and `get_compound_attributes_from_pubchem()` for quick lookups

### Important Count Clarifications
- Bioassay counts are by assay record, not unique targets
- Protein counts include PDB chains as separate entities
- FDA drug count reflects compounds with explicit role annotation
