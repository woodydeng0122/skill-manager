# skill-manager

技能管理分析器 — 检测已安装的 AI IDE Skill，评估必要性与冗余度，按项目需求推荐未安装的高价值 Skill。

## 安装

```bash
npx skills add woodydeng0122/skill-manager --skill skill-manager
```

或手动安装：

```bash
git clone https://github.com/woodydeng0122/skill-manager.git skills/skill-manager
```

## 使用

在 AI IDE 对话中直接提及以下关键词即可触发：

- "分析我的技能" / "技能管理" / "检查技能"
- "技能评估" / "技能推荐" / "skill分析"

Skill 激活后将自动执行：

1. 扫描 `skills/` 目录下所有已安装 Skill
2. 分析当前项目的技术栈和特征
3. 对每个 Skill 进行必要性评分（0-100）和冗余度检测
4. 推荐未安装的高价值 Skill（P0/P1/P2 优先级）
5. 输出结构化分析报告

也可直接运行分析脚本：

```bash
python skills/skill-manager/scripts/skill_analyzer.py scan --skills-dir skills --project-dir .
```

## 目录结构

```
skills/skill-manager/
├── SKILL.md              # 技能定义文件
└── scripts/
    └── skill_analyzer.py # 核心分析引擎（纯 Python 标准库，零依赖）
```

## 许可证

MIT