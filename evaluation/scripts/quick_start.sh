#!/bin/bash
# Quick Start Script for TogoMCP Evaluation

set -e

echo "============================================="
echo "TogoMCP Evaluation - Quick Start"
echo "============================================="
echo ""

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: ANTHROPIC_API_KEY not set"
    echo ""
    echo "Please set your API key:"
    echo "  export ANTHROPIC_API_KEY='sk-ant-your-key-here'"
    echo ""
    exit 1
fi

echo "✅ API key found"

# Check if claude-agent-sdk is installed
if ! python3 -c "import claude_agent_sdk" 2>/dev/null; then
    echo ""
    echo "📦 Installing required packages..."
    pip install -r requirements.txt
else
    echo "✅ claude-agent-sdk installed"
fi

# Check if anthropic is installed
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo "📦 Installing anthropic..."
    pip install anthropic
else
    echo "✅ anthropic installed"
fi

# Check if pandas is installed (for compute_costs.py)
if ! python3 -c "import pandas" 2>/dev/null; then
    echo "📦 Installing pandas..."
    pip install pandas
else
    echo "✅ pandas installed"
fi

echo ""
echo "============================================="
echo "Step 1: Running Evaluation"
echo "============================================="
echo ""
echo "Testing with example questions..."
echo ""

# Run the test runner
python3 automated_test_runner.py example_questions.json

echo ""
echo "============================================="
echo "Step 2: Calculating Costs"
echo "============================================="
echo ""

# Calculate costs
python3 compute_costs.py evaluation_results.csv

echo ""
echo "============================================="
echo "Step 3: Analyzing Results"
echo "============================================="
echo ""

# Analyze results
python3 results_analyzer.py evaluation_results.csv

echo ""
echo "============================================="
echo "✅ Evaluation Complete!"
echo "============================================="
echo ""
echo "📊 Results saved to: evaluation_results.csv"
echo ""
echo "Next steps:"
echo "  1. Review results: open evaluation_results.csv"
echo "  2. Check cost breakdown above"
echo "  3. Generate dashboard: python3 generate_dashboard.py evaluation_results.csv --open"
echo "  4. Create your own questions: cp example_questions.json my_questions.json"
echo ""
echo "Documentation:"
echo "  - README.md - Complete usage guide with cost analysis"
echo "  - QUICK_REFERENCE.md - Quick command reference"
echo "  - QUESTION_FORMAT.md - Question file format"
echo ""
echo "Cost information:"
echo "  - Per question: ~\$0.055 (\$0.002 baseline + \$0.053 TogoMCP)"
echo "  - Uses isolated sessions for optimal cache efficiency"
echo "  - Cache costs are stable and predictable"
echo ""