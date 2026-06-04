# SYSTEM_CONTRACT.md

# Workflow Architect - System Contract

Version: 1.0

Purpose:
This document defines the shared data structure used across all modules of Workflow Architect.

Every component (Frontend, Backend, AI Engine, Database) must follow this contract.

Changes to this contract must be discussed and approved by all contributors before implementation.

---

# Top-Level Response Schema

```json
{
  "goal": {},
  "deliverables": [],
  "recommended_tools": [],
  "workflow": [],
  "alternative_workflows": {},
  "knowledge_areas": {},
  "estimated_time": ""
}
```

---

# 1. Goal

Description:
Represents the analyzed understanding of the user's objective.

Schema:

```json
{
  "goal": {
    "user_input": "string",
    "domain": "string",
    "goal_type": "string",
    "complexity": "Low | Medium | High"
  }
}
```

Example:

```json
{
  "goal": {
    "user_input": "Build a portfolio website",
    "domain": "Web Development",
    "goal_type": "Portfolio Website",
    "complexity": "Medium"
  }
}
```

---

# 2. Deliverables

Description:
Major outputs required to achieve the goal.

Schema:

```json
{
  "deliverables": [
    {
      "id": 1,
      "title": "string",
      "description": "string"
    }
  ]
}
```

Example:

```json
{
  "deliverables": [
    {
      "id": 1,
      "title": "Portfolio Design",
      "description": "Create visual design and layout."
    },
    {
      "id": 2,
      "title": "Website Development",
      "description": "Build the portfolio website."
    }
  ]
}
```

---

# 3. Recommended Tools

Description:
Tools suggested for achieving the goal.

Schema:

```json
{
  "recommended_tools": [
    {
      "name": "string",
      "category": "AI | Development | Design | Productivity | Marketing | Other",
      "reason": "string"
    }
  ]
}
```

Example:

```json
{
  "recommended_tools": [
    {
      "name": "Figma",
      "category": "Design",
      "reason": "Create wireframes and UI layouts."
    },
    {
      "name": "React",
      "category": "Development",
      "reason": "Build interactive web applications."
    }
  ]
}
```

---

# 4. Workflow

Description:
Actionable execution steps.

Schema:

```json
{
  "workflow": [
    {
      "step_number": 1,
      "title": "string",
      "tool": "string",
      "why": "string",
      "what_to_do": "string",
      "prompt": "string",
      "expected_result": "string"
    }
  ]
}
```

Example:

```json
{
  "workflow": [
    {
      "step_number": 1,
      "title": "Create Website Structure",
      "tool": "ChatGPT",
      "why": "Generate an initial website structure.",
      "what_to_do": "Ask ChatGPT to generate page sections.",
      "prompt": "Generate a modern portfolio website structure for an AIML student.",
      "expected_result": "Website sitemap and page structure."
    }
  ]
}
```

Notes:

* prompt can be an empty string when not applicable.
* workflow steps must be sequential.

---

# 5. Alternative Workflows

Description:
Different approaches for achieving the same goal.

Schema:

```json
{
  "alternative_workflows": {
    "fastest": {
      "summary": "string",
      "tools": ["string"]
    },
    "cheapest": {
      "summary": "string",
      "tools": ["string"]
    },
    "highest_quality": {
      "summary": "string",
      "tools": ["string"]
    },
    "beginner_friendly": {
      "summary": "string",
      "tools": ["string"]
    }
  }
}
```

Example:

```json
{
  "alternative_workflows": {
    "fastest": {
      "summary": "Use AI-assisted builders.",
      "tools": ["Lovable", "Vercel"]
    },
    "cheapest": {
      "summary": "Use only free tools.",
      "tools": ["React", "GitHub Pages"]
    }
  }
}
```

---

# 6. Knowledge Areas

Description:
Knowledge domains related to the goal.

Schema:

```json
{
  "knowledge_areas": {
    "high": ["string"],
    "medium": ["string"],
    "low": ["string"]
  }
}
```

Example:

```json
{
  "knowledge_areas": {
    "high": ["HTML", "CSS", "Git"],
    "medium": ["React"],
    "low": ["SEO"]
  }
}
```

---

# 7. Estimated Time

Description:
Approximate completion time for the overall goal.

Schema:

```json
{
  "estimated_time": "string"
}
```

Example:

```json
{
  "estimated_time": "8-12 hours"
}
```

---

# Integration Rules

1. All modules must return valid JSON.

2. Field names must not be changed without updating this contract.

3. Frontend components should rely only on fields defined here.

4. AI modules must generate outputs matching this structure.

5. Missing values should use:

   * Empty string ("")
   * Empty array ([])
   * Empty object ({})
     instead of null whenever possible.

6. IDs should be unique within their respective arrays.

7. Workflow steps must always be ordered by step_number.

---

# Ownership Boundaries

Module A Responsibilities

* Deliverables Detection
* Workflow Generation
* Prompt Generation

Fields Owned:

* deliverables
* workflow

---

Module B Responsibilities

* Goal Analysis
* Tool Recommendation
* Knowledge Areas
* Time Estimation
* Alternative Workflows

Fields Owned:

* goal
* recommended_tools
* alternative_workflows
* knowledge_areas
* estimated_time

---

Shared Responsibilities

* API Design
* Frontend Integration
* Database Design
* Deployment
* Final Testing

```
```
