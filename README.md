# Autonomous Multi-Stage Dockerfile Generator and Validator Agent

An asynchronous multi-agent orchestration framework designed for automated infrastructure compliance. This utility implements an Evaluator-Optimizer design loop pattern utilizing the Google Gemini API to programmatically generate, securely audit, and automatically fix structural flaws in Dockerfile configurations prior to execution in continuous integration (CI) environments.

---

## Architecture Design Principles

Traditional Infrastructure-as-Code (IaC) verification relies on static rulesets that break linearly upon execution failure. This framework moves logic verification into a dynamic runtime loop by decoupling responsibilities into two distinct software agents:

1. Generator Agent: Orchestrates the contextual creation of multi-stage container files targeting specific enterprise tech stacks.
2. Validator Agent: Represents a rigid gatekeeping role, operating on standard corporate compliance frameworks (Shift-Left validation model).

The orchestrator establishes a closed-loop feedback block. If the Validator Agent identifies non-deterministic tags (such as using latest) or privilege vulnerabilities (running as root), it cancels disk deployment and dynamically feeds the feedback payload directly back into the Generator for state re-alignment.

---

## Technical Stack

* Language Environment: Python 3.11+
* LLM Engine: Google Gemini (gemini-2.5-flash)
* SDK: google-genai
* Pipeline Design Pattern: Evaluator-Optimizer Workflow

---

## Enterprise Compliance Rule Matrix

The Validator Agent judges all input parameters using the following structural evaluation criteria:

* Immutability Policy: Base images must use pinned deterministic variants. The usage of general tags like ':latest' triggers an automatic pipeline rejection.
* Minimum Privilege Policy: Explicit USER separation directives must exist. Containers executing execution vectors under administrative root accounts are blocked.
* Storage Optimization Policy: Multi-stage assembly layers are enforced via dual 'FROM' targets to isolate compilation noise from light distribution artifacts.

---

## Installation and Execution

### 1. Set Up Dependencies
Ensure the Google GenAI SDK package is installed in your runtime workspace:
```bash
pip install google-genai