#!/usr/bin/env python3
"""
Brainstorm Framework - AI-powered codebase analysis and issue generation

This script provides three main functionalities:
0. Project Manager Mode: High-level strategic analysis of codebase direction
1. Idea Generator: Generate K improvement ideas for the codebase
2. Issue Creator: Convert ideas into GitHub issues automatically
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ImprovementIdea:
    """Represents a single improvement idea for the codebase"""
    title: str
    description: str
    category: str  # e.g., "feature", "refactor", "bug", "documentation", "test"
    priority: str  # e.g., "low", "medium", "high"
    estimated_effort: str  # e.g., "small", "medium", "large"
    tags: List[str]
    rationale: str


@dataclass
class ProjectStrategy:
    """Represents strategic direction for the project"""
    vision: str
    key_objectives: List[str]
    recommended_priorities: List[str]
    technical_debt_areas: List[str]
    future_directions: List[str]


class CodebaseAnalyzer:
    """Analyzes codebase structure and content"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        
    def get_file_tree(self, max_depth: int = 3) -> str:
        """Get directory structure of the repository"""
        try:
            result = subprocess.run(
                ["find", str(self.repo_path), "-type", "f", "-name", "*.py"],
                capture_output=True,
                text=True,
                timeout=10
            )
            files = result.stdout.strip().split('\n')
            # Filter out hidden and build directories
            files = [f for f in files if not any(
                part.startswith('.') or part in ['__pycache__', 'venv', 'env', 'node_modules']
                for part in Path(f).parts
            )]
            return '\n'.join(files[:50])  # Limit to 50 files
        except Exception as e:
            return f"Error getting file tree: {e}"
    
    def read_key_files(self) -> Dict[str, str]:
        """Read important files like README, main scripts, etc."""
        key_files = {}
        
        # Look for README
        for readme in ['README.md', 'README.txt', 'README']:
            readme_path = self.repo_path / readme
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        key_files[readme] = f.read()
                except Exception:
                    pass
        
        # Look for main Python files
        for py_file in self.repo_path.glob('*.py'):
            if py_file.name not in ['setup.py', '__init__.py']:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Limit content size
                        if len(content) < 10000:
                            key_files[py_file.name] = content
                except Exception:
                    pass
        
        return key_files
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Gather general repository information"""
        info = {
            "path": str(self.repo_path),
            "file_tree": self.get_file_tree(),
            "key_files": self.read_key_files(),
        }
        
        # Try to get git info
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                info["is_git_repo"] = True
                
                # Get recent commits
                result = subprocess.run(
                    ["git", "log", "--oneline", "-10"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    info["recent_commits"] = result.stdout.strip()
        except Exception:
            info["is_git_repo"] = False
        
        return info


class AIProvider:
    """Base class for AI providers (Claude, OpenAI, etc.)"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or self._get_api_key_from_env()
        self.model = model
        
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables"""
        # Try multiple environment variable names
        for env_var in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'AI_API_KEY']:
            key = os.environ.get(env_var)
            if key:
                return key
        return None
    
    def call_ai(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Make API call to AI provider - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement call_ai")


class ClaudeProvider(AIProvider):
    """Claude API provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(api_key, model)
        
    def call_ai(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Claude API"""
        if not self.api_key:
            return self._simulate_response(prompt)
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt or "You are a helpful AI assistant for code analysis.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except ImportError:
            print("Warning: anthropic package not installed. Install with: pip install anthropic")
            return self._simulate_response(prompt)
        except Exception as e:
            print(f"Warning: Error calling Claude API: {e}")
            return self._simulate_response(prompt)
    
    def _simulate_response(self, prompt: str) -> str:
        """Simulate AI response when API is not available"""
        # Check if this is an idea generation request
        if "improvement ideas" in prompt.lower():
            # Return empty array to trigger fallback ideas
            return "[]"
        # For strategy analysis
        return json.dumps({
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
        })


class OpenAIProvider(AIProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        super().__init__(api_key, model)
        
    def call_ai(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call OpenAI API"""
        if not self.api_key:
            return self._simulate_response(prompt)
        
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except ImportError:
            print("Warning: openai package not installed. Install with: pip install openai")
            return self._simulate_response(prompt)
        except Exception as e:
            print(f"Warning: Error calling OpenAI API: {e}")
            return self._simulate_response(prompt)
    
    def _simulate_response(self, prompt: str) -> str:
        """Simulate AI response when API is not available"""
        # Check if this is an idea generation request
        if "improvement ideas" in prompt.lower():
            # Return empty array to trigger fallback ideas
            return "[]"
        # For strategy analysis
        return json.dumps({
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
        })


class ProjectManagerAI:
    """Component 0: High-level strategic project management"""
    
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider
        
    def analyze_project_direction(self, repo_info: Dict[str, Any]) -> ProjectStrategy:
        """Analyze project and provide strategic direction"""
        
        system_prompt = """You are an experienced technical project manager and software architect.
Your role is to analyze codebases and provide strategic direction for their evolution.
Focus on: vision, key objectives, priorities, technical debt, and future directions."""
        
        prompt = f"""Analyze this codebase and provide strategic guidance:

Repository Information:
{json.dumps(repo_info, indent=2)}

Please provide a strategic analysis in JSON format with:
- vision: A clear vision for where this project should go
- key_objectives: List of 3-5 key objectives
- recommended_priorities: What should be prioritized now
- technical_debt_areas: Areas that need attention
- future_directions: Potential future directions for the project

Respond ONLY with valid JSON."""
        
        response = self.ai.call_ai(prompt, system_prompt)
        
        # Parse response
        try:
            data = json.loads(response)
            return ProjectStrategy(
                vision=data.get("vision", ""),
                key_objectives=data.get("key_objectives", []),
                recommended_priorities=data.get("recommended_priorities", []),
                technical_debt_areas=data.get("technical_debt_areas", []),
                future_directions=data.get("future_directions", [])
            )
        except json.JSONDecodeError:
            # Fallback if response is not JSON
            return ProjectStrategy(
                vision="Strategic analysis available",
                key_objectives=["Improve code quality", "Add features", "Enhance documentation"],
                recommended_priorities=["Focus on core functionality"],
                technical_debt_areas=["Areas to be analyzed"],
                future_directions=["Continue development"]
            )


class IdeaGenerator:
    """Component 1: Generate improvement ideas"""
    
    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider
        
    def generate_ideas(self, repo_info: Dict[str, Any], num_ideas: int = 5) -> List[ImprovementIdea]:
        """Generate K improvement ideas for the codebase"""
        
        system_prompt = """You are an expert software engineer and code reviewer.
Your role is to analyze codebases and suggest concrete, actionable improvements.
Focus on practical ideas that add value: features, refactorings, tests, documentation, etc."""
        
        prompt = f"""Analyze this codebase and generate exactly {num_ideas} improvement ideas:

Repository Information:
{json.dumps(repo_info, indent=2)}

For each idea, provide:
- title: Clear, concise title
- description: Detailed description of the improvement
- category: One of [feature, refactor, bug, documentation, test, infrastructure]
- priority: One of [low, medium, high]
- estimated_effort: One of [small, medium, large]
- tags: List of relevant tags
- rationale: Why this improvement is valuable

Respond with a JSON array of exactly {num_ideas} ideas, each following the structure above.
Respond ONLY with valid JSON array."""
        
        response = self.ai.call_ai(prompt, system_prompt)
        
        # Parse response
        try:
            data = json.loads(response)
            ideas = []
            # Handle both array and object responses
            items = data if isinstance(data, list) else [data]
            
            # If no items or empty response, use fallback
            if not items:
                return self._generate_fallback_ideas(num_ideas)
            
            for item in items[:num_ideas]:
                ideas.append(ImprovementIdea(
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    category=item.get("category", "feature"),
                    priority=item.get("priority", "medium"),
                    estimated_effort=item.get("estimated_effort", "medium"),
                    tags=item.get("tags", []),
                    rationale=item.get("rationale", "")
                ))
            
            # If we got valid items but they're empty, use fallback
            if ideas and not ideas[0].title:
                return self._generate_fallback_ideas(num_ideas)
                
            return ideas
        except (json.JSONDecodeError, KeyError, TypeError):
            # Fallback ideas if response is not JSON
            return self._generate_fallback_ideas(num_ideas)
    
    def _generate_fallback_ideas(self, num_ideas: int) -> List[ImprovementIdea]:
        """Generate fallback ideas when AI is not available"""
        fallback_ideas = [
            ImprovementIdea(
                title="Add comprehensive test suite",
                description="Create unit tests and integration tests to improve code quality and reliability",
                category="test",
                priority="high",
                estimated_effort="medium",
                tags=["testing", "quality"],
                rationale="Tests ensure code correctness and make refactoring safer"
            ),
            ImprovementIdea(
                title="Improve documentation",
                description="Add docstrings, README improvements, and usage examples",
                category="documentation",
                priority="medium",
                estimated_effort="small",
                tags=["docs", "usability"],
                rationale="Good documentation makes the project more accessible"
            ),
            ImprovementIdea(
                title="Add CI/CD pipeline",
                description="Set up automated testing and deployment workflow",
                category="infrastructure",
                priority="medium",
                estimated_effort="medium",
                tags=["ci", "automation"],
                rationale="Automation improves development velocity and code quality"
            ),
            ImprovementIdea(
                title="Refactor core modules",
                description="Improve code organization and reduce technical debt",
                category="refactor",
                priority="low",
                estimated_effort="large",
                tags=["refactor", "quality"],
                rationale="Clean code is easier to maintain and extend"
            ),
            ImprovementIdea(
                title="Add new features",
                description="Implement features requested by users or identified gaps",
                category="feature",
                priority="medium",
                estimated_effort="medium",
                tags=["feature", "enhancement"],
                rationale="New features increase project value and adoption"
            ),
        ]
        return fallback_ideas[:num_ideas]


class GitHubIssueCreator:
    """Component 2: Create GitHub issues from ideas"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        
    def create_issue(self, idea: ImprovementIdea, dry_run: bool = True) -> Dict[str, Any]:
        """Create a GitHub issue from an improvement idea"""
        
        # Format issue body
        issue_body = f"""{idea.description}

## Rationale
{idea.rationale}

## Details
- **Category**: {idea.category}
- **Priority**: {idea.priority}
- **Estimated Effort**: {idea.estimated_effort}
- **Tags**: {', '.join(idea.tags)}

---
*This issue was automatically generated by the Brainstorm Framework*
"""
        
        if dry_run:
            return {
                "status": "dry_run",
                "title": idea.title,
                "body": issue_body,
                "labels": [idea.category, f"priority-{idea.priority}"]
            }
        
        # Try to create actual GitHub issue using gh CLI
        try:
            labels = [idea.category, f"priority-{idea.priority}"] + idea.tags
            label_args = []
            for label in labels:
                label_args.extend(["--label", label])
            
            cmd = [
                "gh", "issue", "create",
                "--title", idea.title,
                "--body", issue_body
            ] + label_args
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    "status": "created",
                    "title": idea.title,
                    "url": result.stdout.strip()
                }
            else:
                return {
                    "status": "error",
                    "title": idea.title,
                    "error": result.stderr
                }
        except FileNotFoundError:
            return {
                "status": "error",
                "title": idea.title,
                "error": "gh CLI not found. Install from: https://cli.github.com/"
            }
        except Exception as e:
            return {
                "status": "error",
                "title": idea.title,
                "error": str(e)
            }
    
    def create_issues_batch(self, ideas: List[ImprovementIdea], dry_run: bool = True) -> List[Dict[str, Any]]:
        """Create multiple GitHub issues"""
        results = []
        for idea in ideas:
            result = self.create_issue(idea, dry_run=dry_run)
            results.append(result)
        return results


class BrainstormFramework:
    """Main orchestrator for the brainstorm framework"""
    
    def __init__(self, repo_path: str = ".", provider: str = "claude", api_key: Optional[str] = None):
        self.repo_path = repo_path
        self.analyzer = CodebaseAnalyzer(repo_path)
        
        # Initialize AI provider
        if provider.lower() == "claude":
            self.ai_provider = ClaudeProvider(api_key)
        elif provider.lower() in ["openai", "gpt"]:
            self.ai_provider = OpenAIProvider(api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'claude' or 'openai'")
        
        self.project_manager = ProjectManagerAI(self.ai_provider)
        self.idea_generator = IdeaGenerator(self.ai_provider)
        self.issue_creator = GitHubIssueCreator(repo_path)
    
    def run_project_analysis(self) -> ProjectStrategy:
        """Run Component 0: Project Manager analysis"""
        print("🔍 Analyzing project direction...")
        repo_info = self.analyzer.get_repository_info()
        strategy = self.project_manager.analyze_project_direction(repo_info)
        return strategy
    
    def run_idea_generation(self, num_ideas: int = 5) -> List[ImprovementIdea]:
        """Run Component 1: Generate improvement ideas"""
        print(f"💡 Generating {num_ideas} improvement ideas...")
        repo_info = self.analyzer.get_repository_info()
        ideas = self.idea_generator.generate_ideas(repo_info, num_ideas)
        return ideas
    
    def run_issue_creation(self, ideas: List[ImprovementIdea], dry_run: bool = True) -> List[Dict[str, Any]]:
        """Run Component 2: Create GitHub issues"""
        print(f"📝 Creating GitHub issues (dry_run={dry_run})...")
        results = self.issue_creator.create_issues_batch(ideas, dry_run)
        return results
    
    def run_full_pipeline(self, num_ideas: int = 5, create_issues: bool = False) -> Dict[str, Any]:
        """Run the complete brainstorm pipeline"""
        print("🚀 Starting Brainstorm Framework...")
        print()
        
        # Component 0: Strategic analysis
        strategy = self.run_project_analysis()
        print("\n📊 Project Strategy:")
        print(f"Vision: {strategy.vision}")
        print(f"Key Objectives: {', '.join(strategy.key_objectives[:3])}")
        print()
        
        # Component 1: Generate ideas
        ideas = self.run_idea_generation(num_ideas)
        print(f"\n💡 Generated {len(ideas)} ideas:")
        for i, idea in enumerate(ideas, 1):
            print(f"{i}. [{idea.category}] {idea.title} (Priority: {idea.priority})")
        print()
        
        # Component 2: Create issues
        dry_run = not create_issues
        results = self.run_issue_creation(ideas, dry_run=dry_run)
        
        if dry_run:
            print("\n📋 Issue Preview (dry run mode):")
            for result in results:
                print(f"  - {result['title']}")
        else:
            print("\n✅ Issues Created:")
            for result in results:
                if result["status"] == "created":
                    print(f"  ✓ {result['title']}: {result.get('url', 'N/A')}")
                else:
                    print(f"  ✗ {result['title']}: {result.get('error', 'Unknown error')}")
        
        return {
            "strategy": asdict(strategy),
            "ideas": [asdict(idea) for idea in ideas],
            "issue_results": results
        }


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Brainstorm Framework - AI-powered codebase analysis and issue generation"
    )
    
    parser.add_argument(
        "--mode",
        choices=["all", "strategy", "ideas", "issues"],
        default="all",
        help="Which component to run (default: all)"
    )
    
    parser.add_argument(
        "--num-ideas",
        type=int,
        default=5,
        help="Number of ideas to generate (default: 5)"
    )
    
    parser.add_argument(
        "--provider",
        choices=["claude", "openai"],
        default="claude",
        help="AI provider to use (default: claude)"
    )
    
    parser.add_argument(
        "--api-key",
        help="API key for the AI provider (or set ANTHROPIC_API_KEY/OPENAI_API_KEY env var)"
    )
    
    parser.add_argument(
        "--repo-path",
        default=".",
        help="Path to the repository (default: current directory)"
    )
    
    parser.add_argument(
        "--create-issues",
        action="store_true",
        help="Actually create GitHub issues (default: dry run)"
    )
    
    parser.add_argument(
        "--output",
        help="Save results to JSON file"
    )
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = BrainstormFramework(
        repo_path=args.repo_path,
        provider=args.provider,
        api_key=args.api_key
    )
    
    results = {}
    
    # Run selected mode
    if args.mode == "all":
        results = framework.run_full_pipeline(
            num_ideas=args.num_ideas,
            create_issues=args.create_issues
        )
    elif args.mode == "strategy":
        strategy = framework.run_project_analysis()
        results = {"strategy": asdict(strategy)}
        print("\n📊 Project Strategy:")
        print(json.dumps(results, indent=2))
    elif args.mode == "ideas":
        ideas = framework.run_idea_generation(args.num_ideas)
        results = {"ideas": [asdict(idea) for idea in ideas]}
        print("\n💡 Generated Ideas:")
        print(json.dumps(results, indent=2))
    elif args.mode == "issues":
        # For issues-only mode, need to load ideas from somewhere
        print("Error: 'issues' mode requires ideas. Use 'all' or 'ideas' mode first.")
        sys.exit(1)
    
    # Save results if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dumps(results, f, indent=2)
        print(f"\n💾 Results saved to {args.output}")
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()
