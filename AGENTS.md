# Yogish AI Portfolio — Codex Project Instructions

## Project Overview

This repository contains Yogish Reddy Dwarampudi's AI-native personal portfolio.

The project is intended to demonstrate real engineering ability across:

* Cloud
* DevOps
* CI/CD
* AI Engineering
* RAG
* Agentic AI
* Full-stack development
* Security awareness

The portfolio should be technically credible and should never exaggerate Yogish's professional experience.

---

## Repository Structure

```text
yogish-portfolio/
├── frontend/
│   └── Next.js portfolio frontend
│
├── backend/
│   ├── main.py
│   ├── retriever.py
│   ├── query_rewriter.py
│   ├── build_index.py
│   ├── knowledge/
│   │   ├── documents.json
│   │   └── index.json
│   └── .env
│
└── AGENTS.md
```

Never expose `.env` or API keys.

---

# Current Architecture

The AI Portfolio Agent currently follows this flow:

```text
Frontend
    ↓
POST /chat
    ↓
message + conversation history
    ↓
main.py
    ↓
keep most recent 10 messages
    ↓
query_rewriter.py
    ↓
retrieval/search query
    ↓
retriever.py
    ↓
Gemini embedding
    ↓
768-dimensional embedding
    ↓
cosine similarity against knowledge index
    ↓
top-K documents
    ↓
similarity threshold
    ↓
knowledge context
    ↓
Gemini generation
    ↓
NDJSON streaming response
    ↓
Next.js UI
```

## Important architectural responsibility

`main.py` is the orchestration layer.

`query_rewriter.py` handles query preparation and conversational follow-up resolution.

`retriever.py` performs retrieval only.

`build_index.py` generates embeddings from `documents.json`.

Do NOT duplicate query rewriting inside `retriever.py`.

The current correct flow is:

```python
search_query = rewrite_query(
    request.message,
    recent_history,
)

results = retrieve(
    search_query,
    top_k=3,
)
```

Then `retriever.py` embeds `search_query`.

---

# Knowledge Base

The current knowledge base contains 22 documents covering:

* Profile
* Career direction
* Education
* Accenture experience
* Accenture responsibilities
* Cloud skills
* DevOps skills
* Programming skills
* AI skills
* Security background
* Supraja Technologies internship
* IEEE experience
* Student developer activities
* Grey Wolf college project
* College website project
* AI Portfolio Agent
* AI SRE Platform
* GraphicCore AI
* Certifications
* Learning style
* Strengths/development areas
* Personal interests

`documents.json` is the source of truth.

`index.json` is generated from `documents.json` and contains embeddings.

If documents are changed, regenerate the index using:

```bash
python build_index.py
```

Do not manually edit embeddings in `index.json`.

---

# Grounding Rules

The portfolio AI must never invent information about Yogish.

The knowledge context is the source of truth for factual claims about Yogish.

Do not turn:

* planned work into completed work
* learning into professional experience
* project technology into production experience
* capabilities into claimed outcomes
* concepts into implemented systems

Examples:

```text
"AI SRE Platform is planned to investigate incidents"
does NOT mean
"Yogish has deployed an AI incident-response platform."
```

```text
"Learning Kubernetes"
does NOT mean
"Professional Kubernetes production experience."
```

Be especially careful with AI, Kubernetes, security and cloud claims.

---

# Current Professional Experience

Yogish joined Accenture in September 2024 as an Associate Software Engineer.

He works as part of a CloudBees CI / Jenkins platform team.

The environment includes approximately:

* 9 lines of business
* 300+ Jenkins controllers
* approximately 3,000 builds per day
* managed controllers
* Operations Center
* static Windows/Linux VM agents
* ephemeral Kubernetes/EKS agents
* Docker images

His current work includes:

* Jenkins pipeline troubleshooting
* agent selection/connectivity troubleshooting
* pod-agent memory issues
* credentials configuration
* GitHub credentials
* third-party credentials such as SonarQube
* managed controller access processes
* plugin upgrades and validation
* quarterly platform upgrades
* agent connectivity validation
* Windows/Linux VM vulnerability remediation
* Docker base/custom image maintenance
* EKS workload monitoring
* Datadog
* AWS backup/restore
* Cloud Native Restore
* Jenkins operational automation jobs
* searching Jenkins/CJOC console output for specific information
* license recovery
* inactive user/controller/job cleanup
* Jira for stories/tasks
* ServiceNow for service requests/incidents

Yogish is still an Associate Software Engineer.

He has worked within the team and supported implementations, but should not be represented as independently architecting or owning major production platform implementations unless explicitly supported by the knowledge base.

---

# Skills Positioning

## Strong professional

AWS:

* AWS
* EC2
* ECR
* SSM
* EKS
* AWS backup/restore capabilities

DevOps:

* Jenkins
* CloudBees CI
* CI/CD
* GitHub
* Docker

Programming:

* Python
* Bash

## Working level

* Terraform
* Helm

## Basic professional

* Java

## Learning/personal projects

GCP:

* Strong personal learning/project experience
* Do not represent GCP as current professional production experience unless explicitly supported.

AI:

* LLMs
* RAG
* LangGraph
* Agentic AI
* Gemini APIs
* Gemini embeddings
* Gemini Live
* AI application development

AI technologies should currently be represented primarily as personal learning/projects, not professional production experience.

Security:

* cybersecurity
* ethical hacking
* penetration testing
* black-box testing
* Kali Linux
* OWASP
* Burp Suite
* Nmap
* Metasploit
* Wireshark
* cryptography

Security knowledge primarily comes from internship, college activities and personal learning.

Ansible should not be listed as a skill.

---

# Education

B.Tech in Computer Science:

NBKR Institute of Science and Technology (NBKRIST), Nellore

2020–2024

Final grade:

8.0 / 10

Higher secondary:

Narayana Junior College, Nellore

MPC

2018–2020

---

# College Projects

## Grey Wolf Algorithm for Wireless Sensor Networking

Completed B.Tech team project.

Team size: 4.

Python implementation.

Network simulator.

Purpose:

Use Grey Wolf Optimization to find efficient paths between wireless sensors and a receiver while considering lower latency and cost.

Inactive/damaged sensors are avoided in favor of active alternatives.

Yogish's contribution:

Worked on the Python implementation of the Grey Wolf Algorithm.

This project is completed.

## College Website

Completed college team project.

Technologies:

* PHP
* MySQL

The portal supported students and parents.

Features included:

* student details
* academic year
* branch
* mid-semester marks
* semester marks
* fee information
* semester balance
* fee payment-related information

Yogish worked on the backend responsible for fetching student records, grades and marks after authentication.

The project used sample data rather than the college's complete production database.

---

# Supraja Technologies Internship

8-week cybersecurity internship.

Yogish received the internship after participating in a college-organized cybersecurity hackathon/CTF.

Exposure included:

* ethical hacking
* penetration testing
* black-box testing
* Kali Linux VMs
* Bash
* PowerShell
* Python scripts
* cryptography
* OWASP
* Nmap
* Metasploit
* Burp Suite
* Wireshark

Do not describe this as professional cybersecurity employment.

---

# IEEE

Yogish was involved with IEEE for approximately three years during college.

Role:

Newsletter and Reporting Team Lead.

Led a team of 8.

Responsibilities included:

* documenting technical papers
* documenting technical news
* reporting events
* preparing IEEE-related content
* helping organize events with team leads

The IEEE team helped organize a three-day cybersecurity event.

The final day included an approximately 8-hour Capture The Flag competition.

---

# Student Developer Activities

Yogish participated in a student developer club that provided exposure to company-hosted technology programs and events.

He attended events including Microsoft events in Chennai and Bengaluru.

This should be represented as student participation/exposure rather than professional employment or significant contribution.

---

# Personal Projects

## AI Portfolio Agent

Current project.

Status:

Actively evolving production MVP.

Stack:

* Next.js
* FastAPI
* Gemini APIs
* Gemini embeddings
* RAG
* cosine similarity
* conversation history
* query rewriting
* streaming responses

The backend is deployed on Render.

The project is maintained through GitHub.

The project continuously evolves.

Current/ongoing exploration includes:

* improved knowledge base
* Gemini Live
* voice interaction
* additional AI capabilities

Do not mark it as completely finished while active development continues.

## AI SRE Platform

Personal project.

Status:

Building / early development.

Current work has established a local Jenkins environment.

Work performed so far includes:

* local Jenkins setup
* Jenkins builds
* Docker image experimentation
* SonarQube security testing

The AI agent itself has not yet been implemented.

Planned direction includes:

* incident investigation
* CI/CD failure analysis
* evidence gathering
* safe remediation assistance
* LangGraph
* RAG
* AWS
* Kubernetes

Do not claim those planned technologies are already implemented in this project.

## GraphicCore AI

Concept/exploration stage.

Concept:

An entertainment platform that understands user input and provides personalized recommendations and responses.

Potential interaction:

* text
* voice

Detailed implementation has not yet been finalized.

---

# Career Direction

Yogish does not consider AI a replacement for or departure from Cloud/DevOps.

His direction is to build on Cloud and DevOps knowledge and combine it with AI to create more advanced products.

His current interest is Agentic AI systems where a user can provide a single input and the system can complete the intended task with minimal manual work.

Long-term engineering goal:

Become an engineer capable of:

* architecting products at a high level
* quickly producing MVPs
* communicating architecture clearly
* explaining capabilities
* identifying security considerations
* explaining limitations and tradeoffs
* building systems capable of serving large numbers of users

---

# Strengths

Yogish considers these strengths:

* attention to detail
* in-depth understanding
* teamwork
* critical thinking
* communication

Current development areas:

* building more detailed and well-engineered products
* improving client communication

---

# Learning Style

Yogish prefers:

1. Understand the intended use case first.
2. Understand limitations.
3. Start building.
4. Use official documentation.
5. Learn from open-source projects.
6. Use AI models as pair-programming assistants.

He prefers building over watching large numbers of tutorials without applying the knowledge.

---

# Personal Interests

Yogish enjoys:

* chess
* comics
* manga/manhwa/manhua
* light novels
* AAA video games
* Spider-Man
* Grand Theft Auto: Vice City
* movies across many genres

---

# Current RAG Baseline

Current knowledge base size:

22 documents.

Embeddings:

Gemini `gemini-embedding-2`

Embedding dimension:

768

Retrieval:

Cosine similarity.

Current top-K:

3.

Current similarity threshold in `main.py`:

0.70.

The current system has demonstrated successful retrieval for:

* Accenture experience
* PHP/college website
* college projects
* AI projects
* education
* certifications
* personal interests

However, broad semantic queries can rank broad documents above more specific documents.

Example:

Query:

"What AI projects is Yogish currently building?"

Current retrieval observed:

1. AI Skills — 0.8458
2. Career Direction — 0.7940
3. AI Portfolio Agent — 0.7922

This indicates a retrieval-ranking problem rather than a query-rewriting failure.

Another example:

"What did Yogish build with PHP?"

Current retrieval:

1. College Website — 0.7701
2. AI Skills — 0.7589
3. Strengths — 0.7458

Correct document is retrieved first, but unrelated documents occupy the remaining slots.

Another example:

"What does Yogish do at Accenture?"

Current retrieval:

1. Accenture Experience — 0.7874
2. Strengths — 0.7692
3. Profile — 0.7682

The correct document is retrieved first.

---

# Important Current RAG Decision

Do NOT blindly change the embedding model.

Do NOT add a vector database simply because it is common in RAG projects.

Do NOT add complex infrastructure without demonstrating why it is needed.

The knowledge base currently has only 22 documents.

First evaluate and improve retrieval quality systematically.

Potential next improvement:

1. Structured metadata
2. Category-aware retrieval
3. Better ranking/reranking
4. Retrieval evaluation
5. Fallback behavior

Potential metadata categories:

* profile
* professional_experience
* skills
* education
* college_project
* personal_project
* internship
* certification
* extracurricular
* personal_interest
* career_direction

Metadata should complement semantic retrieval rather than replace it.

---

# Engineering Principles

Prioritize:

* correctness
* grounded answers
* maintainability
* security
* clear architecture
* minimal unnecessary dependencies
* explainable changes
* tests
* small incremental improvements

Do not perform large refactors without first explaining why they are necessary.

Before modifying architecture, inspect the existing implementation.

Before adding a dependency, determine whether the current stack can solve the problem.

Do not expose API keys.

Do not commit `.env`.

Run relevant tests after changes.

---

# Working Style

Yogish is learning while building.

When making significant changes:

1. Explain what problem the change solves.
2. Explain the architecture.
3. Implement the smallest useful version.
4. Run tests.
5. Show the result.
6. Explain what was learned.
7. Only then move to the next improvement.

Avoid dumping large amounts of code without explanation.

For complex changes, prefer a short implementation plan before modifying files.

---

# Deployment

Frontend:

Next.js.

Backend:

FastAPI.

Backend currently deployed on Render.

GitHub is used for source-code management.

Do not break the existing deployment contract without explaining the impact.

---

# Definition of Done

A feature is not complete merely because the code compiles.

For meaningful changes:

* code should run
* relevant tests should pass
* existing functionality should remain intact
* security considerations should be checked
* deployment implications should be considered
* documentation should be updated when architecture changes
