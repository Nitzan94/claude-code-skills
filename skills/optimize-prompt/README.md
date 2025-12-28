# Optimize Prompt (GEPA)

A Claude Code skill that optimizes prompts using Genetic-Pareto Evolution. Give it a prompt and test cases, it evolves the prompt until it hits your target accuracy.

## How It Works

GEPA (Genetic-Pareto Evolution for AI) uses four techniques:

1. **Pareto Frontier** - Maintains a pool of prompts that excel on different test cases
2. **Trace-Based Reflection** - Analyzes full reasoning chains, not just outputs
3. **Crossover Mutations** - Merges insights from multiple successful prompts
4. **Diversity Pressure** - Prevents premature convergence to local optima

## Usage

In Claude Code:
```
/optimize-prompt

Seed: "Extract action items from text"

Test cases:
- Input: "John will send report by Friday"
  Expected: "- John: Send report (Due: Friday)"

- Input: "We should improve the process sometime"
  Expected: ""
```

## What You Get

After optimization:

| Metric | Example |
|--------|---------|
| Baseline Score | 40% |
| Final Score | 92% |
| Iterations | 3 |
| Key Discoveries | "Model doesn't know to skip vague items" |

Plus the optimized prompt with explicit rules added based on failure analysis.

## Scoring

The optimizer scores each output 0-10:
- 10: Perfect match (content AND format)
- 7-8: Correct content, minor format differences
- 3-4: Partial content, significant omissions
- 0: Completely wrong

## When to Use

- You have a prompt that works sometimes but not consistently
- You have examples of desired input/output pairs
- You want to find edge cases your prompt doesn't handle

## Minimum Input

- 1 seed prompt
- 1 test case (optimizer will generate synthetic edge cases)

Recommended: 5-10 test cases for robust optimization.
