#!/usr/bin/env python3
"""技能管理分析器 - 核心分析引擎

扫描已安装的技能，评估必要性和冗余度，并推荐高价值的未安装技能。
纯 Python 3 标准库实现，零外部依赖。
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


EXCLUDE_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    ".trae", ".cursor", ".windsurf", ".vscode", ".idea",
    "skills", "dist", "build", ".next", ".nuxt",
}


def scan_skills(skills_dir: str) -> list[dict]:
    """扫描技能目录并发现所有已安装的技能"""
    skills = []
    skills_path = Path(skills_dir)

    if not skills_path.exists():
        return skills

    for skill_dir in sorted(skills_path.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        info = parse_skill_md(skill_md)
        info["dir_name"] = skill_dir.name
        info["path"] = str(skill_dir)
        info["has_scripts"] = (skill_dir / "scripts").exists()
        info["file_count"] = count_files(skill_dir)
        skills.append(info)

    return skills


def parse_skill_md(skill_md_path: Path) -> dict:
    """解析 SKILL.md 文件并提取元数据"""
    info = {
        "name": skill_md_path.parent.name,
        "description": "",
        "raw_frontmatter": {},
        "sections": [],
        "keywords": [],
        "line_count": 0,
    }

    try:
        content = skill_md_path.read_text(encoding="utf-8")
        info["line_count"] = len(content.splitlines())
    except Exception:
        return info

    in_frontmatter = False
    frontmatter_lines = []
    body_start = 0

    for i, line in enumerate(content.splitlines()):
        stripped = line.strip()
        if stripped == "---":
            if not in_frontmatter:
                in_frontmatter = True
            else:
                body_start = i + 1
                break
        elif in_frontmatter:
            frontmatter_lines.append(stripped)

    for fl in frontmatter_lines:
        match = re.match(r'^(\w+):\s*"(.*)"$', fl)
        if match:
            info["raw_frontmatter"][match.group(1)] = match.group(2)

    info["name"] = info["raw_frontmatter"].get("name", info["name"])
    info["description"] = info["raw_frontmatter"].get("description", "")

    body = "\n".join(content.splitlines()[body_start:]) if body_start else content

    info["sections"] = re.findall(r'^#{1,3}\s+(.+)$', body, re.MULTILINE)

    keywords = set()
    for word in re.findall(r'[\w\u4e00-\u9fff]{2,}', info["description"]):
        keywords.add(word.lower())
    for section in info["sections"]:
        for word in re.findall(r'[\w\u4e00-\u9fff]{2,}', section):
            keywords.add(word.lower())
    info["keywords"] = list(keywords)

    return info


def count_files(directory: Path) -> int:
    """统计目录中的文件数量"""
    count = 0
    try:
        for _ in directory.rglob("*"):
            if _.is_file():
                count += 1
    except Exception:
        pass
    return count


def analyze_project(project_dir: str) -> dict:
    """分析项目上下文"""
    project_path = Path(project_dir)
    context = {
        "languages": Counter(),
        "frameworks": [],
        "project_type": "未知",
        "total_files": 0,
        "has_package_json": False,
        "has_requirements_txt": False,
        "has_cargo_toml": False,
        "has_git": False,
        "tech_keywords": set(),
    }

    ext_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript/React",
        ".jsx": "JavaScript/React",
        ".vue": "Vue",
        ".rs": "Rust",
        ".go": "Go",
        ".java": "Java",
        ".kt": "Kotlin",
        ".swift": "Swift",
        ".c": "C",
        ".cpp": "C++",
        ".h": "C/C++ Header",
        ".css": "CSS",
        ".scss": "SCSS",
        ".html": "HTML",
        ".md": "Markdown",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".toml": "TOML",
        ".sql": "SQL",
        ".sh": "Shell",
        ".dockerfile": "Docker",
    }

    try:
        for f in project_path.rglob("*"):
            if f.is_file() and not any(excl in str(f).split(os.sep) for excl in EXCLUDE_DIRS):
                context["total_files"] += 1
                ext = f.suffix.lower()
                if ext in ext_map:
                    context["languages"][ext_map[ext]] += 1
    except Exception:
        pass

    context["has_package_json"] = (project_path / "package.json").exists()
    context["has_requirements_txt"] = (project_path / "requirements.txt").exists()
    context["has_cargo_toml"] = (project_path / "Cargo.toml").exists()
    context["has_git"] = (project_path / ".git").exists()

    if context["has_package_json"]:
        try:
            pkg = json.loads((project_path / "package.json").read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            framework_indicators = {
                "react": "React",
                "vue": "Vue",
                "next": "Next.js",
                "nuxt": "Nuxt",
                "express": "Express",
                "fastify": "Fastify",
                "nestjs": "NestJS",
                "angular": "Angular",
                "svelte": "Svelte",
                "electron": "Electron",
                "tailwindcss": "Tailwind CSS",
            }
            for dep, framework in framework_indicators.items():
                if dep in deps:
                    context["frameworks"].append(framework)
        except Exception:
            pass

    if context["has_requirements_txt"]:
        try:
            reqs = (project_path / "requirements.txt").read_text(encoding="utf-8").lower()
            py_frameworks = {
                "django": "Django",
                "flask": "Flask",
                "fastapi": "FastAPI",
                "sqlalchemy": "SQLAlchemy",
                "pandas": "Pandas",
                "numpy": "NumPy",
                "pytest": "Pytest",
            }
            for dep, framework in py_frameworks.items():
                if dep in reqs:
                    context["frameworks"].append(framework)
        except Exception:
            pass

    top_langs = context["languages"].most_common(3)
    if any(lang in ["TypeScript/React", "JavaScript/React", "Vue", "HTML"] for lang, _ in top_langs):
        context["project_type"] = "web_frontend"
    elif any(lang in ["Python", "Go", "Rust", "Java"] for lang, _ in top_langs):
        if context["frameworks"]:
            context["project_type"] = "web_backend"
        else:
            context["project_type"] = "cli_tool_or_library"
    elif context["total_files"] < 10:
        context["project_type"] = "small_project"
    else:
        context["project_type"] = "general"

    for lang, _ in top_langs:
        context["tech_keywords"].add(lang.lower())
    for fw in context["frameworks"]:
        context["tech_keywords"].add(fw.lower())

    return context


def calc_necessity(skill: dict, project_context: dict) -> tuple[int, str]:
    """计算技能必要性评分"""
    score = 0
    reasons = []

    skill_keywords = set(k.lower() for k in skill.get("keywords", []))
    tech_keywords = project_context.get("tech_keywords", set())

    overlap = skill_keywords & tech_keywords
    if overlap:
        domain_score = min(40, len(overlap) * 10)
        score += domain_score
        reasons.append(f"领域匹配：与项目技术栈共享 {len(overlap)} 个关键词")

    desc = skill.get("description", "").lower()
    name = skill.get("name", "").lower()

    problem_indicators = {
        "test": 15, "debug": 15,
        "deploy": 15, "doc": 10,
        "code": 15, "manage": 10,
        "analy": 15, "generat": 15,
        "secur": 15, "perform": 15,
    }
    for indicator, points in problem_indicators.items():
        if indicator in desc or indicator in name:
            score += points
            reasons.append(f"问题解决：涉及 {indicator} 相关能力")
            break

    if skill.get("line_count", 0) > 100:
        score += 10
        reasons.append("维护状态：内容完整性高")
    if skill.get("has_scripts"):
        score += 10
        reasons.append("维护状态：包含辅助脚本")

    score = min(100, score)
    return score, "; ".join(reasons) if reasons else "与当前项目相关性较低"


def calc_redundancy(skills: list[dict]) -> list[dict]:
    """计算技能之间的冗余度"""
    redundancies = []

    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            ki = set(k.lower() for k in skills[i].get("keywords", []))
            kj = set(k.lower() for k in skills[j].get("keywords", []))

            if not ki or not kj:
                continue

            intersection = ki & kj
            union = ki | kj
            if not union:
                continue

            jaccard = len(intersection) / len(union)

            if jaccard > 0.3:
                redundancies.append({
                    "skill_a": skills[i]["name"],
                    "skill_b": skills[j]["name"],
                    "overlap_ratio": round(jaccard * 100, 1),
                    "shared_keywords": list(intersection)[:5],
                    "severity": "高" if jaccard > 0.5 else "中" if jaccard > 0.3 else "低",
                })

    redundancies.sort(key=lambda x: x["overlap_ratio"], reverse=True)
    return redundancies


def recommend_skills(project_context: dict, installed_names: list[str]) -> list[dict]:
    """根据项目上下文推荐未安装的技能"""
    recommendations = []

    installed_set = set(installed_names)

    skill_db = [
        {
            "name": "skill-creator",
            "description": "用于创建和管理自定义技能的官方工具",
            "match_condition": lambda ctx: True,
            "priority": "P0",
            "benefit": "快速创建和管理技能，所有技能开发的基础",
        },
        {
            "name": "code-reviewer",
            "description": "自动化代码审查，检测潜在问题和改进点",
            "match_condition": lambda ctx: any(l in str(ctx["languages"]) for l in ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java"]),
            "priority": "P0",
            "benefit": "自动发现代码问题，提高代码质量",
        },
        {
            "name": "test-generator",
            "description": "自动生成单元测试和集成测试",
            "match_condition": lambda ctx: ctx["total_files"] > 5,
            "priority": "P1",
            "benefit": "自动生成测试用例，提高测试覆盖率",
        },
        {
            "name": "doc-generator",
            "description": "自动生成 API 文档和代码注释",
            "match_condition": lambda ctx: ctx["total_files"] > 10,
            "priority": "P1",
            "benefit": "自动生成文档，减少手动维护成本",
        },
        {
            "name": "git-helper",
            "description": "智能 Git 提交信息生成和分支管理",
            "match_condition": lambda ctx: ctx["has_git"],
            "priority": "P1",
            "benefit": "标准化 Git 提交，提高协作效率",
        },
        {
            "name": "refactor-assistant",
            "description": "代码重构助手，识别代码异味并提供重构方案",
            "match_condition": lambda ctx: ctx["total_files"] > 10,
            "priority": "P2",
            "benefit": "识别代码异味，提供重构建议",
        },
        {
            "name": "api-designer",
            "description": "RESTful API 设计和 Mock 数据生成",
            "match_condition": lambda ctx: ctx["project_type"] in ("web_backend", "web_frontend"),
            "priority": "P1",
            "benefit": "快速设计 API 接口，生成 Mock 数据",
        },
        {
            "name": "db-migration-helper",
            "description": "数据库迁移脚本生成和版本管理",
            "match_condition": lambda ctx: any(l in str(ctx["languages"]) for l in ["Python", "Go", "Java", "Rust"]),
            "priority": "P2",
            "benefit": "安全生成数据库迁移脚本",
        },
        {
            "name": "docker-compose-generator",
            "description": "自动生成 Docker Compose 配置",
            "match_condition": lambda ctx: ctx["project_type"] in ("web_backend", "web_frontend"),
            "priority": "P2",
            "benefit": "快速生成容器化部署配置",
        },
        {
            "name": "performance-profiler",
            "description": "性能分析工具，检测瓶颈并提供优化建议",
            "match_condition": lambda ctx: ctx["total_files"] > 20,
            "priority": "P2",
            "benefit": "发现性能瓶颈，提供优化方案",
        },
    ]

    for skill in skill_db:
        if skill["name"] in installed_set:
            continue
        if skill["match_condition"](project_context):
            recommendations.append({
                "name": skill["name"],
                "description": skill["description"],
                "priority": skill["priority"],
                "benefit": skill["benefit"],
            })

    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 99))

    return recommendations


def generate_report(skills: list[dict], project_context: dict, redundancies: list[dict], recommendations: list[dict]) -> str:
    """生成格式化的分析报告"""
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("╔══════════════════════════════════════════════════╗")
    lines.append("║           📊 技能管理分析报告   ║")
    lines.append("╠══════════════════════════════════════════════════╣")
    lines.append(f"║ 项目类型: {project_context['project_type']:<42}║")
    top_langs = ", ".join(f"{l}({c})" for l, c in project_context["languages"].most_common(3))
    lines.append(f"║ 主要语言: {top_langs:<40}║")
    if project_context["frameworks"]:
        fw_str = ", ".join(project_context["frameworks"][:3])
        lines.append(f"║ 框架: {fw_str:<44}║")
    lines.append(f"║ 已安装技能: {len(skills)}{' ' * 37}║")
    lines.append(f"║ 分析时间: {now:<42}║")
    lines.append("╚══════════════════════════════════════════════════╝")
    lines.append("")

    lines.append("## 1. 已安装技能评估")
    lines.append("")

    if not skills:
        lines.append("> ⚠️ 当前未安装任何技能。考虑安装 skill-creator 来创建你的第一个技能。")
        return "\n".join(lines)

    lines.append("| 技能名称 | 必要性 | 冗余风险 | 状态 | 备注 |")
    lines.append("|------------|-----------|-----------------|--------|-------|")

    redundant_names = set()
    for r in redundancies:
        redundant_names.add(r["skill_a"])
        redundant_names.add(r["skill_b"])

    for skill in skills:
        name = skill["name"]
        necessity, reason = calc_necessity(skill, project_context)

        if necessity >= 80:
            status = "✅ 核心"
        elif necessity >= 60:
            status = "👍 推荐"
        elif necessity >= 40:
            status = "⚠️ 可选"
        else:
            status = "💤 低优先级"

        risk = "高" if name in redundant_names else "低"
        desc_short = skill["description"][:40] if skill["description"] else "-"
        lines.append(f"| {name} | {necessity}/100 | {risk} | {status} | {desc_short} |")

    lines.append("")

    if redundancies:
        lines.append("## 2. 冗余详情")
        lines.append("")
        lines.append("| 技能 A | 技能 B | 重叠率 | 严重度 | 共享关键词 |")
        lines.append("|---------|---------|-----------|----------|-----------------|")
        for r in redundancies:
            kw_str = ", ".join(r["shared_keywords"][:3])
            lines.append(f"| {r['skill_a']} | {r['skill_b']} | {r['overlap_ratio']}% | {r['severity']} | {kw_str} |")
        lines.append("")

    if recommendations:
        lines.append("## 3. 推荐安装的技能")
        lines.append("")
        lines.append("| 优先级 | 技能名称 | 匹配原因 | 预期收益 |")
        lines.append("|----------|-----------|--------------|------------------|")
        for rec in recommendations:
            lines.append(f"| {rec['priority']} | {rec['name']} | {rec['description']} | {rec['benefit']} |")
        lines.append("")

    lines.append("## 4. 行动项")
    lines.append("")

    suggestions = []
    low_necessity = [s for s in skills if calc_necessity(s, project_context)[0] < 40]
    if low_necessity:
        names = ", ".join(s["name"] for s in low_necessity)
        suggestions.append(f"- 🔴 低必要性技能 ({names})：考虑移除或归档")

    if redundancies:
        high_sev = [r for r in redundancies if r["severity"] == "高"]
        if high_sev:
            for r in high_sev:
                suggestions.append(f"- 🟡 `{r['skill_a']}` 和 `{r['skill_b']}` 重叠率较高 ({r['overlap_ratio']}%)：考虑合并或二选一")

    if recommendations:
        p0_recs = [r for r in recommendations if r["priority"] == "P0"]
        if p0_recs:
            names = ", ".join(r["name"] for r in p0_recs)
            suggestions.append(f"- 🟢 强烈建议安装：{names}")

    if not suggestions:
        suggestions.append("- ✅ 当前技能配置合理，无需调整")

    lines.extend(suggestions)
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="技能管理分析器")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    scan_parser = subparsers.add_parser("scan", help="扫描和分析技能")
    scan_parser.add_argument("--skills-dir", default="skills", help="技能目录路径")
    scan_parser.add_argument("--project-dir", default=".", help="项目目录路径")
    scan_parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    args = parser.parse_args()

    if args.command == "scan":
        skills = scan_skills(args.skills_dir)
        project_context = analyze_project(args.project_dir)
        redundancies = calc_redundancy(skills)
        installed_names = [s["name"] for s in skills]
        recommendations = recommend_skills(project_context, installed_names)

        if args.json:
            output = {
                "project_context": {
                    "project_type": project_context["project_type"],
                    "languages": dict(project_context["languages"].most_common(10)),
                    "frameworks": project_context["frameworks"],
                    "total_files": project_context["total_files"],
                },
                "installed_skills": [
                    {
                        "name": s["name"],
                        "description": s["description"],
                        "necessity": calc_necessity(s, project_context)[0],
                        "necessity_reason": calc_necessity(s, project_context)[1],
                    }
                    for s in skills
                ],
                "redundancies": redundancies,
                "recommendations": recommendations,
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            report = generate_report(skills, project_context, redundancies, recommendations)
            print(report)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
