# Brainstorm Framework Examples

This file contains practical examples of using the Brainstorm Framework.

## Example 1: Quick Analysis (No API Key Required)

Get 3 improvement ideas for your current repository:

```bash
python3 brainstorm.py --num-ideas 3
```

Output:
```
🚀 Starting Brainstorm Framework...

🔍 Analyzing project direction...

📊 Project Strategy:
Vision: Strategic analysis available
Key Objectives: Improve code quality, Add features, Enhance documentation

💡 Generating 3 improvement ideas...

💡 Generated 3 ideas:
1. [test] Add comprehensive test suite (Priority: high)
2. [documentation] Improve documentation (Priority: medium)
3. [infrastructure] Add CI/CD pipeline (Priority: medium)

📝 Creating GitHub issues (dry_run=True)...

📋 Issue Preview (dry run mode):
  - Add comprehensive test suite
  - Improve documentation
  - Add CI/CD pipeline
```

## Example 2: Strategy-Only Mode

Get strategic analysis of your codebase:

```bash
python3 brainstorm.py --mode strategy
```

Output:
```json
{
  "strategy": {
    "vision": "Build a modern, extensible project management system",
    "key_objectives": [
      "Improve code quality and maintainability",
      "Add comprehensive testing",
      "Enhance documentation"
    ],
    "recommended_priorities": [
      "Focus on core functionality",
      "Build a solid foundation"
    ],
    "technical_debt_areas": [
      "Missing test coverage",
      "Limited documentation"
    ],
    "future_directions": [
      "API development",
      "Integration with external tools"
    ]
  }
}
```

## Example 3: Save Results to File

Generate ideas and save to JSON file for later use:

```bash
python3 brainstorm.py --mode ideas --num-ideas 5 --output ideas.json
```

Then you can process the ideas programmatically:
```bash
cat ideas.json | python3 -m json.tool
```

## Example 4: Using with Claude API

Set up your API key and run with Claude:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python3 brainstorm.py --provider claude --num-ideas 5
```

The AI will analyze your actual codebase and provide context-specific suggestions!

## Example 5: Using with OpenAI API

Set up OpenAI and run:

```bash
export OPENAI_API_KEY="sk-..."
python3 brainstorm.py --provider openai --num-ideas 5
```

## Example 6: Creating GitHub Issues (Requires gh CLI)

First, preview the issues (dry run):
```bash
python3 brainstorm.py --num-ideas 3
```

When satisfied, create actual issues:
```bash
python3 brainstorm.py --num-ideas 3 --create-issues
```

**Prerequisites:**
1. Install GitHub CLI: `brew install gh` or see https://cli.github.com/
2. Authenticate: `gh auth login`
3. Be in a GitHub repository

## Example 7: Analyze Different Repository

Analyze a different project:

```bash
python3 brainstorm.py --repo-path ~/projects/myapp --num-ideas 5 --output myapp-analysis.json
```

## Example 8: Integration with Existing Workflow

You can integrate this into your development workflow:

```bash
#!/bin/bash
# weekly-analysis.sh

echo "Running weekly codebase analysis..."
cd /path/to/your/project

# Generate strategic analysis
python3 /path/to/brainstorm.py --mode strategy --output strategy-$(date +%Y%m%d).json

# Generate improvement ideas
python3 /path/to/brainstorm.py --mode ideas --num-ideas 10 --output ideas-$(date +%Y%m%d).json

echo "Analysis complete! Check the generated JSON files."
```

## Example 9: Batch Processing Multiple Repositories

```bash
#!/bin/bash
# analyze-all-repos.sh

for repo in ~/projects/*/; do
    echo "Analyzing $repo"
    python3 brainstorm.py --repo-path "$repo" --num-ideas 5 --output "$(basename $repo)-ideas.json"
done
```

## Example 10: Custom Idea Count

Generate different numbers of ideas for different needs:

```bash
# Quick scan - 2 ideas
python3 brainstorm.py --num-ideas 2

# Normal analysis - 5 ideas
python3 brainstorm.py --num-ideas 5

# Deep analysis - 10 ideas
python3 brainstorm.py --num-ideas 10
```

## Tips

1. **Start Small**: Begin with 2-3 ideas to understand the output
2. **Use Dry Run**: Always preview issues before creating them
3. **Save Results**: Use `--output` to keep analysis history
4. **Regular Analysis**: Run weekly or monthly to track improvement opportunities
5. **Combine Modes**: Use strategy mode for planning, ideas mode for execution

## Troubleshooting

### "Permission denied"
```bash
chmod +x brainstorm.py
```

### "anthropic package not installed"
```bash
pip install anthropic
```

### "gh not found"
Install GitHub CLI: https://cli.github.com/

### Empty or generic results
This means you're in simulation mode (no API key). Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` for real AI analysis.
