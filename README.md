# skill-manager

一个用于技能管理和发布的 AI IDE 技能集合。

- **skill-manager** — 检测已安装的 AI IDE 技能，评估必要性和冗余度，并根据项目需求推荐高价值的未安装技能。
- **skill-publisher** — 引导你将技能发布并提交到 skills.sh 目录，使其可以通过 `npx skills find` 被搜索到。

## 安装

```bash
npx skills add woodydeng0122/skill-manager --skill skill-manager
npx skills add woodydeng0122/skill-manager --skill skill-publisher
```

或者手动安装：

```bash
git clone https://github.com/woodydeng0122/skill-manager.git skills/skill-manager
```

## 技能说明

### skill-manager — 技能管理分析器

**触发关键词：**
- "分析我的技能" / "技能管理" / "检查技能"
- "技能评估" / "技能推荐" / "技能分析"

**功能说明：**

1. 扫描 `skills/` 目录中所有已安装的技能
2. 分析当前项目的技术栈和特征
3. 为每个技能评分必要性（0-100）并检测冗余
4. 推荐高价值的未安装技能（P0/P1/P2 优先级）
5. 输出结构化的分析报告

**直接运行：**

```bash
python skills/skill-manager/scripts/skill_analyzer.py scan --skills-dir skills --project-dir .
```

### skill-publisher — 技能发布指南

**触发关键词：**
- "发布技能" / "提交技能" / "技能搜索"
- "技能发现" / "让技能可被搜索" / "分享技能"

**功能说明：**

1. 验证技能的 SKILL.md 结构和格式
2. 优化技能描述以提高可发现性
3. 引导你提交到 https://agentskill.sh/submit
4. 帮助设置 GitHub webhook 实现自动同步
5. 验证技能可以通过 `npx skills find` 被搜索到

## 目录结构

```
skills/
├── skill-manager/
│   ├── SKILL.md              # 技能定义文件
│   └── scripts/
│       └── skill_analyzer.py # 核心分析引擎（纯 Python 标准库，无外部依赖）
└── skill-publisher/
    └── SKILL.md              # 技能发布指南
```

## 许可证

MIT
