# TogoMCP Evaluation Scripts

Automated evaluation tools for testing TogoMCP's effectiveness in answering biological database queries.

## 📋 Overview

This directory contains Python scripts for automated evaluation of TogoMCP:
- **Run evaluations**: Compare baseline Claude vs TogoMCP-enhanced responses
- **Analyze results**: Generate statistics and identify high-value questions
- **Validate questions**: Check question files before running evaluations
- **Visualize data**: Create interactive HTML dashboards

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
export ANTHROPIC_API_KEY="your-key-here"

# 3. Run evaluation
python automated_test_runner.py example_questions.json

# 4. Analyze results
python results_analyzer.py evaluation_results.csv

# 5. Generate dashboard
python generate_dashboard.py evaluation_results.csv --open
```

## 📦 Installation

### Requirements
- Python 3.8+
- Anthropic API key

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install claude-agent-sdk anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 🛠️ Scripts Overview

### 1. automated_test_runner.py

**Purpose**: Run automated evaluations comparing baseline vs TogoMCP responses

**Features**:
- Two-phase testing (baseline without tools, TogoMCP with MCP servers)
- Automatic correctness evaluation
- Expected answer matching
- Tool usage tracking
- Response time measurement
- Token usage tracking

**Usage**:
```bash
# Basic usage
python automated_test_runner.py questions.json

# Custom output path
python automated_test_runner.py questions.json -o results.csv

# With custom config
python automated_test_runner.py questions.json -c config.json

# JSON output format
python automated_test_runner.py questions.json --format json
```

**Output**: CSV file with columns:
- `question_id`, `date`, `category`, `question_text`
- `baseline_success`, `baseline_actually_answered`, `baseline_has_expected`
- `baseline_confidence`, `baseline_text`, `baseline_time`, `baseline_input_tokens`, `baseline_output_tokens`
- `togomcp_success`, `togomcp_has_expected`, `togomcp_confidence`
- `togomcp_text`, `togomcp_time`, `tools_used`, `tool_details`
- `value_add`, `expected_answer`, `notes`

### 2. results_analyzer.py

**Purpose**: Analyze evaluation results and generate insights

**Features**:
- Overall statistics (success rates, tool usage, response times)
- Category breakdown (performance by question category)
- Pattern analysis (both succeeded, only baseline, only TogoMCP, both failed)
- Value-add assessment (CRITICAL, VALUABLE, MARGINAL, REDUNDANT)
- Problematic question identification
- Recommendations for improvement

**Usage**:
```bash
# Basic analysis
python results_analyzer.py evaluation_results.csv

# Verbose output (show individual questions)
python results_analyzer.py evaluation_results.csv -v

# Export detailed report
python results_analyzer.py evaluation_results.csv --export report.md
```

**Metrics Explained**:
- **Has Expected Answer**: Percentage of responses containing the expected answer
- **Actually Answered**: Percentage where baseline didn't refuse/say "I don't have access"
- **Tool Usage Rate**: Percentage of questions using MCP tools
- **Value Add Categories**:
  - CRITICAL (15-18 points): Essential improvements, use for benchmarks
  - VALUABLE (9-14 points): Significant improvements, include in evaluation
  - MARGINAL (4-8 points): Minor improvements, consider revising
  - REDUNDANT (0-3 points): No improvement, exclude

### 3. validate_questions.py

**Purpose**: Validate question files before running evaluations

**Features**:
- JSON syntax validation
- Required field checking
- Category balance analysis
- Duplicate detection
- API cost estimation
- Question quality assessment

**Usage**:
```bash
# Basic validation
python validate_questions.py questions.json

# Strict mode (enforce all recommendations)
python validate_questions.py questions.json --strict

# Show cost estimate
python validate_questions.py questions.json --estimate-cost
```

**Checks**:
- ✅ Valid JSON format
- ✅ Required fields present (`question`)
- ✅ Valid categories (Precision, Completeness, Integration, Currency, Specificity, Structured Query)
- ✅ Category balance (at least 3 questions per category)
- ✅ No duplicate questions
- ✅ Question quality (length, clarity)
- 💰 API cost estimation

### 4. generate_dashboard.py

**Purpose**: Create interactive HTML dashboard from evaluation results

**Features**:
- Visual charts and graphs
- Success rate comparison
- Category performance breakdown
- Tool usage statistics
- Response time comparison
- Pattern distribution analysis
- **Based on "Has Expected Answer" metric**

**Usage**:
```bash
# Generate dashboard
python generate_dashboard.py evaluation_results.csv

# Custom output path
python generate_dashboard.py evaluation_results.csv -o dashboard.html

# Generate and open in browser
python generate_dashboard.py evaluation_results.csv --open
```

**Dashboard Components**:
- 📊 Overall statistics cards
- 📈 Has Expected Answer comparison chart
- 🥧 Expected Answer pattern distribution
- 📉 Category performance breakdown
- 🔧 Top tools used
- ⏱️ Response time comparison

## 📝 Question File Format

Questions are defined in JSON format:

```json
[
  {
    "id": 1,
    "category": "Precision",
    "question": "What is the UniProt ID for human BRCA1?",
    "expected_answer": "P38398",
    "notes": "Test basic UniProt lookup",
    "mcp_servers": {
      "togomcp": {
        "type": "http",
        "url": "https://togomcp.rdfportal.org/mcp"
      }
    }
  }
]
```

### Required Fields
- `question` (string): The question text

### Recommended Fields
- `id` (number): Unique identifier
- `category` (string): One of: Precision, Completeness, Integration, Currency, Specificity, Structured Query
- `expected_answer` (string): What you expect the answer to contain
- `notes` (string): Additional context or purpose

### Optional Fields
- `mcp_servers` (object): Override default MCP configuration for this question

### Question Categories

| Category | Purpose | Example |
|----------|---------|---------|
| **Precision** | Test exact ID/value retrieval | "What is the UniProt ID for human BRCA1?" |
| **Completeness** | Test comprehensive results | "How many genes are annotated with GO:0006281?" |
| **Integration** | Test cross-database linking | "Convert UniProt P04637 to NCBI Gene ID" |
| **Currency** | Test recent/updated information | "What SARS-CoV-2 pathways are in Reactome?" |
| **Specificity** | Test niche/specialized queries | "What is the MeSH ID for Erdheim-Chester disease?" |
| **Structured Query** | Test complex multi-step queries | "Find all human kinases in UniProt with ChEMBL compounds" |

## ⚙️ Configuration

### config.json

Configure MCP servers and model settings:

```json
{
  "model": "claude-sonnet-4-20250514",
  "mcp_servers": {
    "togomcp": {
      "type": "http",
      "url": "https://togomcp.rdfportal.org/mcp"
    },
    "pubmed": {
      "type": "http",
      "url": "https://pubmed.mcp.claude.com/mcp"
    }
  }
}
```

### MCP Server Types

#### HTTP Server
```json
{
  "togomcp": {
    "type": "http",
    "url": "https://togomcp.rdfportal.org/mcp",
    "headers": {
      "Authorization": "Bearer ${API_TOKEN}"
    }
  }
}
```

#### Local stdio Server
```json
{
  "local-server": {
    "command": "npx",
    "args": ["@modelcontextprotocol/server-filesystem"],
    "env": {
      "ALLOWED_PATHS": "/path/to/data"
    }
  }
}
```

## 📊 Complete Workflow Example

### Step 1: Create Questions
```bash
# Create questions file
cat > my_questions.json << 'EOF'
[
  {
    "id": 1,
    "category": "Precision",
    "question": "What is the UniProt ID for human BRCA1?",
    "expected_answer": "P38398"
  },
  {
    "id": 2,
    "category": "Integration",
    "question": "Convert UniProt P04637 to NCBI Gene ID",
    "expected_answer": "7157"
  }
]
EOF
```

### Step 2: Validate Questions
```bash
python validate_questions.py my_questions.json --estimate-cost
```

### Step 3: Run Evaluation
```bash
python automated_test_runner.py my_questions.json -o results_$(date +%Y%m%d).csv
```

### Step 4: Analyze Results
```bash
python results_analyzer.py results_$(date +%Y%m%d).csv -v
```

### Step 5: Generate Dashboard
```bash
python generate_dashboard.py results_$(date +%Y%m%d).csv --open
```

### Step 6: Export Report
```bash
python results_analyzer.py results_$(date +%Y%m%d).csv --export analysis_$(date +%Y%m%d).md
```

## 🔍 Understanding Results

### Success Patterns

| Pattern | Interpretation | Action |
|---------|----------------|--------|
| Both have expected | Question may be too easy | Consider more complex questions |
| Only baseline has expected | TogoMCP failed | Check MCP configuration, tool availability |
| Only TogoMCP has expected | **Good!** Clear value-add | Keep this question |
| Neither has expected | Question too hard or unclear | Revise question or expected answer |

### Value-Add Assessment

The system automatically categorizes each question:

- **CRITICAL (15-18 pts)**: Baseline didn't answer OR got it wrong, TogoMCP got it right
  - Action: Use for benchmarks and publications
  
- **VALUABLE (9-14 pts)**: Both answered, but TogoMCP significantly better
  - Action: Include in evaluation set
  
- **MARGINAL (4-8 pts)**: Both answered similarly, minor TogoMCP improvement
  - Action: Consider revising or excluding
  
- **REDUNDANT (0-3 pts)**: Both answered correctly, no clear difference
  - Action: Exclude from evaluation

### Tool Usage

Good tool usage rates indicate questions are actually using the MCP servers:

- **>70%**: Excellent, questions require database access
- **50-70%**: Good, but some questions may be answerable from training data
- **<50%**: Review questions, they may be too simple or too general

## 🚨 Troubleshooting

### Common Issues

#### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

#### "claude-agent-sdk not found"
```bash
pip install claude-agent-sdk anthropic
```

#### "MCP server connection failed"
Check:
1. Server URL is correct
2. Server is online: `curl https://togomcp.rdfportal.org/mcp`
3. Network allows outbound connections
4. API tokens set (if required)

#### No tools are being used
- Questions may be too simple (answerable from training data)
- MCP servers not configured correctly
- Questions don't actually require database access

#### Low "has expected answer" rate
- Expected answers may be too specific or exact
- Questions may need revision
- Expected answer format may not match response format

## 📈 Best Practices

### Question Design
1. **Be specific**: Clear, answerable questions with verifiable results
2. **Include expected answers**: Enables automatic correctness evaluation
3. **Balance categories**: Aim for 3-5 questions per category
4. **Start small**: Test with 5-10 questions first, then scale
5. **Iterate**: Review results, refine questions, re-run

### Testing
1. **Validate first**: Always run `validate_questions.py` before evaluation
2. **Check costs**: Use `--estimate-cost` for large question sets
3. **Save results**: Use dated filenames (e.g., `results_20250117.csv`)
4. **Version control**: Track questions and configs in git

### Analysis
1. **Review statistics**: Look at overall patterns first
2. **Examine failures**: Understand why questions failed
3. **Focus on CRITICAL**: These show the clearest value-add
4. **Check tool usage**: Ensure MCP tools are being used
5. **Export reports**: Save analysis for documentation

### Iteration
1. **Fix problems first**: Address failed tests before adding more
2. **Refine questions**: Based on problematic patterns
3. **Balance categories**: Fill gaps in category coverage
4. **Document insights**: Note findings and decisions
5. **Re-evaluate**: Test improvements with updated questions

## 📁 File Structure

```
evaluation/scripts/
├── README.md                    # This file
├── QUICK_REFERENCE.md          # Quick command reference
├── automated_test_runner.py     # Main evaluation script
├── results_analyzer.py          # Results analysis script
├── validate_questions.py        # Question validation script
├── generate_dashboard.py        # Dashboard generator
├── requirements.txt             # Python dependencies
├── config.json                  # MCP configuration
├── example_questions.json       # Sample questions
├── evaluation_results.csv       # Results output (generated)
└── evaluation_dashboard.html   # Dashboard output (generated)
```

## 🔗 Related Documentation

- **[../EVALUATION_README.md](../EVALUATION_README.md)**: Overall evaluation system overview
- **[../togomcp_evaluation_rubric.md](../togomcp_evaluation_rubric.md)**: Manual evaluation methodology
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Quick command reference card

## 🤝 Contributing

When adding new features or scripts:
1. Update this README
2. Add examples to `example_questions.json`
3. Document configuration options
4. Add troubleshooting tips
5. Update QUICK_REFERENCE.md

## 📄 License

This evaluation tooling follows the same license as the main TogoMCP project.

---

**Last Updated**: December 2025  
**Version**: 2.0  
**Status**: Production-ready
