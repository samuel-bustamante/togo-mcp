# TogoMCP Evaluation Scripts - Quick Reference

## ⚡ 30-Second Start

```bash
export ANTHROPIC_API_KEY="your-key"
python automated_test_runner.py example_questions.json
python results_analyzer.py evaluation_results.csv
python generate_dashboard.py evaluation_results.csv --open
```

## 🎯 Common Commands

### Run Evaluation
```bash
# Basic
python automated_test_runner.py questions.json

# With custom output
python automated_test_runner.py questions.json -o results.csv

# With config
python automated_test_runner.py questions.json -c config.json

# JSON format output
python automated_test_runner.py questions.json --format json
```

### Validate Questions
```bash
# Basic validation
python validate_questions.py questions.json

# Strict mode
python validate_questions.py questions.json --strict

# With cost estimate
python validate_questions.py questions.json --estimate-cost
```

### Analyze Results
```bash
# Basic analysis
python results_analyzer.py results.csv

# Verbose (show all questions)
python results_analyzer.py results.csv -v

# Export report
python results_analyzer.py results.csv --export report.md
```

### Generate Dashboard
```bash
# Generate dashboard
python generate_dashboard.py results.csv

# Custom output path
python generate_dashboard.py results.csv -o dashboard.html

# Generate and open
python generate_dashboard.py results.csv --open
```

## 📊 Complete Workflow

```bash
# 1. Create questions file (see format below)
vim my_questions.json

# 2. Validate
python validate_questions.py my_questions.json --estimate-cost

# 3. Run evaluation
python automated_test_runner.py my_questions.json -o results_$(date +%Y%m%d).csv

# 4. Analyze
python results_analyzer.py results_$(date +%Y%m%d).csv -v

# 5. Visualize
python generate_dashboard.py results_$(date +%Y%m%d).csv --open

# 6. Export report
python results_analyzer.py results_$(date +%Y%m%d).csv --export analysis_$(date +%Y%m%d).md
```

## 📝 Question File Format

```json
[
  {
    "id": 1,
    "category": "Precision",
    "question": "What is the UniProt ID for human BRCA1?",
    "expected_answer": "P38398",
    "notes": "Test basic ID lookup"
  }
]
```

**Required**: `question`  
**Recommended**: `id`, `category`, `expected_answer`, `notes`

## 📂 Scripts at a Glance

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `automated_test_runner.py` | Run evaluations | questions.json | results.csv |
| `results_analyzer.py` | Analyze results | results.csv | statistics + report.md |
| `validate_questions.py` | Validate questions | questions.json | validation report |
| `generate_dashboard.py` | Create dashboard | results.csv | dashboard.html |

## 🎓 Question Categories

| Category | Example | Purpose |
|----------|---------|---------|
| **Precision** | "What is UniProt ID for BRCA1?" | Exact IDs, values |
| **Completeness** | "How many genes in GO:0006281?" | Counts, lists |
| **Integration** | "Convert UniProt P04637 to Gene ID" | Cross-database |
| **Currency** | "SARS-CoV-2 pathways in Reactome?" | Recent info |
| **Specificity** | "MeSH ID for Erdheim-Chester?" | Niche topics |
| **Structured Query** | "Find all kinases in UniProt+ChEMBL" | Complex queries |

**Target**: 3-5 questions per category

## 📈 Understanding Results

### Value-Add Categories

| Score | Category | Meaning | Action |
|-------|----------|---------|--------|
| 15-18 | **CRITICAL** | Baseline failed, TogoMCP succeeded | Use for benchmarks |
| 9-14 | **VALUABLE** | Significant improvement | Include in eval |
| 4-8 | **MARGINAL** | Minor improvement | Consider revising |
| 0-3 | **REDUNDANT** | No improvement | Exclude |

### Success Patterns

| Pattern | Count | Interpretation |
|---------|-------|----------------|
| Both have expected | High | May be too easy |
| Only baseline | >0 | **Problem**: Check TogoMCP |
| Only TogoMCP | High | **Good**: Clear value-add |
| Neither | >0 | Revise questions |

### Tool Usage

| Rate | Meaning | Action |
|------|---------|--------|
| >70% | Excellent | Continue |
| 50-70% | Good | Add more DB-focused questions |
| <50% | Too simple | Revise questions |

## 🔧 Configuration

### config.json Structure

```json
{
  "model": "claude-sonnet-4-20250514",
  "mcp_servers": {
    "togomcp": {
      "type": "http",
      "url": "https://togomcp.rdfportal.org/mcp"
    }
  }
}
```

### Environment Variables

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 🚨 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| API key error | `export ANTHROPIC_API_KEY="sk-ant-..."` |
| SDK not found | `pip install claude-agent-sdk anthropic` |
| MCP failed | Check URL, network, server status |
| No tools used | Questions too simple, add DB requirements |
| Low success | Simplify questions or check config |

## 📊 Output Files

### evaluation_results.csv

**Key Columns**:
- `baseline_has_expected`: Did baseline include expected answer?
- `togomcp_has_expected`: Did TogoMCP include expected answer?
- `baseline_actually_answered`: Did baseline try to answer (vs "I don't know")?
- `tools_used`: Comma-separated MCP tools used
- `value_add`: Assessment (CRITICAL/VALUABLE/MARGINAL/REDUNDANT)

### analysis report (via --export)

**Sections**:
- Overall Statistics
- Category Breakdown
- Success Patterns
- Value-Add Assessment
- Problematic Questions
- Recommendations

### dashboard.html

**Charts**:
- Has Expected Answer comparison
- Expected Answer pattern distribution
- Category performance
- Top tools used
- Response time comparison

## 💡 Pro Tips

1. **Start Small**: 5-10 questions to learn, then scale
2. **Validate First**: Always run `validate_questions.py` before evaluation
3. **Use Dates**: Name outputs with dates (`results_20250117.csv`)
4. **Git Everything**: Version control questions, configs, and reports
5. **Focus on CRITICAL**: These show clearest value-add
6. **Check Tool Usage**: If <50%, questions may be too simple
7. **Iterate Fast**: Run → Analyze → Refine → Repeat
8. **Export Reports**: Save analysis with dates for tracking

## 🎯 Quality Checklist

**Good Question Set:**
- [ ] 3-5 questions per category
- [ ] >70% tool usage rate
- [ ] >70% questions show TogoMCP value-add
- [ ] <10% problematic questions
- [ ] All questions have expected answers
- [ ] Clear CRITICAL questions identified

**Good Workflow:**
- [ ] Questions validated before running
- [ ] Results saved with dates
- [ ] Analysis reports exported
- [ ] Dashboard generated and reviewed
- [ ] Insights documented
- [ ] Iterations tracked in git

## 📐 Evaluation Scale Guide

| Scale | Questions | Time | Approach |
|-------|-----------|------|----------|
| **Small** | 5-10 | 1-2h | Learn the system |
| **Medium** | 20-40 | 3-6h | Comprehensive eval |
| **Large** | 50+ | 1-2d | Benchmark creation |

## 🔄 Iteration Loop

```
Create Questions → Validate → Run Eval → Analyze
       ↑                                     ↓
       └───────────── Refine ←───────────────┘
```

**Stop When:**
- 70%+ questions show value-add
- All categories have 3+ questions
- <10% problematic questions
- Clear CRITICAL candidates identified

## 📚 Quick Help

```bash
# View README
cat README.md | less

# Show this card
cat QUICK_REFERENCE.md

# Check requirements
cat requirements.txt

# View example questions
cat example_questions.json | jq

# Check config
cat config.json | jq
```

## 🔗 Related Files

- **README.md**: Full documentation
- **../EVALUATION_README.md**: System overview
- **../togomcp_evaluation_rubric.md**: Evaluation methodology
- **requirements.txt**: Python dependencies
- **config.json**: MCP configuration
- **example_questions.json**: Sample questions

## ⚙️ Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or manually
pip install claude-agent-sdk anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Verify installation
python -c "import anthropic, claude_agent_sdk; print('OK')"
```

## 💰 Cost Estimation

```bash
# Estimate cost before running
python validate_questions.py questions.json --estimate-cost

# Typical costs (Claude Sonnet 4):
# - Small eval (10 questions): ~$0.10-0.20
# - Medium eval (40 questions): ~$0.40-0.80
# - Large eval (100 questions): ~$1.00-2.00
```

## 🎨 Dashboard Features

**Metrics Displayed**:
- Total questions evaluated
- Baseline "has expected" rate
- TogoMCP "has expected" rate
- Unique tools used
- Total tool calls

**Charts**:
- Stacked bar: Has expected vs missing expected
- Doughnut: Pattern distribution (both/only baseline/only TogoMCP/neither)
- Bar: Category performance comparison
- Horizontal bar: Top 10 tools used
- Bar: Average response time comparison

## 📞 Getting Help

1. **Check README.md**: Full documentation
2. **Run with --help**: `python script.py --help`
3. **Check examples**: Review `example_questions.json`
4. **Validate questions**: Find issues before running
5. **Review errors**: Error messages usually point to the issue

## ✅ Success Indicators

You're on the right track when:
- ✅ Evaluations complete without errors
- ✅ >70% tool usage rate
- ✅ Clear CRITICAL questions identified
- ✅ All categories represented
- ✅ Can explain each metric
- ✅ Dashboard shows clear patterns
- ✅ Iteration improves results

---

**Remember**:
- Quality > Quantity
- Start small, iterate fast
- Document everything
- Tool usage = question quality
- CRITICAL questions = your benchmarks

**Need more details?** → Read [README.md](README.md)
