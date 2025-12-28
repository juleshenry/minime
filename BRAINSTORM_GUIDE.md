# Brainstorm Framework Guide

The Brainstorm Framework is an AI-powered tool for analyzing codebases and generating improvement ideas that can be automatically converted into GitHub issues.

## Overview

The framework consists of three main components:

### Component 0: Project Manager AI
Provides high-level strategic analysis of your codebase, including:
- Vision and direction for the project
- Key objectives
- Recommended priorities
- Technical debt areas
- Future directions

### Component 1: Idea Generator
Analyzes your codebase and generates K actionable improvement ideas:
- Features
- Refactorings
- Bug fixes
- Documentation improvements
- Test additions
- Infrastructure enhancements

Each idea includes:
- Title and description
- Category and priority
- Estimated effort
- Tags
- Rationale

### Component 2: Issue Creator
Converts generated ideas into GitHub issues automatically:
- Creates well-formatted issues
- Adds appropriate labels
- Includes full context and rationale
- Supports dry-run mode for preview

## Installation

### Basic Setup
```bash
# Clone the repository
git clone https://github.com/juleshenry/minime.git
cd minime

# Make the script executable
chmod +x brainstorm.py
```

### Optional Dependencies

For Claude API support:
```bash
pip install anthropic
```

For OpenAI API support:
```bash
pip install openai
```

**Note:** The script works without API keys in simulation mode using fallback ideas.

## Usage

### Basic Usage

Run the full pipeline (without API keys - uses simulation mode):
```bash
python3 brainstorm.py
```

Generate 5 ideas:
```bash
python3 brainstorm.py --num-ideas 5
```

### Component Modes

Run only strategic analysis:
```bash
python3 brainstorm.py --mode strategy
```

Generate ideas only:
```bash
python3 brainstorm.py --mode ideas --num-ideas 3
```

Run full pipeline:
```bash
python3 brainstorm.py --mode all --num-ideas 5
```

### With AI Providers

Using Claude (recommended):
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
python3 brainstorm.py --provider claude --num-ideas 5
```

Using OpenAI:
```bash
export OPENAI_API_KEY="your-api-key-here"
python3 brainstorm.py --provider openai --num-ideas 5
```

Pass API key directly:
```bash
python3 brainstorm.py --api-key "your-key" --provider claude
```

### Creating GitHub Issues

Preview issues (dry run - default):
```bash
python3 brainstorm.py --num-ideas 3
```

Actually create GitHub issues (requires `gh` CLI):
```bash
python3 brainstorm.py --num-ideas 3 --create-issues
```

**Note:** To create actual issues, you need:
1. The GitHub CLI (`gh`) installed: https://cli.github.com/
2. Be authenticated: `gh auth login`
3. Run the command with `--create-issues` flag

### Save Results to File

```bash
python3 brainstorm.py --output results.json --num-ideas 5
```

### Analyze Different Repository

```bash
python3 brainstorm.py --repo-path /path/to/repo --num-ideas 3
```

## Command-Line Options

```
--mode {all,strategy,ideas,issues}
    Which component to run (default: all)

--num-ideas NUM_IDEAS
    Number of ideas to generate (default: 5)

--provider {claude,openai}
    AI provider to use (default: claude)

--api-key API_KEY
    API key for the AI provider

--repo-path REPO_PATH
    Path to the repository (default: current directory)

--create-issues
    Actually create GitHub issues (default: dry run)

--output OUTPUT
    Save results to JSON file
```

## Examples

### Example 1: Quick Analysis
```bash
# Get 3 improvement ideas for current repo
python3 brainstorm.py --num-ideas 3
```

### Example 2: Full Strategic Analysis with Claude
```bash
# Set up API key
export ANTHROPIC_API_KEY="your-key"

# Run full analysis and save results
python3 brainstorm.py --mode all --num-ideas 5 --output analysis.json
```

### Example 3: Generate and Create Issues
```bash
# Generate ideas and create GitHub issues
python3 brainstorm.py --num-ideas 3 --create-issues
```

### Example 4: Analyze External Repository
```bash
# Analyze a different repository
python3 brainstorm.py --repo-path ~/projects/myapp --num-ideas 5
```

## Output Format

### Strategy Output
```json
{
  "strategy": {
    "vision": "Project vision statement",
    "key_objectives": ["objective1", "objective2"],
    "recommended_priorities": ["priority1", "priority2"],
    "technical_debt_areas": ["debt1", "debt2"],
    "future_directions": ["direction1", "direction2"]
  }
}
```

### Ideas Output
```json
{
  "ideas": [
    {
      "title": "Add comprehensive test suite",
      "description": "Create unit tests and integration tests...",
      "category": "test",
      "priority": "high",
      "estimated_effort": "medium",
      "tags": ["testing", "quality"],
      "rationale": "Tests ensure code correctness..."
    }
  ]
}
```

### Issue Creation Output
```json
{
  "issue_results": [
    {
      "status": "created",
      "title": "Add comprehensive test suite",
      "url": "https://github.com/owner/repo/issues/123"
    }
  ]
}
```

## Simulation Mode

When no API key is provided, the framework operates in simulation mode:
- Uses predefined strategic analysis
- Generates fallback improvement ideas
- All features work without external API calls
- Perfect for testing and demonstration

## Best Practices

1. **Start with Strategy Mode**: Run `--mode strategy` first to understand high-level direction
2. **Iterate on Ideas**: Generate different numbers of ideas to find the right balance
3. **Use Dry Run**: Always preview issues before creating them
4. **Save Results**: Use `--output` to keep records of analyses
5. **Regular Analysis**: Run periodically to keep track of improvement opportunities

## Troubleshooting

### "anthropic package not installed"
```bash
pip install anthropic
```

### "openai package not installed"
```bash
pip install openai
```

### "gh CLI not found"
Install from: https://cli.github.com/

### API Key Issues
Make sure your API key is set:
```bash
export ANTHROPIC_API_KEY="your-key"
# or
export OPENAI_API_KEY="your-key"
```

## Integration with Minime

This framework integrates seamlessly with the Minime project management system:
- Generated ideas can be imported into the BoardManager
- Issues can be tracked through the Minime workflow
- Combines AI-powered planning with structured project management

## Contributing

The Brainstorm Framework is part of the Minime project. Contributions are welcome!

## License

Same as the Minime project.
