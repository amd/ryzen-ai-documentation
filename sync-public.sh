#!/bin/bash
# sync-public.sh

# Add some safety checks
echo "Syncing main branch to public repository..."

# Ensure we're on the main branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "Error: Not on main branch. Currently on: $current_branch"
    exit 1
fi

# merge the remote changes first
git pull https://github.com/amd/ryzen-ai-documentation.git main
# Push to public repo
git push https://github.com/amd/ryzen-ai-documentation.git main:main

if [ $? -eq 0 ]; then
    echo "Successfully synced main branch to public repository!"
else
    echo "Failed to sync to public repository"
    exit 1
fi
