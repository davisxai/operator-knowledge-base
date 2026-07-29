---
name: swarm
description: >
  Decompose a complex task into parallel subagents and create all agent
  files for execution. Invoke when: "create agents for this", "spin up
  a swarm", "parallel agents", "swarm this", "break this into subagents".
argument-hint: <endstate or full task description>
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Swarm

Analyze a requested endstate, decompose it into independent parallel
workstreams, design a purpose-built subagent for each, create all agent
files, and deliver a ready-to-execute orchestration plan with wave
structure and exact invocation commands.

## Phase 1: Context Capture
Read project context. Inventory existing agents. Parse the endstate.

## Phase 2: Workstream Decomposition
Identify parallel workstreams. Each produces one independent deliverable.
Target 2-6 agents. Map wave structure before writing files.

## Phase 3: Agent Specification
For each workstream: name, model (haiku/sonnet/opus), tools (least-privilege),
output definition.

## Phase 4: Create Agent Files
Write each agent file with: mission, context, protocol (setup, core work,
verification, output), and quality standards.

## Phase 5: Orchestration Plan
Output the wave map with exact Task() invocations.
