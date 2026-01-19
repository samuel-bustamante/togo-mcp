# ChEMBL Exploration Report

## Database Overview
- **Purpose**: Manually curated database of bioactive molecules with drug-like properties
- **Key data types**: Small molecules, bioactivity measurements, protein targets, assays, drug mechanisms, drug indications
- **Scale**: 1.9M+ molecules, 21M+ activities, 1.7M+ assays, 15K+ targets
- **Scope**: Drug discovery data including compound-target-activity relationships

## Schema Analysis (from MIE file)

### Main Entity Types
1. **SmallMolecule**: Core compound entity
   - Properties: chemblId, substanceType, highestDevelopmentPhase, atcClassification
   - Relationships: hasActivity, hasDrugIndication, hasMechanism, moleculeXref

2. **Activity**: Bioactivity measurement
   - Properties: standardType (IC50, Ki, etc.), standardValue, standardUnits, pChembl
   - Relationships: hasMolecule, hasAssay

3. **Target**: Drug target (proteins, organisms, cells)
   - Types: SingleProtein, ProteinComplex, ProteinFamily
   - Properties: targetType, organismName
   - Relationships: hasTargetComponent

4. **Assay**: Experimental assay
   - Properties: assayType (Functional, Binding, ADME, etc.)
   - Relationships: hasTarget

5. **DrugIndication**: Clinical indication
   - Properties: hasMesh, hasMeshHeading, highestDevelopmentPhase
   - Relationships: hasMolecule

### Query Patterns
- Use `search_chembl_molecule` and `search_chembl_target` for keyword search
- Use `bif:contains` for SPARQL full-text search
- Always specify `FROM <http://rdf.ebi.ac.uk/dataset/chembl>`
- Filter by activity units when comparing values

## Search Queries Performed

1. **Query**: Search for imatinib
   - Results: CHEMBL941 (IMATINIB), CHEMBL1642 (IMATINIB MESYLATE), plus 3 derivatives

2. **Query**: Search for BRCA1 targets
   - Results: CHEMBL5990 (Breast cancer type 1 susceptibility protein), CHEMBL4105965, CHEMBL5291566, CHEMBL1293314

3. **Query**: Total molecule count
   - Results: 1,920,809 small molecules

4. **Query**: Total activity count
   - Results: 21,123,501 bioactivity measurements

5. **Query**: Development phase distribution
   - Results: Phase 4 (marketed): 3,678 | Phase 3: 1,105 | Phase 2: 6,442 | Phase 1: 959

6. **Query**: Target type distribution
   - Results: SINGLE PROTEIN (9,432), ORGANISM (2,353), CELL-LINE (1,920), PROTEIN COMPLEX (613)

7. **Query**: Assay type distribution
   - Results: Functional (831K), Binding (523K), ADME (297K), Toxicity (60K)

## SPARQL Queries Tested

```sparql
# Query 1: Count molecules by development phase
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT ?phase (COUNT(?molecule) as ?moleculeCount)
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?molecule a cco:SmallMolecule .
  ?molecule cco:highestDevelopmentPhase ?phase .
}
GROUP BY ?phase
ORDER BY ?phase
# Results: Phase 4: 3,678 | Phase 3: 1,105 | Phase 2: 6,442 | Phase 1: 959
```

```sparql
# Query 2: Target type distribution
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT ?targetType (COUNT(?target) as ?targetCount)
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?target cco:targetType ?targetType .
}
GROUP BY ?targetType
ORDER BY DESC(?targetCount)
# Results: SINGLE PROTEIN (9,432), ORGANISM (2,353), etc.
```

```sparql
# Query 3: Bioactivity data for imatinib (CHEMBL941)
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT ?activity ?type ?value ?units ?targetLabel
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?activity a cco:Activity ;
            cco:hasMolecule <http://rdf.ebi.ac.uk/resource/chembl/molecule/CHEMBL941> ;
            cco:standardType ?type ;
            cco:standardValue ?value ;
            cco:standardUnits ?units ;
            cco:hasAssay/cco:hasTarget ?target .
  ?target rdfs:label ?targetLabel .
}
LIMIT 20
# Results: Multiple activity types including AC50 against K562 (680 nM)
```

```sparql
# Query 4: Assay type distribution
PREFIX cco: <http://rdf.ebi.ac.uk/terms/chembl#>
SELECT ?assayType (COUNT(?assay) as ?assayCount)
FROM <http://rdf.ebi.ac.uk/dataset/chembl>
WHERE {
  ?assay a cco:Assay .
  ?assay cco:assayType ?assayType .
}
GROUP BY ?assayType
ORDER BY DESC(?assayCount)
# Results: Functional (831K), Binding (523K), ADME (297K)
```

## Interesting Findings

### Specific Entities for Questions
- **Imatinib**: CHEMBL941 - tyrosine kinase inhibitor for CML
- **BRCA1 target**: CHEMBL5990 - Breast cancer type 1 susceptibility protein
- **Marketed drugs**: 3,678 compounds at Phase 4
- **Single protein targets**: 9,432 targets available

### Unique Properties
- Development phase tracking (0.5 to 4)
- Standardized activity units (nM, uM, %, etc.)
- ATC (Anatomical Therapeutic Chemical) classification
- Drug mechanisms with action types (INHIBITOR, AGONIST, etc.)

### Cross-Database Connections
- PubChem (2.2M+ molecules)
- DrugBank (8.4K molecules)
- UniProt (via TargetComponent, 11K links)
- ChEBI (35K molecules)
- MeSH (51K drug indications)
- PubMed (88K documents)
- NCBI Taxonomy (organism info)

### Verifiable Facts
- 1,920,809 small molecules in ChEMBL
- 21,123,501 bioactivity measurements
- 3,678 marketed drugs (Phase 4)
- 9,432 single protein targets
- Imatinib (CHEMBL941) is a tyrosine kinase inhibitor
- 830,894 functional assays, 523,393 binding assays

## Question Opportunities by Category

### Precision
- "What is the ChEMBL ID for imatinib?" (Answer: CHEMBL941)
- "What is the ChEMBL target ID for BRCA1?" (Answer: CHEMBL5990)
- "What is the ChEMBL ID for the human angiotensin-converting enzyme target?" (Answer: CHEMBL1808)

### Completeness
- "How many small molecules are in ChEMBL?" (Answer: 1,920,809)
- "How many bioactivity measurements are in ChEMBL?" (Answer: 21,123,501)
- "How many marketed drugs (Phase 4) are in ChEMBL?" (Answer: 3,678)
- "What are all the target types in ChEMBL?" (List of types)

### Integration
- "What UniProt IDs are linked to ChEMBL target CHEMBL1808?" (via TargetComponent)
- "What DrugBank ID is linked to CHEMBL941?" (via moleculeXref)
- "Find ChEMBL molecules cross-referenced to PubChem"

### Currency
- "What are the most recently added ChEMBL assays?"

### Specificity
- "Find ChEMBL molecules in Phase 3 clinical trials for melanoma"
- "What kinase inhibitors in ChEMBL have IC50 < 10 nM?"
- "Find ChEMBL targets classified as PROTEIN COMPLEX"

### Structured Query
- "Find ChEMBL molecules with IC50 < 100 nM against kinase targets"
- "List ChEMBL drugs with both DrugBank AND UniProt cross-references"
- "Find binding assays for human single protein targets"
- "Find molecules with Phase 4 development AND ATC classification"

## Notes

### Limitations
- Not all molecules have complete chemical descriptors
- Activity values may lack units (always check standardUnits)
- Some targets lack UniProt mappings (especially non-human)
- Development phase most complete for marketed drugs

### Best Practices
- Use search_chembl_molecule and search_chembl_target for keyword searches
- Always include `FROM <http://rdf.ebi.ac.uk/dataset/chembl>` in SPARQL
- Use `bif:contains` for full-text search with boolean operators
- Always filter by standardUnits when comparing activity values
- Filter by standardType (IC50, Ki, EC50) for meaningful comparisons
- Use pChembl for normalized potency comparisons

### Activity Value Handling
- standardType: IC50, Ki, EC50, AC50, etc.
- standardValue: Numeric value
- standardUnits: nM, uM, %, U.L-1, etc.
- pChembl: Negative log of activity value (normalized)
