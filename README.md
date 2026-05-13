# skill-manager

Skill Management Analyzer — Detects installed AI IDE Skills, evaluates necessity and redundancy, and recommends high-value uninstalled Skills based on project needs.

## Installation

```bash
npx skills add woodydeng0122/skill-manager --skill skill-manager
```

Or install manually:

```bash
git clone https://github.com/woodydeng0122/skill-manager.git skills/skill-manager
```

## Usage

Mention the following keywords in your AI IDE conversation to trigger the skill:

- "analyze my skills" / "skill management" / "check skills"
- "skill evaluation" / "skill recommendation" / "skill analysis"

Once activated, the Skill will automatically:

1. Scan all installed Skills in the `skills/` directory
2. Analyze the current project's tech stack and characteristics
3. Score each Skill's necessity (0-100) and detect redundancy
4. Recommend high-value uninstalled Skills (P0/P1/P2 priority)
5. Output a structured analysis report

You can also run the analysis script directly:

```bash
python skills/skill-manager/scripts/skill_analyzer.py scan --skills-dir skills --project-dir .
```

## Directory Structure

```
skills/skill-manager/
├── SKILL.md              # Skill definition file
└── scripts/
    └── skill_analyzer.py # Core analysis engine (pure Python stdlib, zero dependencies)
```

## License

MIT
