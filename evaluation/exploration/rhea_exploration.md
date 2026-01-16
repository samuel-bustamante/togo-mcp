# Rhea - Annotated Reactions Database Exploration Report

## Database Overview
- **Purpose**: Expert-curated database of biochemical reactions
- **Scope**: Enzymatic and transport reactions with atom-balanced equations
- **Scale**: 17,078 master reactions, 11,763 small molecules, 254 polymers
- **Key features**: ChEBI integration, EC numbers, GO terms, directional variants

## Schema Analysis (from MIE file)

### Main Entity Types
- **Reaction**: Master reaction (unspecified direction) - rdfs:subClassOf rhea:Reaction
- **DirectionalReaction**: Left-to-right or right-to-left direction
- **BidirectionalReaction**: Reversible reactions
- **ReactionSide**: Left (_L) or right (_R) side with participants
- **ReactionParticipant**: Compound in a reaction with optional location
- **SmallMolecule**: Chemical compounds with ChEBI links
- **Polymer**: Macromolecular structures with polymerization indices

### Important Properties
- `rhea:accession`: Reaction identifier (e.g., "RHEA:10000")
- `rhea:equation`: Text equation
- `rhea:status`: Approved, Preliminary, or Obsolete
- `rhea:isTransport`: Boolean for transport reactions
- `rhea:isChemicallyBalanced`: Always 1 for approved reactions
- `rhea:ec`: EC number link to UniProt enzyme namespace
- `rhea:directionalReaction`: Links to directional variants
- `rhea:side`: Links to left and right sides
- `rhea:chebi`: Direct ChEBI link for compounds

### Reaction ID Structure
Each reaction has a quartet of IDs:
- Master (unspecified): RHEA:10000
- Left-to-right: RHEA:10001
- Right-to-left: RHEA:10002
- Bidirectional: RHEA:10003

## Search Queries Performed

1. **search_rhea_entity("ATP")** → 10 reactions including transport reactions with ATP hydrolysis
2. **search_rhea_entity("glucose")** → 10 reactions including glucose oxidation, phosphorylation
3. **RHEA:10000** → Pentanamide hydrolysis (H2O + pentanamide = NH4(+) + pentanoate)
4. **RHEA:14293** → D-glucose + NAD(+) = D-glucono-1,5-lactone + NADH + H(+)

### Notable Reactions Found
| RHEA ID | Equation |
|---------|----------|
| RHEA:22044 | K(+)(out) + ATP + H2O + H(+)(in) = K(+)(in) + ADP + phosphate + 2 H(+)(out) |
| RHEA:14293 | D-glucose + NAD(+) = D-glucono-1,5-lactone + NADH + H(+) |
| RHEA:16689 | D-glucose 6-phosphate + H2O = D-glucose + phosphate |

## SPARQL Queries Tested

### Query 1: Total Reaction Count
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rhea: <http://rdf.rhea-db.org/>

SELECT (COUNT(DISTINCT ?reaction) as ?reaction_count)
WHERE {
  ?reaction rdfs:subClassOf rhea:Reaction .
}
```
**Result**: **17,078 master reactions**

### Query 2: Reactions by Status
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rhea: <http://rdf.rhea-db.org/>

SELECT ?status (COUNT(DISTINCT ?reaction) as ?count)
WHERE {
  ?reaction rdfs:subClassOf rhea:Reaction ;
            rhea:status ?status .
}
GROUP BY ?status
```
**Results**:
| Status | Count |
|--------|-------|
| Approved | 16,685 |
| Obsolete | 280 |
| Preliminary | 113 |

### Query 3: Transport Reactions
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rhea: <http://rdf.rhea-db.org/>

SELECT (COUNT(DISTINCT ?reaction) as ?transport_count)
WHERE {
  ?reaction rdfs:subClassOf rhea:Reaction ;
            rhea:isTransport 1 .
}
```
**Result**: **1,496 transport reactions**

### Query 4: Compound Counts
```sparql
SELECT 
  (COUNT(DISTINCT ?sm) as ?small_molecules)
  (COUNT(DISTINCT ?poly) as ?polymers)
WHERE {
  { ?sm rdfs:subClassOf rhea:SmallMolecule . }
  UNION
  { ?poly rdfs:subClassOf rhea:Polymer . }
}
```
**Results**:
- Small molecules: **11,763**
- Polymers: **254**

### Query 5: Cross-Reference Coverage
```sparql
# Count reactions with EC numbers
SELECT (COUNT(DISTINCT ?reaction) as ?reactions_with_ec)
WHERE {
  ?reaction rdfs:subClassOf rhea:Reaction ;
            rhea:ec ?ec .
}
```
**Results**:
- Reactions with EC numbers: **7,434** (43.5%)
- Reactions with GO terms: **4,440** (26%)

### Query 6: Specific Reaction Details (RHEA:10000)
```sparql
SELECT ?property ?value
WHERE {
  ?reaction rhea:accession "RHEA:10000" ;
            ?property ?value .
}
```
**Results**:
- Equation: H2O + pentanamide = NH4(+) + pentanoate
- EC number: 3.5.1.50
- Status: Approved
- GO term: GO:0050168
- Has directional variants: 10001, 10002, 10003

## Interesting Findings

### Specific Entities for Questions
1. **RHEA:10000**: Pentanamide hydrolysis, EC 3.5.1.50
2. **RHEA:14293**: Glucose dehydrogenase reaction
3. **RHEA:22044**: K+/ATP transport reaction
4. **EC 3.5.1.50**: Linked to RHEA:10000

### Unique Properties
- All approved reactions are atom-balanced and charge-balanced
- Transport reactions have location annotations (rhea:In, rhea:Out)
- Polymer notation uses (n), (n-1) for polymerization indices
- Literature citations in rdfs:comment field

### Connections to Other Databases
- **ChEBI**: 100% of small molecules have ChEBI cross-references
- **EC Numbers**: 7,434 reactions (43.5%) have EC classification
- **GO**: 4,440 reactions (26%) have Gene Ontology cross-references
- **KEGG, MetaCyc, Reactome**: Additional pathway database links via rdfs:seeAlso

### Specific, Verifiable Facts
- Total master reactions: **17,078**
- Approved reactions: **16,685**
- Preliminary reactions: **113**
- Obsolete reactions: **280**
- Transport reactions: **1,496**
- Small molecules: **11,763**
- Polymers: **254**
- Reactions with EC numbers: **7,434**
- Reactions with GO annotations: **4,440**

## ⚠️ CRITICAL: Cross-Reference/Mapping Analysis

### EC Number Cross-References
1. **Entity Count** (reactions with EC numbers): **7,434** (43.5% of total)
2. Multiple EC numbers per reaction possible (enzyme promiscuity)

### GO Cross-References
1. **Entity Count** (reactions with GO terms): **4,440** (26% of total)
2. Typically link to molecular function GO terms (GO:004xxxx)

### ChEBI Cross-References
1. **Entity Count**: **11,763** (100% of small molecules)
2. All small molecule compounds have ChEBI identifiers by design

## Question Opportunities by Category

### Precision
- "What is the equation for Rhea reaction RHEA:10000?" (H2O + pentanamide = NH4(+) + pentanoate)
- "What EC number is associated with RHEA:10000?" (EC 3.5.1.50)
- "What is the GO term linked to RHEA:10000?" (GO:0050168)
- "What is the ChEBI ID for water in Rhea?" (CHEBI:15377)

### Completeness
- "How many reactions are in Rhea?" (17,078 master reactions)
- "How many approved reactions are in Rhea?" (16,685)
- "How many transport reactions are in Rhea?" (1,496)
- "How many small molecule compounds are in Rhea?" (11,763)
- "How many Rhea reactions have EC number annotations?" (7,434)

### Integration
- "What EC numbers are in Rhea?" (via rhea:ec property)
- "Which GO terms are linked to Rhea reactions?" (via rdfs:seeAlso)
- "What ChEBI IDs are used in Rhea?"
- "What is the ChEBI ID for ATP in Rhea reactions?"

### Currency
- "What is the current status of RHEA:10000?" (Approved)
- "How many preliminary reactions await approval?" (113)
- "What new reactions were added to Rhea recently?"

### Specificity
- "What are the directional variants of RHEA:10000?" (10001, 10002, 10003)
- "Which reactions involve polymer substrates?" (~254 polymer-related)
- "What transport reactions involve potassium?" (K+ transport)

### Structured Query
- "Find all ATP-involving reactions in Rhea"
- "Find transport reactions with both inside and outside locations"
- "Find reactions with both EC number and GO annotation"
- "Find reactions involving glucose and phosphate"

## Notes

### Limitations
- Not all reactions have EC numbers (~43.5% coverage)
- GO term coverage is ~26%
- Some reactions have Preliminary or Obsolete status
- Polymer formula notation requires parsing for applications

### Best Practices
- Use `bif:contains` for keyword search in equations
- Filter by `rhea:status rhea:Approved` for validated reactions
- Use `rdfs:subClassOf rhea:Reaction` to get master reactions only
- Always add LIMIT for exploratory queries

### Important Count Clarifications
- **17,078** = master (unspecified direction) reactions
- **34,156** = directional reactions (2 per master)
- **17,078** = bidirectional reactions (1 per master)
- Total representations = 68,312 (4 × master count)
