# GitHub Publish Guide

## 1) Create repository

Recommended repo name:

- `openclaw-agent-autotune`

## 2) Push

```bash
cd skills/openclaw-agent-autotune
git init
git add .
git commit -m "feat: initial release openclaw-agent-autotune"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## 3) Suggested release title

`v0.1.0 — Initial public release`

## 4) Suggested release notes

- Introduced safe OpenClaw autotune loop (candidate -> benchmark -> keep/rollback)
- Added scoring model and hard safety gates
- Included benchmark/program/results examples
- Added MIT license
