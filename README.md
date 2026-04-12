---
title: ambiguity-env
sdk: docker
emoji: 🧠
colorTo: purple
---

# Ambiguity Resolution Environment

An RL environment where an AI agent resolves ambiguous real-world instructions by asking targeted clarifying questions before executing tasks.

## Overview
Real-world instructions are often incomplete. This environment trains agents to identify missing information, ask precise questions, and only execute once fully informed — mimicking how a smart assistant should behave.

## Tasks
| ID | Name | Difficulty | Required Fields |
|----|------|------------|----------------|
| task_easy_1 | Schedule Meeting | Easy | time, participants |
| task_easy_2 | Order Food | Easy | restaurant, items, delivery_address |
| task_medium_1 | Send Report | Medium | report_type, recipient, format |
| task_medium_2 | Book Cab | Medium | pickup_location, destination, time, cab_type |
| task_hard_1 | Plan Trip | Hard | destination, dates, budget, travelers |
| task_hard_2 | Organize Event | Hard | event_type, date, venue, guests, budget |

## Action Space
- `ask` — Ask a clarifying question to gather missing information
- `execute` — Complete the task once all required fields are known

## Reward Structure
- Rewards are shaped per step based on % of required fields discovered
- Score range: strictly between 0.1 and 0.9
- Penalty for repeating questions or asking useless questions
- Bonus progress for gathering multiple fields in one question

## API Endpoints
- `GET /` — Health check
- `GET /health` — Service status
- `GET /tasks` — List all tasks with grader info
- `POST /reset` — Run the inference agent across all tasks

## Environment Variables
| Variable | Description |
|----------|-------------|
| `API_BASE_URL` | LLM proxy endpoint |
| `API_KEY` | API key for LLM |
| `MODEL_NAME` | Model identifier (default: Qwen/Qwen2.5-72B-Instruct) |

## Local Setup
```bash
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

## Built With
- OpenEnv framework
- FastAPI
- Qwen 2.5 72B via HuggingFace router
- Docker