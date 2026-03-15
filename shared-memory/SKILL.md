---
name: shared-memory
description: Read and write shared memory across NanoClaw and OpenClaw instances. Use to recall user preferences, project facts, past decisions, and key entities. Supports semantic search via Nowledge Mem.
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(tee:*), Bash(rm:*), Bash(curl:*), Read, Write
---

# Shared Memory

Two storage backends — use both when writing, prefer Nowledge Mem for searching.

## 1. Nowledge Mem (semantic search)

A semantic memory service with a REST API. Set `NOWLEDGE_MEM_URL` in your `.env` to the base URL of your Nowledge Mem instance.

### Search (preferred over file grep)

```bash
# Try Nowledge Mem first; fall back to file grep if unavailable
if [ -n "$NOWLEDGE_MEM_URL" ]; then
  curl -s --max-time 5 -X POST "$NOWLEDGE_MEM_URL/memories/search" \
    -H "Content-Type: application/json" \
    -d '{"query": "search terms here", "limit": 5}' | python3 -m json.tool
else
  echo "[NOWLEDGE_MEM_URL not set, searching files]"
  grep -ril "search terms" /workspace/shared-memory/ 2>/dev/null | xargs cat 2>/dev/null
fi
```

### Write

```bash
[ -n "$NOWLEDGE_MEM_URL" ] && curl -s -X POST "$NOWLEDGE_MEM_URL/memories" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User prefers TypeScript over Python for backend services.",
    "title": "Language Preference: TypeScript",
    "importance": 0.7,
    "metadata": {"source": "nanoclaw", "category": "preference"}
  }' | python3 -m json.tool
```

### Read by ID

```bash
[ -n "$NOWLEDGE_MEM_URL" ] && curl -s "$NOWLEDGE_MEM_URL/memories/MEMORY_ID" | python3 -m json.tool
```

## 2. Shared Files (sync between instances)

Directory: `/workspace/shared-memory/`

Files can be synced between agent instances via any file sync tool.

### Read files

```bash
cat /workspace/shared-memory/*.md
```

### Write file

```bash
cat > /workspace/shared-memory/category-short-description.md << 'EOF'
---
source: nanoclaw
created: 2026-03-13
category: preference
---
Jun prefers TypeScript over Python for backend services.
EOF
```

### Delete file

```bash
rm /workspace/shared-memory/outdated-file.md
```

## Write workflow

**Always write the file first** (guaranteed to work), then try Nowledge Mem:

```bash
# Step 1: Write file (always succeeds)
cat > /workspace/shared-memory/category-short-description.md << 'EOF'
---
source: nanoclaw
created: 2026-03-13
category: fact
---
Memory content here.
EOF

# Step 2: Try Nowledge Mem (timeout 5s, ignore failure)
[ -n "$NOWLEDGE_MEM_URL" ] && curl -s --max-time 5 -X POST "$NOWLEDGE_MEM_URL/memories" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Memory content here.",
    "title": "Short Title",
    "importance": 0.7,
    "metadata": {"source": "nanoclaw@mac", "category": "fact"}
  }' || echo "[nowledge-mem unavailable, file-only write]"
```

If curl fails or times out, the file write is already done — no data loss.

## File format

```markdown
---
source: nanoclaw
created: 2026-03-13
category: fact
---
Memory content here.
```

Categories: `preference`, `fact`, `decision`, `entity`, `other`

## When to use

- **Search** Nowledge Mem when user references past conversations, decisions, or knowledge
- **Write** when you learn something about the user, project, or decisions that other instances should know
- **Read files** when checking what OpenClaw has written recently
- Do NOT store: conversation-specific context, session state, ephemeral task details, or instance identity info
