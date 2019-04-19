#!/usr/bin/env bash

python english_please.py

git add created_repo_issues.md
git commit -m "Created new issues. $(date "+%H:%M %F")"
git push origin test_auto_server