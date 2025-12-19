# TogoMCP Evaluation

**Automated evaluation suite for testing TogoMCP's biological database query capabilities.**

## 🚀 Quick Start (30 seconds)

```bash
cd scripts
export ANTHROPIC_API_KEY="your-key-here"
python automated_test_runner.py ../questions/Q01.json
python compute_costs.py evaluation_results.csv
python results_analyzer.py evaluation_results.csv
python generate_dashboard.py evaluation_results.csv --open
```

**First time here?** → Read the [5-minute overview](#5-minute-overview) below.

---

## 📁 What's Here

| Directory | What It Contains | When You Need It |
|-----------|------------------|------------------|
| **`scripts/`** | Automated evaluation tools | Running evaluations ⭐ |
| **`questions/`** | 120 pre-designed test questions | Understanding what's tested |
| **`exploration/`** | Database capability documentation | Reference material |
| **`results/`** | Evaluation output data | Analyzing results |
| **`archive/`** | Deprecated manual templates | Historical reference only |

**Key files**:
- **`README.md`** - Quick start guide (you are here)
- **`QUESTION_DESIGN_GUIDE.md`** - How to create evaluation questions
- **`PROJECT_STATUS.md`** - Current progress and timeline

---

## 5-Minute Overview

### What Is This?

This evaluation suite tests how well TogoMCP (Model Context Protocol for biological databases) improves Claude's ability to answer biology research questions.

**The Test**: Ask Claude the same question twice:
1. **Baseline**: Without access to database tools
2. **TogoMCP**: With access to 22 biological databases

**The Goal**: Measure the improvement when Claude can query real databases.

### What's Been Done?

✅ **Phase 1**: Explored 22 biological databases (UniProt, PubChem, GO, etc.)  
✅ **Phase 2**: Created 120 evaluation questions across 6 categories  
🔄 **Phase 3**: Running automated evaluations (24/120 complete)  
📊 **Phase 4**: Comprehensive analysis (pending)

**See**: [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for detailed progress.

### The 120 Questions

Questions test 6 different capabilities:

| Category | Tests | Example |
|----------|-------|---------|
| **Precision** | Exact IDs, values | "What is the UniProt ID for human BRCA1?" |
| **Completeness** | Counts, exhaustive lists | "How many genes in GO term DNA repair?" |
| **Integration** | Cross-database linking | "Convert UniProt P04637 to Gene ID" |
| **Currency** | Recent/updated data | "SARS-CoV-2 pathways in Reactome?" |
| **Specificity** | Niche, specialized topics | "MeSH ID for Erdheim-Chester disease?" |
| **Structured Query** | Complex multi-step queries | "Find all kinases with ChEMBL data" |

**See**: [`questions/SUMMARY.md`](questions/SUMMARY.md) for complete details.

### The 22 Databases

**Proteins & Genes**: UniProt, PDB, NCBI Gene, Ensembl, DDBJ, Taxonomy  
**Chemicals**: ChEBI, ChEMBL, PubChem, Rhea  
**Pathways**: Reactome, GO  
**Clinical**: ClinVar, MedGen, MONDO, NANDO  
**Literature**: MeSH, PubMed, PubTator  
**Specialized**: BacDive, MediaDive, GlyCosmos

**See**: [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md) for database capabilities.

---

## 🎯 Common Use Cases

### I want to create evaluation questions

```bash
cat QUESTION_DESIGN_GUIDE.md  # Read the question design guide
cat questions/Q01.json | jq   # See examples
```

**Full guide**: [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)

### I want to run evaluations

```bash
cd scripts
cat README.md  # Read the complete guide
python automated_test_runner.py ../questions/Q03.json
```

**Full documentation**: [`scripts/README.md`](scripts/README.md)  
**Quick commands**: [`scripts/QUICK_REFERENCE.md`](scripts/QUICK_REFERENCE.md)

### I want to calculate evaluation costs

```bash
cd scripts
python compute_costs.py ../results/results.csv
python compute_costs.py ../results/results.csv --export cost_report.json
```

The cost calculator provides:
- Breakdown of baseline vs TogoMCP costs
- Cache usage analysis (creation + read tokens)
- Costs by category and value-add
- Per-question cost averages

**Supports**:
- Multiple Claude models (Sonnet 4, Opus 4, Haiku 4)
- Custom pricing configurations
- Detailed JSON export for further analysis

### I want to understand the questions

```bash
cat questions/SUMMARY.md
cat questions/Q01.json | jq
```

Each question includes:
- Natural language question text
- Expected answer for verification
- Category (Precision/Completeness/etc.)
- Detailed notes explaining the test

### I want to see what databases can do

```bash
cat exploration/00_SUMMARY.md  # Overview of all 22 databases
cat exploration/uniprot_exploration.md  # Deep dive on specific database
```

Each database report includes:
- 5+ search query examples
- 3+ SPARQL query examples
- Capabilities and limitations
- Question design opportunities

### I want to check project progress

```bash
cat PROJECT_STATUS.md
```

Shows:
- What's complete (exploration, questions)
- What's in progress (evaluation)
- What's next (analysis)
- Detailed metrics and timeline

### I want to analyze results

```bash
cd scripts
python compute_costs.py ../results/results.csv
python results_analyzer.py ../results/results.csv -v
python generate_dashboard.py ../results/results.csv --open
```

Get:
- Cost analysis with cache breakdown
- Success rate comparisons
- Tool usage statistics
- Category performance breakdown
- Interactive HTML dashboard

---

## 📚 Documentation Guide

**Start here** (pick one based on your goal):

| I want to... | Read this |
|--------------|-----------|
| **Create evaluation questions** | [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md) |
| **Run evaluations** | [`scripts/README.md`](scripts/README.md) |
| **Calculate costs** | See [Cost Analysis](#cost-analysis) below |
| **Quick command reference** | [`scripts/QUICK_REFERENCE.md`](scripts/QUICK_REFERENCE.md) |
| **Check project status** | [`PROJECT_STATUS.md`](PROJECT_STATUS.md) |
| **Learn about questions** | [`questions/SUMMARY.md`](questions/SUMMARY.md) |
| **Learn about databases** | [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md) |

---

## 💰 Cost Analysis

### Using compute_costs.py

The `compute_costs.py` script provides comprehensive cost breakdowns for your evaluation runs:

```bash
# Basic usage
python compute_costs.py evaluation_results.csv

# Specify different model
python compute_costs.py results.csv --model claude-opus-4-20250514

# Export detailed JSON report
python compute_costs.py results.csv --export cost_report.json

# Use custom pricing
python compute_costs.py results.csv --pricing custom_pricing.json
```

### What It Calculates

**Baseline Costs**:
- Input/output token usage
- Per-test and total costs
- Success rate impact

**TogoMCP Costs** (with cache efficiency):
- Regular input/output tokens
- **Cache creation tokens** (system prompt + tools, charged at +25%)
- **Cache read tokens** (reading cached content, charged at -90%)
- Tool usage overhead

**Breakdowns**:
- By question category (Precision, Completeness, etc.)
- By value-add level (CRITICAL, VALUABLE, etc.)
- Per-question averages

### Understanding Cache Costs

The evaluation runner uses **isolated sessions** for optimal cache efficiency:

**How it works**:
```
Q1: CREATE cache (system + tools) + READ cache → Answer
Q2: CREATE minimal + READ cache → Answer  ← Fresh session
Q3: CREATE minimal + READ cache → Answer  ← Fresh session
```

**Benefits**:
- Stable, predictable costs per question
- No exponential cache growth
- ~46% cheaper than conversation accumulation
- Each question independent (no cross-contamination)

**Example** (12 questions):
- Cache creation: ~98k tokens × $3.75/MTok = $0.37
- Cache reads: ~644k tokens × $0.30/MTok = $0.19
- **Total cache cost: ~$0.56**

### Supported Models

Built-in pricing for:
- `claude-sonnet-4-20250514` - $3.00/$15.00 per MTok (default)
- `claude-opus-4-20250514` - $15.00/$75.00 per MTok
- `claude-haiku-4-20250110` - $0.80/$4.00 per MTok
- `claude-sonnet-3-5-20241022` - $3.00/$15.00 per MTok

**Cache pricing** automatically calculated:
- Creation: base price + 25%
- Read: base price - 90%

### Sample Output

```
================================================================================
COST ANALYSIS FOR TOGOMCP EVALUATION
================================================================================
Model: Claude Sonnet 4
Pricing: $3.00/MTok input, $15.00/MTok output
Total questions evaluated: 12

BASELINE COSTS (No Tools)
--------------------------------------------------------------------------------
  Successful tests:     12/12
  Input tokens:         780
  Output tokens:        1,400
  Total tokens:         2,180
  Total cost:           $0.0234
  Avg cost per test:    $0.0020

TOGOMCP COSTS (With MCP Tools) (EXACT)
--------------------------------------------------------------------------------
  ✅ Using actual token counts from Agent SDK ResultMessage

  Successful tests:     12/12
  Input tokens:         108
  Output tokens:        4,600
  Cache creation:       98,011 tokens
  Cache read:           644,288 tokens
  Total tokens:         4,708
  Total cost:           $0.6308
  Avg cost per test:    $0.0526

TOTAL EVALUATION COST
--------------------------------------------------------------------------------
  Baseline:             $0.0234 (3.6%)
  TogoMCP:              $0.6308 (96.4%)
  TOTAL:                $0.6542

  TogoMCP overhead:     +2596.2% vs baseline

COSTS BY CATEGORY
--------------------------------------------------------------------------------
  Precision            $0.0908  (Base: $0.0038, TogoMCP: $0.0869)
  Completeness         $0.0860  (Base: $0.0039, TogoMCP: $0.0821)
  Integration          $0.0880  (Base: $0.0039, TogoMCP: $0.0841)
  ...
```

### Cost Estimation Strategy

**For planning**:
- Small evaluation (12 questions): ~$0.65
- Medium evaluation (24 questions): ~$1.30
- Full evaluation (120 questions): ~$6.50

**Per question average**:
- Baseline: ~$0.002
- TogoMCP: ~$0.053
- Total: ~$0.055

**Cache efficiency note**: The isolated session design keeps costs predictable and ~46% lower than accumulating conversation sessions.

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Anthropic API key
- ~30 minutes for small evaluation (10 questions)
- ~6-8 hours for full evaluation (120 questions)

### Setup

```bash
# 1. Install dependencies
cd scripts
pip install -r requirements.txt

# 2. Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Verify setup
python -c "import anthropic; print('Ready!')"

# 4. Test with example
python automated_test_runner.py example_questions.json
```

**Troubleshooting**: See [`scripts/README.md`](scripts/README.md#troubleshooting)

---

## 📊 Current Status

**Last Updated**: 2025-12-19

| Phase | Status | Progress |
|-------|--------|----------|
| Database Exploration | ✅ Complete | 22/22 databases (100%) |
| Question Generation | ✅ Complete | 120/120 questions (100%) |
| Automated Evaluation | 🔄 In Progress | 24/120 questions (20%) |
| Analysis & Reporting | 📊 Pending | Awaiting full evaluation |

**Next**: Complete evaluation for Q03-Q10 (96 questions)

**See**: [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for detailed breakdown.

---

## 💡 Key Concepts

### Baseline vs TogoMCP

**Baseline**: Claude answers using only training knowledge (cutoff: January 2025)
- May be outdated
- No access to specific database IDs
- Can't verify current data
- Limited to general knowledge

**TogoMCP**: Claude answers with database access via MCP
- Current, verified data
- Exact IDs and values
- Cross-database integration
- Comprehensive results

### Isolated Session Design

The evaluation runner uses **isolated sessions** for optimal efficiency:

**Architecture**:
```python
for question in questions:
    async with ClaudeSDKClient(options=options) as client:
        # Fresh session - no history
        result = await client.query(question)
    # Client closes, history discarded
```

**Benefits**:
- ✅ Predictable cache costs
- ✅ No cross-question contamination
- ✅ Stable performance
- ✅ 46% cheaper than conversation accumulation

### Value-Add Categories

Questions are automatically scored:

- **CRITICAL** (15-18 points): Essential improvement, use for benchmarks
- **VALUABLE** (9-14 points): Significant improvement, include in evaluation
- **MARGINAL** (4-8 points): Minor improvement, consider revising
- **REDUNDANT** (0-3 points): No improvement, exclude

**Goal**: Identify CRITICAL questions that clearly demonstrate TogoMCP's value.

### Success Patterns

After evaluation, each question falls into one of four patterns:

| Pattern | Meaning | Action |
|---------|---------|--------|
| **Both have expected** | Both answered correctly | Question may be too easy |
| **Only baseline** | TogoMCP failed | Check configuration |
| **Only TogoMCP** | Clear value-add! | **Keep this question** |
| **Neither** | Both failed | Revise or clarify question |

---

## 🔬 Example Workflow

### Complete Evaluation for One Question Set

```bash
# 1. Validate questions
cd scripts
python validate_questions.py ../questions/Q03.json --estimate-cost

# 2. Run evaluation
python automated_test_runner.py ../questions/Q03.json -o ../results/Q03_out.csv

# 3. Calculate costs
python compute_costs.py ../results/Q03_out.csv

# 4. Analyze results
python results_analyzer.py ../results/Q03_out.csv -v

# 5. Generate dashboard
python generate_dashboard.py ../results/Q03_out.csv --open

# 6. Review and document findings
# (Check dashboard for insights, identify high-value questions)
```

**Time**: ~30-45 minutes for 12 questions  
**Cost**: ~$0.65 (includes cache overhead)

---

## 🎓 Learning Path

**New to this project?** Follow this sequence:

1. **Read this README** (you're here!) - 5 min
2. **Check [`PROJECT_STATUS.md`](PROJECT_STATUS.md)** - Understand progress - 5 min
3. **Browse [`questions/SUMMARY.md`](questions/SUMMARY.md)** - See what's tested - 10 min
4. **Read [`scripts/README.md`](scripts/README.md)** - Learn the tools - 20 min
5. **Run a test evaluation** - Try Q01.json - 30 min
6. **Calculate costs** - Analyze spending - 5 min
7. **Review results** - Analyze what happened - 15 min

**Total**: ~90 minutes to full understanding

**Want details on databases?** See [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md)  
**Want to create questions?** See [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)

---

## 🚨 Common Questions

### Why is evaluation only 20% complete?

The automated evaluation is compute-intensive:
- Each question requires 2 API calls (baseline + TogoMCP)
- Full evaluation = 240 API calls
- Takes 6-8 hours + ~$6.50 in API costs

We ran Q01-Q02 as validation. Q03-Q10 are ready to run.

### How much does evaluation cost?

Use `compute_costs.py` for exact calculations:

**Example costs** (Claude Sonnet 4):
- 12 questions: ~$0.65 total
- 24 questions: ~$1.30 total
- 120 questions: ~$6.50 total

**Per question**: ~$0.055 ($0.002 baseline + $0.053 TogoMCP)

Most cost is from TogoMCP cache operations, which are optimized through isolated sessions.

### What's the cache efficiency strategy?

The runner uses **isolated sessions**:
- Each question gets a fresh client (no conversation history)
- Only system prompt + tools are cached
- Cache reads stay constant (~30-85k tokens per question)
- **46% cheaper** than accumulating conversation sessions
- **No cross-question contamination**

See the [Cost Analysis](#cost-analysis) section for details.

### Can I add my own questions?

Yes! See [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md) for the complete guide.

Quick example:

```json
{
  "id": 121,
  "category": "Precision",
  "question": "Your question here",
  "expected_answer": "Expected result",
  "notes": "Why this tests database access"
}
```

Then validate and run:

```bash
python validate_questions.py my_questions.json
python automated_test_runner.py my_questions.json
python compute_costs.py results.csv
```

### What happened to the manual templates?

They've been archived to `archive/manual_evaluation/`. The automated scripts replaced the manual workflow for consistency and reproducibility.

**Still accessible** if you need them for special cases.

### How do I interpret results?

Key metrics:
- **has_expected**: Did the answer include the expected result?
- **tools_used**: Which MCP tools were called?
- **value_add**: CRITICAL/VALUABLE/MARGINAL/REDUNDANT
- **cache metrics**: Creation and read token counts

**Use compute_costs.py** to understand spending breakdown.

**See**: [`scripts/README.md`](scripts/README.md#understanding-results) for details.

---

## 🤝 Contributing

### Adding Questions
1. Read [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)
2. Follow format in existing JSON files
3. Use `validate_questions.py` to check
4. Ensure expected answers are verifiable

### Improving Documentation
1. Keep README.md concise (entry point)
2. Put details in specific docs (scripts/README.md, QUESTION_DESIGN_GUIDE.md)
3. Update PROJECT_STATUS.md when progress changes
4. Add examples to help users

### Reporting Issues
- Missing database functionality? Document in exploration reports
- Question problems? Note in question SUMMARY.md
- Script bugs? See scripts/README.md for troubleshooting
- Cost discrepancies? Check compute_costs.py output

---

## 📈 Next Steps

**If you're here to use the evaluation suite**:
1. Install dependencies: `pip install -r scripts/requirements.txt`
2. Read the full guide: [`scripts/README.md`](scripts/README.md)
3. Run your first evaluation: Start with Q01.json
4. Calculate costs: `compute_costs.py`
5. Analyze results and iterate

**If you're here to understand the project**:
1. Check status: [`PROJECT_STATUS.md`](PROJECT_STATUS.md)
2. Review questions: [`questions/SUMMARY.md`](questions/SUMMARY.md)
3. Explore databases: [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md)
4. Learn question design: [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)

**If you're here to complete the evaluation**:
1. Run Q03-Q10: See [`scripts/QUICK_REFERENCE.md`](scripts/QUICK_REFERENCE.md)
2. Track costs: Use `compute_costs.py` for each batch
3. Combine results: Use `results/combine_csv.py`
4. Analyze: `results_analyzer.py` + `generate_dashboard.py`
5. Document findings: Update PROJECT_STATUS.md

---

## 📞 Support

**For question design**: [`QUESTION_DESIGN_GUIDE.md`](QUESTION_DESIGN_GUIDE.md)  
**For script usage**: [`scripts/README.md`](scripts/README.md)  
**For cost analysis**: See [Cost Analysis](#cost-analysis) section above  
**For question format**: [`scripts/QUESTION_FORMAT.md`](scripts/QUESTION_FORMAT.md)  
**For database info**: [`exploration/00_SUMMARY.md`](exploration/00_SUMMARY.md)  
**For project status**: [`PROJECT_STATUS.md`](PROJECT_STATUS.md)

---

## 📄 License

This evaluation tooling follows the same license as the main TogoMCP project.

---

**Last Updated**: 2025-12-19  
**Version**: 2.1 (Optimized Cache Design + Cost Analysis)  
**Status**: Foundation Complete ✅ | Evaluation In Progress 🔄

**Ready to start?** → Pick your path above and dive in!
