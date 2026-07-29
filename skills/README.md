# Skills

Claude Code skills from the OperatorOS setup. Each folder is a complete skill: copy it into `~/.claude/skills/` and invoke it with `/skill-name`. No restart needed.

```bash
# install a skill globally
cp -r extract ~/.claude/skills/extract
```

## Index

- **[create/](create/)** The skill that builds every other skill. Describe a workflow, get a complete SKILL.md.
- **[extract/](extract/)** Turn any messy input (transcripts, meeting notes, Slack dumps, email threads) into structured decisions, action items, facts, and open questions.
- **[research/](research/)** Deep research with parallel discovery across web, codebase, and alternatives. Cross-referenced findings, one clear recommendation.
- **[recurring-report/](recurring-report/)** Compile a recurring status report from Gmail, Notion, Linear, and GitHub. Built for Claude Desktop's task scheduler.
- **[swarm/](swarm/)** Decompose a complex task into parallel subagents with a ready-to-execute orchestration plan.
- **[system-design/](system-design/)** Map a software or business system into a buildable architecture with named tools and realistic costs.

The full skill-writing playbook is in [guides/claude-code-skills-starter-kit/](../guides/claude-code-skills-starter-kit/).
