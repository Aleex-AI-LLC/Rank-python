# Rank Python SDK

[![PyPI version](https://img.shields.io/pypi/v/rank-sdk.svg)](https://pypi.org/project/rank-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/rank-sdk.svg)](https://pypi.org/project/rank-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python library for the [Rank API](https://aleex-rank.ai) — AI-powered autonomous pentesting.

Rank lets you run full penetration tests driven by AI agents in minutes. This SDK provides convenient access to the Rank REST API and real-time streaming from Python 3.8+, with both synchronous and asynchronous clients.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Running a Pentest (End-to-End)](#running-a-pentest-end-to-end)
  - [1. Create a Chat Session](#1-create-a-chat-session)
  - [2. Create a Pentest](#2-create-a-pentest)
  - [3. Assign Agents](#3-assign-agents)
  - [4. Execute — Automatic Mode](#4-execute--automatic-mode)
  - [5. Execute — Guided Mode (Phase by Phase)](#5-execute--guided-mode-phase-by-phase)
  - [6. Generate a Report](#6-generate-a-report)
  - [Cancelling a Running Pentest](#cancelling-a-running-pentest)
- [Vulnerability Management](#vulnerability-management)
  - [List and Inspect](#list-and-inspect)
  - [Status Transitions](#status-transitions)
  - [Assignment](#assignment)
  - [Comments](#comments)
  - [Evidence Files](#evidence-files)
  - [Bulk Operations](#bulk-operations)
  - [Quality Gate](#quality-gate)
  - [Export and Global Summary](#export-and-global-summary)
- [AI Chat](#ai-chat)
- [Streaming Events Reference](#streaming-events-reference)
- [Agents](#agents)
- [Teams](#teams)
- [Usage](#usage)
- [Chats](#chats)
- [Tickets (Jira)](#tickets-jira)
- [Error Handling](#error-handling)
- [Async Usage](#async-usage)
- [Configuration](#configuration)
- [Requirements](#requirements)

## Installation

```bash
pip install rank-sdk
```

## Quick Start

```python
import rank

client = rank.Rank(api_key="rk_...")

# List your pentests
pentests = client.pentests.list()
for p in pentests.items:
    print(p.name, p.status)

# Get the current user
me = client.auth.me()
print(me.username, me.email)
```

## Authentication

The SDK authenticates via an API key sent in the `X-API-Key` header. You can provide it in two ways:

```python
# 1. Explicit parameter
client = rank.Rank(api_key="rk_...")

# 2. Environment variable (recommended)
#    export RANK_API_KEY=rk_...
client = rank.Rank()
```

API keys are created from the Rank dashboard under **Settings > API Tokens**. Each token can be scoped to specific permissions and teams.

## Running a Pentest (End-to-End)

This section walks through the complete lifecycle of a pentest, from creation to report generation. This is the core workflow of Rank.

### 1. Create a Chat Session

A chat session provides conversation persistence and context across the pentest execution. All AI interactions (agent prompts, phase outputs) are stored in the chat.

```python
chat = client.chats.create(nombre="Web Scan - example.com")
print(chat.id)
```

### 2. Create a Pentest

A pentest requires a **type**, a **mode**, a **methodology**, and at least one **asset**.

**Pentest types:**

| Type | Target |
|---|---|
| `web` | Web applications |
| `api` | REST/GraphQL APIs |
| `server` | Servers and infrastructure |

**Asset types:**

| `asset_type` | `asset_value` | Example |
|---|---|---|
| `url` | Target URL | `https://example.com` |
| `domain` | Domain name | `example.com` |
| `ip` | IP address | `192.168.1.100` |
| `api` | API endpoint or documentation URL | `https://api.example.com/v1` |

Each pentest must have at least one asset, and exactly one should be marked as `is_primary`.

**Modes — automatic vs. guided:**

| Mode | Methodology | Phases | Vulnerability processing |
|---|---|---|---|
| `automatic` | OWASP Top 10 (forced, `methodology_id=1`) | All phases run sequentially without intervention | Automatic — handled during the stream |
| `guided` | You choose — list available methodologies first | You control each phase (1-3) individually | Manual — start `process_vulnerabilities` after the phases, then poll with `wait_for_vulnerabilities` |

#### Automatic mode

In automatic mode, the methodology is always **OWASP Top 10** (`methodology_id=1`), regardless of what you pass. The agents run all phases end-to-end and vulnerabilities are processed automatically.

```python
pentest = client.pentests.create(
    name="Quick Web Scan",
    url="https://example.com",
    type="web",
    mode="automatic",
    assets=[
        {
            "asset_type": "url",
            "asset_value": "https://example.com",
            "is_primary": True,
        },
    ],
)
```

#### Guided mode

In guided mode, you must choose a methodology. List the available ones first:

```python
# List available methodologies
methodologies = client.pentests.methodologies.list()
for m in methodologies.items:
    print(f"[{m.id}] {m.name} — {m.description}")

# Create the pentest with a specific methodology
pentest = client.pentests.create(
    name="Full Infrastructure Audit",
    url="https://example.com",
    type="web",
    mode="guided",
    methodology_id=2,
    assets=[
        {
            "asset_type": "domain",
            "asset_value": "example.com",
            "is_primary": True,
        },
        {
            "asset_type": "ip",
            "asset_value": "93.184.216.34",
            "is_primary": False,
        },
        {
            "asset_type": "api",
            "asset_value": "https://api.example.com/v2",
            "is_primary": False,
        },
    ],
)
print(f"Pentest #{pentest.id} created — status: {pentest.status}")
```

### 3. Assign Agents

Before executing, you need to assign AI agents to the pentest.

**For guided mode**, list the available pentest agents, pick at least 3 (max 4), and assign them to a phase:

```python
# List pentest agents
agents_resp = client.agents.list(type="pentest")
for agent in agents_resp.items:
    print(f"[{agent.id}] {agent.name} — phase {agent.phase_id}")

# Assign agents to phase 1 (minimum 3, maximum 4)
client.pentests.agents.assign(
    pentest.id,
    agents=[
        {"agent_id": 10, "phase_id": 1, "execution_order": 1},
        {"agent_id": 11, "phase_id": 1, "execution_order": 2},
        {"agent_id": 12, "phase_id": 1, "execution_order": 3},
    ],
)
```

**For automatic mode**, use default agents — they are auto-assigned across all phases:

```python
defaults = client.pentests.agents.default(pentest.id)
print(f"Auto-assigned {defaults.assigned_count} agents")
for phase in defaults.items:
    print(f"Phase {phase.phase_id}: {[a.name for a in phase.agents]}")
```

### 4. Execute — Automatic Mode

Launch the pentest and stream the real-time output. In automatic mode, the agents run all phases sequentially and process vulnerabilities at the end — all within a single stream:

```python
from rank import AgentEvent

with client.ai.chat.stream(
    user_prompt="Start the pentest on the configured targets",
    pentest_id=pentest.id,
    mode="automatic",
    chat_id=chat.id,
) as stream:
    for event in stream:
        if event.type == "content":
            print(event.content, end="", flush=True)
        elif event.type == "phase_start":
            meta = event.metadata
            print(f"\n[Phase started] {event.content} ({meta.get('progress')}%)")
        elif event.type == "phase_complete":
            meta = event.metadata
            print(f"\n[Phase done] {event.content} ({meta.get('progress')}%)")
        elif event.is_agent_event:
            ev = event.agent_event
            if ev.event_type == AgentEvent.TOOL_CALL:
                print(f"\n[Tool] {ev.data['tool_name']}")
            elif ev.event_type == AgentEvent.AGENT_FINISHED:
                print(f"\n[Agent done] reason={ev.data.get('stop_reason')} "
                      f"findings={ev.data.get('findings')}")
        elif event.type == "processing_vulnerabilities":
            print(f"\n[Processing vulns] {event.content}")
        elif event.type == "vulnerabilities_complete":
            meta = event.metadata
            found = meta.get("vulnerabilities_found", 0)
            stored = meta.get("vulnerabilities_stored", 0)
            print(f"\n[Vulns] Found: {found} | Stored: {stored}")
        elif event.type == "complete":
            meta = event.metadata
            print(f"\n[Complete] {meta.get('elapsed_time', 0):.1f}s elapsed")
        elif event.type == "error":
            print(f"\n[Error] {event.error}")
```

After the stream completes, vulnerabilities are already processed (the backend does it automatically at the end of the run). You cannot reprocess them — trying to call `process_vulnerabilities` again returns `409 Conflict`.

If the stream disconnects while vulnerabilities are still being processed, recover the final result by polling the status endpoint instead of re-running the pentest:

```python
result = client.pentests.wait_for_vulnerabilities(pentest.id, timeout=600)
if result.status == "completed":
    print(f"Created: {result.total_created}")
    if result.summary:
        print(f"By severity: critical={result.summary.critical} high={result.summary.high}")
# Or a single, non-blocking check:
#   status = client.pentests.get_vulnerability_status(pentest.id)
```

When you're ready, finish the pentest:

```python
result = client.pentests.finish(pentest.id)
print(result.message)
```

### 5. Execute — Guided Mode (Phase by Phase)

In guided mode, you execute one phase at a time. Between phases you can review results, reassign agents, or stop early.

```python
# Phase 1
with client.ai.chat.stream(
    user_prompt="Start the pentest on the configured targets",
    pentest_id=pentest.id,
    mode="guided",
    phase_id=1,
    chat_id=chat.id,
) as stream:
    for event in stream:
        if event.type == "content":
            print(event.content, end="", flush=True)
        elif event.type == "phase_complete":
            print(f"\n[Phase 1 done]")

# Phase 2
with client.ai.chat.stream(
    user_prompt="Continue with phase 2",
    pentest_id=pentest.id,
    mode="guided",
    phase_id=2,
    chat_id=chat.id,
) as stream:
    for event in stream:
        if event.type == "content":
            print(event.content, end="", flush=True)

# Phase 3
with client.ai.chat.stream(
    user_prompt="Continue with phase 3",
    pentest_id=pentest.id,
    mode="guided",
    phase_id=3,
    chat_id=chat.id,
) as stream:
    for event in stream:
        if event.type == "content":
            print(event.content, end="", flush=True)
```

After completing the desired phases, process the raw agent outputs into structured vulnerabilities using AI, and then finish the pentest.

Vulnerability processing is **asynchronous**: `process_vulnerabilities` only enqueues the job and returns immediately. Block until it finishes with `wait_for_vulnerabilities` (which polls `get_vulnerability_status` under the hood), or poll the status yourself:

```python
# Start the async processing job
job = client.pentests.process_vulnerabilities(
    pentest.id,
    model_alias="gemini-2.5-flash",
)
print(f"Job status: {job.status}")  # "processing"

# Block until it finishes (raises TimeoutError if it takes too long)
result = client.pentests.wait_for_vulnerabilities(pentest.id, timeout=600)

if result.status == "completed":
    print(f"Responses analysed  : {result.total_responses}")
    print(f"Detected            : {result.total_detected}")
    print(f"Created             : {result.total_created}")
    if result.summary:
        s = result.summary
        print(f"By severity         : critical={s.critical} high={s.high} "
              f"medium={s.medium} low={s.low} info={s.info}")
    for v in result.vulnerabilities_created:
        print(f"  vuln_id={v.vulnerability_id}  operation_id={v.operation_id}")
else:
    print(f"Processing failed: {result.error}")

# Or poll manually instead of blocking:
#   status = client.pentests.get_vulnerability_status(pentest.id)
#   while status.status == "processing":
#       time.sleep(3)
#       status = client.pentests.get_vulnerability_status(pentest.id)

# Finish the pentest
result = client.pentests.finish(pentest.id)
print(result.message)

if result.vulnerabilities:
    vs = result.vulnerabilities
    print(f"Total: {vs.total}")
    print(f"By severity: {vs.by_severity}")
    print(f"By status: {vs.by_status}")
    if vs.risk_score:
        print(f"Risk score: {vs.risk_score.score} ({vs.risk_score.level})")
```

> **Tip:** You don't have to run all 3 phases. You can stop after any phase, process vulnerabilities, and finish the pentest.

### 6. Generate a Report

Generate a PDF report and send it by email. The pentest must be completed.

```python
result = client.pentests.generate_report(
    pentest.id,
    recipient_email="security@example.com",
    recipient_name="Security Team",
    subject="Pentest Report — example.com",
    cc_emails=["cto@example.com", "devops@example.com"],
    extended=1,  # 0 = summary, 1 = full report with evidence
)
print(result.message)
```

### Cancelling a Running Pentest

Cancel a pentest that is currently executing:

```python
result = client.pentests.cancel(pentest.id)
print(result.message)  # "Pentest cancelled successfully"
```

You can also reconnect to the SSE stream of a running pentest:

```python
with client.pentests.stream(pentest_id=pentest.id) as stream:
    for event in stream:
        print(event.type, event.content)
```

## Vulnerability Management

Vulnerabilities are nested under pentests and offer a rich set of operations for triaging, resolving, and tracking findings.

### List and Inspect

```python
# List vulnerabilities (paginated, filterable by severity)
vulns = client.pentests.vulnerabilities.list(pentest.id, severity="critical")
for v in vulns.items:
    print(f"[{v.severity}] {v.vulnerability} — {v.status}")

# Get full details
vuln = client.pentests.vulnerabilities.retrieve(pentest.id, vulnerability_id=42)
print(vuln.description)
print(vuln.resolution)

# Update fields
client.pentests.vulnerabilities.update(
    pentest.id, 42,
    severity="high",
    priority="urgent",
    due_date="2026-04-15",
)

# Get aggregated statistics
summary = client.pentests.vulnerabilities.summary(pentest.id)
print(summary)
```

### Status Transitions

Vulnerabilities follow a state machine. Use the dedicated methods for each transition:

```python
# Resolve a vulnerability
client.pentests.vulnerabilities.resolve(
    pentest.id, 42,
    resolution_type="evidenced",  # "evidenced" or "without_evidence"
    comment="Patched in v2.3.1",
)

# Reopen a resolved vulnerability
client.pentests.vulnerabilities.reopen(
    pentest.id, 42,
    reason="Regression found in v2.3.2",
)

# Mark as false positive
client.pentests.vulnerabilities.false_positive(
    pentest.id, 42,
    reason="Test environment only, not reachable in production",
)

# Accept the risk
client.pentests.vulnerabilities.accept_risk(
    pentest.id, 42,
    reason="Low impact, scheduled for next quarter",
)

# Generic status change (only "open" and "in_progress" as targets)
client.pentests.vulnerabilities.change_status(
    pentest.id, 42,
    status="in_progress",
    comment="Investigation started",
)

# Change priority
client.pentests.vulnerabilities.change_priority(
    pentest.id, 42,
    priority="urgent",  # "urgent", "high", "normal", "low"
)
```

### Assignment

Assign vulnerabilities to team members for tracking:

```python
# Assign (auto-moves status to in_progress if currently open)
client.pentests.vulnerabilities.assign(
    pentest.id, 42,
    user_id=7,
    comment="Please investigate this XSS vector",
)

# Remove assignment
client.pentests.vulnerabilities.unassign(pentest.id, 42)
```

### Comments

```python
# List comments
comments = client.pentests.vulnerabilities.list_comments(pentest.id, 42)
for c in comments.items:
    print(f"{c.user.username}: {c.comment}")

# Add a comment
client.pentests.vulnerabilities.add_comment(
    pentest.id, 42,
    comment="Confirmed exploitable in staging environment",
)

# Edit a comment (only the author can edit)
client.pentests.vulnerabilities.update_comment(
    pentest.id, 42, comment_id=15,
    comment="Updated: confirmed exploitable in staging and production",
)

# Delete a comment
client.pentests.vulnerabilities.delete_comment(pentest.id, 42, comment_id=15)
```

### Evidence Files

Attach screenshots, logs, or other files to a vulnerability:

```python
# Upload evidence files (max 10 MB each, max 20 per request)
files = [
    ("files", ("screenshot.png", open("screenshot.png", "rb"), "image/png")),
    ("files", ("exploit.txt", open("exploit.txt", "rb"), "text/plain")),
]
client.pentests.vulnerabilities.upload_evidence_files(
    pentest.id, 42,
    files=files,
)

# List evidence files
evidence = client.pentests.vulnerabilities.list_evidence_files(pentest.id, 42)
for f in evidence.items:
    print(f.filename, f.file_url)

# Get a single file with download URL
file_info = client.pentests.vulnerabilities.get_evidence_file(pentest.id, 42, file_id=5)

# Delete an evidence file
client.pentests.vulnerabilities.delete_evidence_file(pentest.id, 42, file_id=5)
```

### Bulk Operations

Update the status of multiple vulnerabilities at once:

```python
result = client.pentests.vulnerabilities.bulk_update_status(
    pentest.id,
    vulnerability_ids=[42, 43, 44],
    status="in_progress",
    comment="Batch triage — assigning to security team",
)
print(f"Updated: {result.updated_count}, Failed: {result.failed_count}")
```

### Quality Gate

Evaluate your pentest against quality rules:

```python
# Per-pentest quality gate
result = client.pentests.vulnerabilities.quality_gate(
    pentest.id,
    rules=[
        {"severity": "critical", "max_open": 0},
        {"severity": "high", "max_open": 5},
        {"min_resolution_rate": 0.8},
        {"max_overdue": 0},
    ],
)
print(f"Passed: {result.passed}")

# Global quality gate (across last 7 pentests)
global_qg = client.pentests.quality_gate(
    max_open_critical=0,
    max_open_high=5,
    min_resolution_rate=80.0,
)
print(f"Overall: {'PASS' if global_qg.passed else 'FAIL'}")
```

### Export and Global Summary

```python
# Export vulnerabilities as JSON
export = client.pentests.vulnerabilities.export(pentest.id)

# Get original operation evidence for a vulnerability
evidence = client.pentests.vulnerabilities.evidence(pentest.id, 42)

# View change history
history = client.pentests.vulnerabilities.history(pentest.id, 42)
for entry in history.items:
    print(f"{entry.created_at}: {entry.action}")

# Global summary across all pentests
global_summary = client.pentests.vulnerabilities.global_summary()
```

## AI Chat

Beyond pentesting, Rank's general-purpose agents can perform **agentic research tasks** — they autonomously plan, browse, search, run tools, and cross-reference sources to deliver structured results. Think of them as security-focused research assistants that can execute multi-step workflows from a single prompt.

```python
chat = client.chats.create(nombre="Security Research")

# List available general agents
agents = client.agents.list(type="general")
for a in agents.items:
    print(f"[{a.id}] {a.name}")
```

### One-shot vs. agentic

A general agent runs in one of two modes, decided automatically by the backend:

| Mode | When | What you receive |
|---|---|---|
| **One-shot** | The agent's model is not agentic, or the agent has no tools assigned | A single answer streamed as `content`, then `complete` |
| **Agentic** | The agent's model has the agentic flag **and** the agent has at least one tool | A live ReAct loop (plan, tool calls, observations, reflection) streamed as `agent_event` activity, plus the final answer streamed as `content` |

> **Golden rule:** build the assistant's message by concatenating **only** the `content` events. `agent_event` messages describe what the agent is doing (thinking, calling tools, delegating to sub-agents) and are meant for an "activity" / timeline view — never concatenate them into the answer body.

Both modes are consumed with the exact same loop. If you only care about the final answer, just handle `content` and ignore everything else:

```python
with client.ai.chat.stream(
    agent_id=23,
    user_prompt="Research the latest critical Apache vulnerabilities disclosed this month. "
                "For each one, provide the CVE ID, severity score, affected versions, "
                "and a link to the NVD entry.",
    chat_id=chat.id,
) as stream:
    for event in stream:
        if event.type == "content":
            print(event.content, end="", flush=True)
        elif event.type == "complete":
            print()
```

To also surface the live activity of an agentic run, handle `agent_event` (see the [Streaming Events Reference](#streaming-events-reference) for every field):

```python
from rank import AgentEvent

with client.ai.chat.stream(
    agent_id=23,
    user_prompt="Investigate this target end-to-end and summarize the exposure.",
    chat_id=chat.id,
) as stream:
    for event in stream:
        if event.type == "content":
            # The actual answer — only this builds the message body.
            print(event.content, end="", flush=True)

        elif event.is_agent_event:
            ev = event.agent_event
            indent = "    " if ev.depth > 0 else ""  # sub-agents are nested
            if ev.event_type == AgentEvent.THINKING:
                print(f"\n{indent}[thinking] {ev.data['content'][:80]}")
            elif ev.event_type == AgentEvent.TOOL_CALL:
                print(f"\n{indent}[tool] {ev.data['tool_name']}")
            elif ev.event_type == AgentEvent.SUBAGENT_SPAWN:
                print(f"\n{indent}[subagent {ev.data['subagent_id']}] {ev.data['mission']}")
            elif ev.event_type == AgentEvent.TEXT_CHUNK:
                # Sub-agent text (depth > 0). Activity only — NOT the answer.
                print(f"{indent}{ev.data['content']}", end="", flush=True)
            elif ev.event_type == AgentEvent.AGENT_FINISHED:
                print(f"\n{indent}[done] {ev.data.get('stop_reason')}")

        elif event.type == "complete":
            print("\n[stream finished]")
```

> **Sub-agents:** if the agent has the `spawn_subagent` tool, it can delegate subtasks to sub-agents that run with isolated context. Their activity streams in live (nested via `depth` and `parent_agent_id`), but their final text is **not** part of the chat answer: it comes back to the main agent as a tool result. Sub-agent text arrives as `agent_event` with `event_type="text_chunk"` (`depth > 0`), and its consolidated summary appears in `subagent_complete.result_preview`. Group an instance's events by `instance_id`.

### Long-running agentic tasks

Because an agentic general agent keeps iterating until the objective is fully covered, it is ideal for **one-off, long-running tasks** described in a single natural-language prompt — you don't write any orchestration logic. State the goal and a stop condition and the agent will plan, run tools, branch on what it discovers, and keep going (bounded by its `max_iterations`, budget and timeout) until it can report back. The run ends with an `agent_finished` event whose `stop_reason` is usually `goal_reached`.

Tips for writing these prompts:

- State the end-to-end objective and an explicit stop condition (e.g. *"don't stop until..."*).
- Describe branching (*"if you find X, do Y; otherwise..."*) — the agent decides each step.
- Ask for a final consolidated summary so the answer (`content`) wraps everything up.

```python
with client.ai.chat.stream(
    agent_id=23,
    user_prompt=(
        "Analyze the IP 203.0.113.42 step by step. If you find a web server, "
        "enumerate common directories and look for known vulnerabilities; if "
        "there are other services (SSH, etc.), report versions and relevant "
        "CVEs. Don't stop until you've reviewed every open port, and summarize "
        "everything at the end."
    ),
    chat_id=chat.id,
) as stream:
    for event in stream:
        if event.type == "content":          # the final, consolidated answer
            print(event.content, end="", flush=True)
        elif event.type == "complete":
            print("\n[done]")
```

The agent runs the whole investigation autonomously in a single request. To also render each step as it happens (iterations, tool calls, sub-agents), handle `agent_event` exactly as in the agentic example above.

More prompts that map well to a single long-running run:

```python
# Prioritized CVE triage over a feed
"Triage the CVEs published this week affecting nginx or Apache. For each one, "
"fetch the CVSS vector, confirm the affected versions, and build a prioritized "
"remediation table. Don't finish until every item is classified."

# Attack-surface mapping
"Map the attack surface of example.com step by step: enumerate subdomains, "
"identify live hosts and their tech stack, and flag anything outdated or "
"known-vulnerable. Keep going until all subdomains are checked, then summarize "
"the riskiest findings."
```

**IP investigation (simple, one-shot style):**

```python
with client.ai.chat.stream(
    agent_id=23,
    user_prompt="Investigate the IP 203.0.113.42. Find out what services are commonly "
                "associated with it, check for known CVEs related to those services, "
                "and return each CVE with its NIST NVD link.",
    chat_id=chat.id,
) as stream:
    for event in stream:
        if event.type == "content":
            print(event.content, end="", flush=True)
```

**File analysis:**

```python
# Single attachment
with open("report.pdf", "rb") as f:
    with client.ai.chat.stream(
        agent_id=23,
        user_prompt="Analyze this security report and summarize the findings",
        chat_id=chat.id,
        file=f,
    ) as stream:
        for event in stream:
            if event.type == "content":
                print(event.content, end="", flush=True)

# Multiple attachments (use `files` with a list)
with open("report.pdf", "rb") as a, open("diagram.png", "rb") as b:
    with client.ai.chat.stream(
        agent_id=23,
        user_prompt="Cross-reference these files and summarize the findings",
        chat_id=chat.id,
        files=[a, b],
    ) as stream:
        for event in stream:
            if event.type == "content":
                print(event.content, end="", flush=True)
```

Attachments accept PDF, JSON, PNG, JPEG, WEBP and GIF. Use `file` for a single
attachment or `files` for several (they are mutually exclusive). Limits: up to
10 files, 30 MB per file and 50 MB combined per request.

The `chat_id` parameter maintains conversation context, so you can ask follow-up questions in the same session.

## Streaming Events Reference

All streaming responses (AI chat and pentest execution) yield `ServerSentEvent` objects with these properties:

| Property | Type | Description |
|---|---|---|
| `event.type` | `str` | Event type identifier |
| `event.content` | `str` | Text content of the event |
| `event.error` | `str \| None` | Error message (only for `error` events) |
| `event.metadata` | `dict` | Additional data (progress %, vuln counts, elapsed time, etc.) |
| `event.timestamp` | `float \| None` | Event timestamp |
| `event.raw_data` | `str` | Raw JSON string before parsing |
| `event.is_agent_event` | `bool` | `True` when the event carries an `AgentEvent` payload |
| `event.agent_event` | `AgentEvent \| None` | Parsed `AgentEvent` (only when `type="agent_event"`) |
| `event.event_type` | `str \| None` | Shortcut to `agent_event.event_type` |

**Transport event types:**

| Type | When | Key metadata |
|---|---|---|
| `content` | AI-generated text chunk | — |
| `queued` | Pentest enters the execution queue | — |
| `ready` | Pentest starts executing | — |
| `phase_start` | A phase begins | `phase_id`, `agents`, `progress`, `is_last` |
| `phase_complete` | A phase finishes | `phase_id`, `progress`, `forced_advance` |
| `phase_retry` | Phase retry (automatic mode) | — |
| `processing_vulnerabilities` | AI is analyzing findings | `pentest_id` |
| `vulnerabilities_complete` | Vulnerability processing done | `vulnerabilities_found`, `vulnerabilities_stored`, `summary` (severity breakdown) |
| `agent_event` | Agent/orchestrator activity | `event` field with `AgentEvent` (see below) |
| `complete` | Stream finished successfully | `pentest_id`, `total_phases`, `elapsed_time`, `vulnerabilities_found`, `vulnerabilities_stored`, `summary` |
| `error` | An error occurred | — |
| `cancelled` | Pentest was cancelled | `pentest_id`, `cancelled_at_phase` |
| `reconnected` | Reconnected to an existing stream | `current_phase`, `total_phases`, `progress` |

### AgentEvent

When `event.type == "agent_event"`, access the structured payload via `event.agent_event`. The `AgentEvent` dataclass has these fields:

| Field | Type | Description |
|---|---|---|
| `event_type` | `str` | Sub-event identifier (see tables below) |
| `agent_id` | `int \| str \| None` | Agent ID (numeric), `"orchestrator"`, or `None` |
| `parent_agent_id` | `int \| None` | Parent agent ID (for sub-agents) |
| `instance_id` | `str` | Unique per-execution key for grouping events. General main agents use `general_<agentId>_<hex>`; sub-agents use `<agentId>_sub<N>` |
| `depth` | `int` | `0` = top-level agent, `1` = sub-agent |
| `iteration` | `int` | Current iteration of the agent loop |
| `timestamp` | `float` | Unix timestamp |
| `data` | `dict` | Event-specific payload |

**Agent loop event types** (`agent_id` = numeric agent ID):

| `event_type` | When | Key fields in `data` |
|---|---|---|
| `agent_start` | Agent begins its ReAct loop | `model`, `phase`, `mission`, `max_iterations`, `tools` |
| `plan` | Attack plan generated | `plan_text` |
| `iteration_start` | Iteration begins | `iteration`, `max_iterations`, `tokens_used`, `stagnation` |
| `thinking` | Model reasoning (thinking/reasoning) | `content` |
| `tool_call` | Before executing a tool | `tool_name`, `tool_args` |
| `tool_result` | Tool execution result | `tool_name`, `result`, `duration_ms`, `cached`, `blocked`, `skipped` |
| `text_chunk` | Streaming text from a **sub-agent** (`depth > 0`) | `content` |
| `nudge` | Nudge to avoid premature termination | `nudge_count`, `unused_tools` |
| `subagent_spawn` | Sub-agent launched | `subagent_id`, `mission`, `depth` |
| `subagent_complete` | Sub-agent finished | `subagent_id`, `result_preview`, `iterations`, `findings` |
| `context_compaction` | Agent context compacted | `before_entries`, `after_entries`, `tokens_saved` |
| `progress` | Periodic progress update | `progress_log`, `findings_count` |
| `agent_finished` | Agent finished execution | `stop_reason`, `iterations`, `findings`, `output_tokens`, `input_tokens`, `elapsed_s` |

**Orchestration event types** (`agent_id` = `"orchestrator"`):

| `event_type` | When | Key fields in `data` |
|---|---|---|
| `orchestration_start` | Multi-agent phase begins | `agents`, `phase`, `total_agents` |
| `orchestration_status` | Periodic status (~30s) | `alive_agents`, `completed_agents`, `elapsed_time` |
| `agent_status_change` | Agent changes state | `agent_id`, `status`, `reasoning` |
| `consolidation_start` | Result consolidation begins | `agents_completed` |
| `consolidation_heartbeat` | Keepalive during consolidation (~10s) | `elapsed_seconds`, `message` |
| `consolidation_complete` | Consolidation finished | `input_tokens`, `output_tokens` |
| `orchestration_complete` | Multi-agent phase completed | `phase`, `total_agents`, `successful`, `failed` |

**Browser agent event types:**

| `event_type` | When | Key fields in `data` |
|---|---|---|
| `browser_agent_start` | Browser agent starts a mission | `mission`, `target_url`, `max_iterations` |
| `tool_call` / `tool_result` | Browser tool execution | Same fields as agent loop tool events |

All `event_type` values are available as constants on the `AgentEvent` class (e.g. `AgentEvent.TOOL_CALL`, `AgentEvent.TEXT_CHUNK`, `AgentEvent.AGENT_FINISHED`).

#### General agentic flow

General agents (`agent_type="general"` running the agentic loop) reuse the same `AgentEvent` envelope, but a few events carry **different `data` keys** than the pentest flow, and there are no orchestration events (a single agent drives the loop, optionally delegating to sub-agents). `data` is an opaque dict, so reading the keys below is all you need:

| `event_type` | Key fields in `data` (general flow) | Notes |
|---|---|---|
| `agent_start` | `model`, `agent_id`, `mission`, `max_iterations`, `tools` | No `phase`. |
| `thinking` | `content`, `streaming` | `streaming=True` when reasoning arrives in live fragments. |
| `tool_result` | `tool_name`, `result`, `duration_ms`, `skipped` | — |
| `interpretation` | `content` | Free-form analysis of the tool results (in the pentest flow this event uses `phase` / `tools_interpreted` instead). |
| `context_compaction` | `summarized_steps`, `summary_chars` | Long-running tasks compact context (pentest flow uses `before_entries` / `after_entries` / `tokens_saved`). |
| `progress` | `iteration`, `tools_used`, `tokens_used` | Per-iteration progress (pentest flow uses `progress_log` / `findings_count`). |
| `iteration_complete` | `iteration_prompt`, `iteration_response`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens` | Includes cache token counters. |
| `text_chunk` | `content` | **Sub-agents only** (`depth > 0`). Live sub-agent text — activity, never part of the answer. |
| `subagent_spawn` | `subagent_id`, `mission`, `depth` | A sub-agent was launched. |
| `subagent_complete` | `subagent_id`, `result_preview`, `iterations` | Consolidated sub-agent result summary. |
| `agent_finished` | `stop_reason`, `iterations`, `input_tokens`, `output_tokens`, `elapsed_s` | No `findings`. `stop_reason` ∈ `goal_reached`, `max_iterations`, `timeout`, `budget`, `stagnation`, `cancelled`. |

Reconstructing the hierarchy in a UI: if `depth > 0` or `parent_agent_id` is set, the event belongs to a sub-agent — group it by `instance_id`. The assistant's answer is still built **only** from top-level `content` messages.

**Handling agent events:**

```python
from rank import AgentEvent

with client.ai.chat.stream(...) as stream:
    for event in stream:
        if event.type == "content":
            print(event.content, end="", flush=True)

        elif event.is_agent_event:
            ev = event.agent_event
            if ev.event_type == AgentEvent.ORCHESTRATION_START:
                for ag in ev.data.get("agents", []):
                    print(f"  Agent [{ag['id']}] {ag['name']}")
            elif ev.event_type == AgentEvent.TOOL_CALL:
                print(f"  Tool: {ev.data['tool_name']}")
            elif ev.event_type == AgentEvent.TOOL_RESULT:
                print(f"  Result: {ev.data['result'][:100]}")
            elif ev.event_type == AgentEvent.AGENT_FINISHED:
                print(f"  Done: {ev.data['stop_reason']} "
                      f"({ev.data['findings']} findings)")

        elif event.type == "complete":
            print("\nStream finished!")
```

## Agents

Agents are the AI-powered workers that execute tasks in Rank. Each agent has a type, belongs to a phase, runs on a specific AI model, and has access to tools and MCP servers.

### Agent Types and Phases

There are two agent types, each associated with different phases:

| `agent_type` | Phase | `phase_id` | Purpose |
|---|---|---|---|
| `pentest` | Initial Reconnaissance | 1 | OSINT, asset discovery, subdomain enumeration, technology fingerprinting |
| `pentest` | Enumeration | 2 | Service/port scanning, directory brute-forcing, deep enumeration |
| `pentest` | Analysis | 3 | Vulnerability analysis, CVE identification, attack vector prioritization |
| `general` | General | 6 | General-purpose chat agent for research, analysis, and tasks outside of pentests |

**Pentest agents** are assigned to a specific phase and execute during that phase of a pentest. **General agents** are used in [AI Chat](#ai-chat) for agentic research, investigations, and any task that doesn't involve running a pentest.

```python
# List pentest agents (filterable by phase)
pentest_agents = client.agents.list(type="pentest")
phase1_agents = client.agents.list(type="pentest", phase_id=1)

# List general agents
general_agents = client.agents.list(type="general")

# List all agents grouped by ownership (own / team / default)
grouped = client.agents.list()
for a in grouped.own_agents:
    print(f"{a.name} — {a.agent_type} — phase {a.phase_id}")
```

### AI Models

Before creating agents, you need to have AI models available in your account. List the global model catalog, assign the ones you want, and then use your assigned models when creating agents:

```python
# List all available models in the platform
all_models = client.agents.models.list()
for m in all_models.items:
    print(f"[{m.id}] {m.name} ({m.company})")

# Assign models to your account
client.agents.models.assign(model_ids=[5, 6, 12])

# List your assigned models — these are the ones you can use for agents
my_models = client.agents.models.mine()
for m in my_models.items:
    print(f"[{m.id}] {m.name}")

# Remove a model from your account
client.agents.models.remove(model_id=5)
```

### Creating and Managing Agents

```python
# Create a pentest agent for phase 1 (reconnaissance)
agent = client.agents.create(
    name="Custom Recon Agent",
    instructions="Perform thorough reconnaissance on the target. "
                 "Enumerate subdomains, scan for open ports, and identify technologies.",
    agent_type="pentest",
    phase_id=1,
    model_id=6,
)

# Create a general agent for research tasks
general_agent = client.agents.create(
    name="CVE Researcher",
    instructions="You are a security researcher specialized in CVE analysis. "
                 "Always include NVD links and CVSS scores in your responses.",
    agent_type="general",
    phase_id=6,
    model_id=6,
)

# Update, clone, or delete
client.agents.update(agent.agent.id, name="Recon Agent v2")
cloned = client.agents.clone(agent.agent.id)
client.agents.delete(agent.agent.id)
```

### Reasoning: effort and thinking

Agents can override the reasoning behaviour of their model. Two optional settings are available on `create` and `update` (and on `client.teams.agents.create`):

- `effort`: how much reasoning depth the agent uses. Valid values, ordered by ascending intensity, are `"none"`, `"minimal"`, `"low"`, `"medium"`, `"high"`, `"xhigh"`, `"max"`.
- `thinking_enabled`: turns the agent's thinking/reasoning on or off.

Both are optional. When omitted, the agent inherits the model default. A value is only accepted if the model supports it — check the model's capabilities first via `supports_effort`, `effort_values`, `default_effort`, and `supports_thinking_toggle`:

```python
# Inspect what a model supports before configuring an agent
model = client.agents.models.retrieve(model_id=6)
print(model.supports_effort, model.effort_values, model.default_effort)
print(model.supports_thinking_toggle)

# Create an agent with an explicit reasoning configuration
agent = client.agents.create(
    name="Deep Recon Agent",
    instructions="Perform an in-depth reconnaissance of the target.",
    agent_type="pentest",
    phase_id=1,
    model_id=6,
    effort="high",
    thinking_enabled=True,
)

# Change the reasoning configuration later
client.agents.update(agent.agent.id, effort="medium", thinking_enabled=False)

# The resolved values are returned on the agent object
detail = client.agents.retrieve(agent.agent.id)
print(detail.effort, detail.thinking_enabled)
```

### Tools

Each phase has a set of available tools (scanners, fuzzers, enumeration utilities, etc.). You can customize which tools an agent has access to:

```python
# List tools currently assigned to an agent
tools = client.agents.tools.list(agent_id=10)
for t in tools.items:
    print(f"[{t.id}] {t.name}")

# List all tools available for that agent's phase
available = client.agents.tools.available(agent_id=10)

# Assign tools
client.agents.tools.assign(agent_id=10, tool_ids=[1, 2, 3])

# Remove a tool
client.agents.tools.remove(agent_id=10, tool_id=3)
```

### MCP Servers

To give agents more capabilities — especially during pentests — you can connect [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) servers. This lets agents interact with external services, databases, custom tooling, or internal APIs, making pentests significantly more robust.

```python
# Create an MCP server
server = client.agents.mcp_servers.create(
    name="Internal Tooling MCP",
    transport_type="http",
    url="https://mcp.internal.example.com",
)

# List your MCP servers
servers = client.agents.mcp_servers.list()
for s in servers.items:
    print(f"[{s.id}] {s.name} — {s.url}")

# Assign MCP servers to an agent
client.agents.mcps.assign(agent_id=10, mcp_server_ids=[server.id])

# List MCP servers assigned to an agent
agent_mcps = client.agents.mcps.list(agent_id=10)

# Remove an MCP server from an agent
client.agents.mcps.remove(agent_id=10, mcp_id=server.id)

# Delete an MCP server
client.agents.mcp_servers.delete(server_id=server.id)
```

## Teams

Teams are the collaboration layer of Rank. All team resources — pentests, agents, chats, and usage — are **only accessible to members with the appropriate permissions**. This means it's critical to set up a proper role and permission structure before inviting members.

### Create a Team and Define Roles

```python
# Create a team
team = client.teams.create(name="Security Team", description="Red team operations")

# List available permissions in the platform
permissions = client.permissions.list()
for p in permissions.items:
    print(f"[{p.id}] {p.name}")

# Create roles with specific permissions
admin_role = client.teams.roles.create(team.id, name="Team Admin")
client.teams.roles.add_permissions(team.id, admin_role.id, permission_ids=[1, 2, 3, 4, 5])

pentester_role = client.teams.roles.create(team.id, name="Pentester")
client.teams.roles.add_permissions(team.id, pentester_role.id, permission_ids=[1, 2, 3])

viewer_role = client.teams.roles.create(team.id, name="Viewer")
client.teams.roles.add_permissions(team.id, viewer_role.id, permission_ids=[1])
```

### Invite Members

When inviting a member, you assign them a role that determines what they can see and do within the team:

```python
# Invite with a specific role
client.teams.invitations.create(team.id, email="pentester@example.com", role_id=pentester_role.id)
client.teams.invitations.create(team.id, email="manager@example.com", role_id=viewer_role.id)

# List pending invitations
invitations = client.teams.invitations.list(team.id)
```

### Members and Role Management

```python
# List members
members = client.teams.members.list(team.id)
for m in members.items:
    print(f"{m.username} — roles: {[r.name for r in m.roles]}")

# Assign a role to a member
client.teams.roles.assign_to_member(team.id, admin_role.id, user_id=5)

# Remove a role from a member
client.teams.roles.remove_from_member(team.id, pentester_role.id, user_id=5)

# Remove a member from the team
client.teams.members.remove(team.id, user_id=5)
```

### Team Resources

Agents and pentests associated with a team are shared among its members (according to their permissions):

```python
# Team agents — share agents with the team
client.teams.agents.create(team.id, agent_id=10)
team_agents = client.teams.agents.list(team.id)

# Team pentests
pentests = client.teams.pentests(team.id)
```

### Usage and Ownership

```python
# Usage summary and breakdown
usage = client.teams.usage.summary(team.id)
client.teams.usage.daily(team.id)
client.teams.usage.members(team.id)

# Transfer ownership
client.teams.transfer(team.id, new_owner_id=5)

# Leave a team
client.teams.leave(team.id)
```

## Usage

Monitor your personal spending and control costs. Every AI operation (chat messages, pentest executions, vulnerability processing) consumes usage based on the model used.

```python
# Get a summary of your current billing period
summary = client.usage.summary()
print(f"Budget: ${summary.budget.limit_usd}")
print(f"Used:   ${summary.budget.used_usd}")

# Filter by month or date range
summary = client.usage.summary(month="2026-03")
summary = client.usage.summary(from_date="2026-03-01", to_date="2026-03-15")

# Daily breakdown (last 7 or 30 days)
daily = client.usage.daily(period="7d")
for entry in daily.daily:
    print(f"{entry.date}: ${entry.cost_usd}")

# Hourly breakdown for a specific day
hourly = client.usage.daily(date="2026-03-20")

# Full usage history (paginated log of every operation)
history = client.usage.history(page=1, per_page=50)

# Enable on-demand usage with a spending cap
client.usage.toggle_on_demand(enabled=True, limit_usd=50.0)

# Disable on-demand usage
client.usage.toggle_on_demand(enabled=False)
```

## Chats

Manage conversation sessions, share with teams, and access operation history:

```python
# CRUD
chat = client.chats.create(nombre="My Session")
client.chats.update(chat.id, nombre="Renamed Session")
client.chats.delete(chat.id)

# List chats
all_chats = client.chats.list()
my_chats = client.chats.mine()
shared_chats = client.chats.shared()

# Archive / unarchive
client.chats.archive(chat_id=1)
client.chats.unarchive(chat_id=1)

# Share with a team
client.chats.share(chat_id=1, team_id=4)
client.chats.unshare(chat_id=1, team_id=4)
client.chats.unshare_all(chat_id=1)

# Operations (message history)
ops = client.chats.operations.list(chat_id=1)
client.chats.operations.assign(chat_id=1, operations=[...])
client.chats.operations.delete(chat_id=1, operation_id=10)

# Operation logs
logs = client.chats.operation_logs.list()
log = client.chats.operation_logs.retrieve(operation_id=5)
```

## Tickets (Jira)

Create and manage Jira tickets directly from the SDK:

```python
# List tickets
tickets = client.tickets.list()
for t in tickets.items:
    print(f"{t.jira_key}: {t.summary}")

# Create a ticket
ticket = client.tickets.create(
    summary="XSS in login form",
    description="Reflected XSS via the redirect_url parameter",
    issue_type="Bug",
)

# Get details
ticket = client.tickets.retrieve(ticket_id=1)

# Comments
client.tickets.add_comment(ticket_id=1, comment="Confirmed and assigned")
client.tickets.update_comment(ticket_id=1, comment_id="10042", comment="Updated note")
client.tickets.delete_comment(ticket_id=1, comment_id="10042")

# Attachments
files = [("file", ("evidence.png", open("evidence.png", "rb"), "image/png"))]
client.tickets.add_attachment(ticket_id=1, file=files)

# Sync with Jira
client.tickets.sync(ticket_id=1)

# Delete
client.tickets.delete(ticket_id=1)
```

## Error Handling

The SDK raises typed exceptions based on HTTP status codes:

```python
import rank

client = rank.Rank()

try:
    client.pentests.retrieve(999999)
except rank.NotFoundError as e:
    print(f"Not found: {e.message}")
    print(f"Status: {e.status_code}")  # 404
except rank.AuthenticationError:
    print("Invalid or missing API key")
except rank.PermissionDeniedError:
    print("Insufficient permissions")
except rank.UnprocessableEntityError as e:
    print(f"Validation error: {e.body}")
except rank.RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
except rank.InternalServerError:
    print("Server error, try again later")
except rank.APIConnectionError:
    print("Network error — check your connection")
except rank.APITimeoutError:
    print("Request timed out")
except rank.APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

**Exception hierarchy:**

```
RankError
├── APIError
│   ├── AuthenticationError (401)
│   ├── PermissionDeniedError (403)
│   ├── NotFoundError (404)
│   ├── ConflictError (409)
│   ├── UnprocessableEntityError (422)
│   ├── RateLimitError (429)
│   └── InternalServerError (5xx)
├── APIConnectionError
└── APITimeoutError
```

## Async Usage

Every method has an async counterpart via `AsyncRank`:

```python
import asyncio
import rank

async def main():
    client = rank.AsyncRank(api_key="rk_...")

    # All methods are awaitable
    pentests = await client.pentests.list()
    for p in pentests.items:
        print(p.name)

    # Streaming uses async for
    async with await client.ai.chat.stream(
        agent_id=23,
        user_prompt="Hello!",
        chat_id=1,
    ) as stream:
        async for event in stream:
            if event.type == "content":
                print(event.content, end="", flush=True)

    await client.close()

asyncio.run(main())
```

Both clients support context managers for automatic cleanup:

```python
# Sync
with rank.Rank() as client:
    client.pentests.list()

# Async
async with rank.AsyncRank() as client:
    await client.pentests.list()
```

## Configuration

```python
client = rank.Rank(
    api_key="rk_...",

    # Override backend URLs (defaults to Rank production servers)
    base_url="https://api.aleex-rank.ai",          # PHP backend
    agent_base_url="https://aleex.aleex-rank.ai",   # Go backend (AI/streaming)

    # Timeouts and retries
    timeout=60.0,       # Request timeout in seconds (default: 60)
    max_retries=2,      # Automatic retries on 5xx/network errors (default: 2)

    # Custom headers added to every request
    custom_headers={"X-Request-Source": "ci-pipeline"},
)
```

**Environment variables:**

| Variable | Description | Default |
|---|---|---|
| `RANK_API_KEY` | API key (`rk_...`) | — |
| `RANK_BASE_URL` | PHP backend URL | `https://api.aleex-rank.ai` |
| `RANK_AGENT_BASE_URL` | Go backend URL | `https://aleex.aleex-rank.ai` |

## Requirements

- **Python** >= 3.8
- [`httpx`](https://www.python-httpx.org/) >= 0.25.0
- [`pydantic`](https://docs.pydantic.dev/) >= 2.0
- [`typing_extensions`](https://pypi.org/project/typing-extensions/) >= 4.7
- [`anyio`](https://anyio.readthedocs.io/) >= 3.5.0
