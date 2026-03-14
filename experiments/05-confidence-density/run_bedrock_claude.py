#!/usr/bin/env python3
"""
Experiment 05: Confidence Density — Claude model family sweep via Bedrock.

Runs all available Claude models through inference profiles.
Complements run_bedrock.py which covers non-Anthropic models.

Usage:
    python run_bedrock_claude.py              # All Claude models
    python run_bedrock_claude.py --dry-run    # Show what would run
    python run_bedrock_claude.py --max-tasks 2  # Quick test
"""

import sys
from pathlib import Path

# Reuse everything from run_bedrock
sys.path.insert(0, str(Path(__file__).parent))
from run_bedrock import (
    run_sweep,
    load_tasks,
)

CLAUDE_MODELS = [
    # Claude 3 family
    {"id": "us.anthropic.claude-3-haiku-20240307-v1:0", "name": "Claude 3 Haiku", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-3-sonnet-20240229-v1:0", "name": "Claude 3 Sonnet", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-3-opus-20240229-v1:0", "name": "Claude 3 Opus", "provider": "Anthropic"},
    # Claude 3.5 family
    {"id": "us.anthropic.claude-3-5-haiku-20241022-v1:0", "name": "Claude 3.5 Haiku", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0", "name": "Claude 3.5 Sonnet v2", "provider": "Anthropic"},
    # Claude 3.7
    {"id": "us.anthropic.claude-3-7-sonnet-20250219-v1:0", "name": "Claude 3.7 Sonnet", "provider": "Anthropic"},
    # Claude 4 family
    {"id": "us.anthropic.claude-sonnet-4-20250514-v1:0", "name": "Claude Sonnet 4", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-opus-4-20250514-v1:0", "name": "Claude Opus 4", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-opus-4-1-20250805-v1:0", "name": "Claude Opus 4.1", "provider": "Anthropic"},
    # Claude 4.5 family
    {"id": "us.anthropic.claude-haiku-4-5-20251001-v1:0", "name": "Claude Haiku 4.5", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-sonnet-4-5-20250929-v1:0", "name": "Claude Sonnet 4.5", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-opus-4-5-20251101-v1:0", "name": "Claude Opus 4.5", "provider": "Anthropic"},
    # Claude 4.6 family (latest)
    {"id": "us.anthropic.claude-sonnet-4-6", "name": "Claude Sonnet 4.6", "provider": "Anthropic"},
    {"id": "us.anthropic.claude-opus-4-6-v1", "name": "Claude Opus 4.6", "provider": "Anthropic"},
]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Exp 05: Confidence density — Claude family sweep"
    )
    parser.add_argument("--category", choices=["factual", "summarization", "judgment", "creative"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-tasks", type=int)
    args = parser.parse_args()

    tasks = load_tasks(args.category)
    if args.max_tasks:
        tasks = tasks[:args.max_tasks]

    run_sweep(CLAUDE_MODELS, tasks, args.dry_run)
