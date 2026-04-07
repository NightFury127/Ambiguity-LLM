---
title: ' ambiguity-env'
sdk: docker
emoji: 🚀
colorTo: yellow
---
# Ambiguity Resolution Environment

## Overview
This environment simulates real-world ambiguous instructions where an AI agent must ask clarifying questions before completing a task.

## Tasks
- Easy: Schedule a meeting
- Medium: Send a report
- Hard: Plan a trip

## Action Space
- ask: ask clarifying questions
- execute: complete task

## Reward
- +0.3 for correct clarification
- +1.0 for successful execution
- penalties for wrong questions

## How to Run
The environment runs via `inference.py` and logs steps in standard format.

## Deployment
Docker-based deployment on Hugging Face Spaces.