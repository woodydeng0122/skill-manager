# skill-manager

A collection of AI IDE Skills for skill management and publishing.

- **skill-manager** — Detects installed AI IDE Skills, evaluates necessity and redundancy, and recommends high-value uninstalled Skills based on project needs.
- **skill-publisher** — Guides you to publish and submit Skills to the skills.sh directory, making them discoverable via `npx skills find`.

## Installation

```bash
npx skills add woodydeng0122/skill-manager --skill skill-manager
npx skills add woodydeng0122/skill-manager --skill skill-publisher
```

Or install manually:

```bash
git clone https://github.com/woodydeng0122/skill-manager.git skills/skill-manager
```

## Skills

### skill-manager — Skill Management Analyzer

**Trigger keywords:**
- "analyze my skills" / "skill management" / "check skills"
- "skill evaluation" / "skill recommendation" / "skill analysis"

**What it does:**

1. Scan all installed Skills in the `skills/` directory
2. Analyze the current project's tech stack and characteristics
3. Score each Skill's necessity (0-100) and detect redundancy
4. Recommend high-value uninstalled Skills (P0/P1/P2 priority)
5. Output a structured analysis report

**Run directly:**

```bash
python skills/skill-manager/scripts/skill_analyzer.py scan --skills-dir skills --project-dir .
```

### skill-publisher — Skill Publishing Guide

**Trigger keywords:**
- "publish skill" / "submit skill" / "skills find"
- "skill discovery" / "make skill discoverable" / "share skill"

**What it does:**

1. Verify your Skill's SKILL.md structure and format
2. Optimize your Skill description for better discoverability
3. Guide you through submitting to https://agentskill.sh/submit
4. Help set up GitHub webhook for auto-sync
5. Verify your Skill is discoverable via `npx skills find`

## Directory Structure

```
skills/
├── skill-manager/
│   ├── SKILL.md              # Skill definition file
│   └── scripts/
│       └── skill_analyzer.py # Core analysis engine (pure Python stdlib, zero dependencies)
└── skill-publisher/
    └── SKILL.md              # Skill publishing guide
```

## License

MIT
