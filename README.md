# Niuma Skills

Reusable AI agent skills for [NanoClaw](https://github.com/anthropics/nanoclaw) / OpenClaw and other Claude-based agents.

Each skill is a self-contained directory with a `SKILL.md` that agents can read and use via Bash tools.

## Available Skills

| Skill | Description |
|-------|-------------|
| [twitter-manager](./twitter-manager/) | Manage X (Twitter) — post, read timeline, search, like, reply, retweet, bookmarks |

## Usage

### Manual Install

Copy the skill directory into your agent's skills folder:

```bash
# NanoClaw
cp -r twitter-manager /path/to/nanoclaw/container/skills/

# OpenClaw / Claude Code
cp -r twitter-manager /path/to/project/.claude/skills/
```

### Quick Install (curl)

```bash
# Install a single skill
SKILL=twitter-manager
curl -sL https://github.com/iknowu10/niuma-skills/archive/main.tar.gz \
  | tar xz --strip-components=2 -C container/skills/ "niuma-skills-main/$SKILL"
```

## Skill Structure

Each skill follows this format:

```
skill-name/
├── SKILL.md          # Agent instructions (frontmatter + docs)
└── scripts/          # Optional helper scripts
    └── *.py / *.sh
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
description: What this skill does. When to trigger it.
allowed-tools: Bash(skill-prefix:*)
---
```

## Environment Variables

Skills use environment variables for credentials — never hardcoded. Check each skill's SKILL.md for required variables.

## Contributing

1. Create a new directory with your skill name
2. Add a `SKILL.md` following the format above
3. Keep it generic and desensitized — no tokens, passwords, or company-specific values
4. Submit a PR
