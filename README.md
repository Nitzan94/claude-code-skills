# Claude Code Skills

A collection of skills for Claude Code - specialized knowledge modules that turn Claude into an expert at specific tasks.

## What are Skills?

Skills are markdown files that give Claude Code domain expertise. Instead of explaining what you want every time, you invoke a skill and Claude knows exactly what to do.

## Available Skills

| Skill | Description |
|-------|-------------|
| [sync-context](skills/sync-context/) | End-of-session context sync. Reviews what was learned and persists it into project context files so the next session starts up to date. |
| [skill-tutor](skills/skill-tutor/) | Personal AI tutor with spaced repetition. Creates tutorials using YOUR projects, tracks learning progress, quizzes you at optimal intervals. |
| [optimize-prompt](skills/optimize-prompt/) | Evolves prompts using genetic algorithms. Give it test cases, it finds the prompt that works. |
| [deploy-agentcore](skills/deploy-agentcore/) | Deploy Python agents to AWS Bedrock AgentCore. Serverless hosting with memory, auth, and observability. |
| [chrome-extension](skills/chrome-extension/) | Build Chrome extensions with Manifest V3. Scaffolding, patterns, debugging. |

## Installation

Copy any skill folder to your Claude Code skills directory:

```bash
# Clone the repo
git clone https://github.com/Nitzan94/claude-code-skills.git

# Copy a skill (example: skill-tutor)
cp -r claude-code-skills/skills/skill-tutor ~/.claude/skills/
```

Or copy all skills:
```bash
cp -r claude-code-skills/skills/* ~/.claude/skills/
```

## Usage

In Claude Code, either:
- Invoke directly: `/skill-tutor`, `/optimize-prompt`, etc.
- Use trigger phrases: "teach me", "optimize this prompt", "deploy to agentcore"

## Creating Your Own Skills

Each skill is a folder with:
```
skill-name/
├── SKILL.md          # Main skill definition (required)
├── README.md         # Documentation
├── references/       # Domain knowledge files
├── workflows/        # Step-by-step guides
├── templates/        # Code templates
└── scripts/          # Helper scripts
```

See any skill folder for examples.

## License

MIT
