---
name: system-design
description: >
  Map out a software or business system architecture with pipeline stages,
  tool recommendations, realistic volume/pricing numbers, and clear visual
  layouts. Use when the user says "system design", "map this system",
  "how should we build this", "architect this", or "lay out the pipeline".
argument-hint: "[system-type] [client-name]"
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
---

# System Design

Map a business or software system into a clear, buildable architecture.
Output a document with pipeline visualization, named tools, realistic
volume estimates, and monthly cost projections.

## Phase 1: Requirements
Parse the system type. Research current tools and pricing.
Identify data flow, integrations, and scale requirements.

## Phase 2: Architecture
Design the pipeline: Input -> Process -> Store -> Serve -> Monitor.
Name specific tools at each stage. Include fallback options.

## Phase 3: Cost Model
Estimate monthly volume. Calculate costs per tool at that volume.
Total monthly cost with breakdown.

## Phase 4: Output
Pipeline diagram (text-based), tool recommendations with links,
volume/pricing table, implementation sequence, risks and mitigations.
