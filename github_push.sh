#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================${NC}"
echo -e "${BLUE}   Agentforce MCP Server - GitHub Push Script        ${NC}"
echo -e "${BLUE}=====================================================${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git is not installed. Please install git and try again.${NC}"
    exit 1
fi

# Get the current directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Check if .env file exists and warn the user
if [ -f ".env" ]; then
    echo -e "${YELLOW}WARNING: .env file detected. This file contains sensitive information and should NOT be pushed to GitHub.${NC}"
    echo -e "${YELLOW}The .env file has been added to .gitignore, but please verify it won't be included in your commit.${NC}"
    echo ""
fi

# Ask for GitHub repository URL
echo -e "${BLUE}Please enter your GitHub repository URL (e.g., https://github.com/username/repo.git):${NC}"
read -r REPO_URL

if [ -z "$REPO_URL" ]; then
    echo -e "${RED}No repository URL provided. Exiting.${NC}"
    exit 1
fi

# Check if the directory is already a git repository
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    echo -e "${GREEN}Git repository initialized.${NC}"
else
    echo -e "${GREEN}Git repository already exists.${NC}"
fi

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo -e "${YELLOW}Remote 'origin' already exists. Updating to new URL...${NC}"
    git remote set-url origin "$REPO_URL"
else
    echo -e "${YELLOW}Adding remote 'origin'...${NC}"
    git remote add origin "$REPO_URL"
fi

echo -e "${GREEN}Remote 'origin' set to: $REPO_URL${NC}"

# Add all files to git
echo -e "${YELLOW}Adding files to git...${NC}"
git add .

# Show status
echo -e "${YELLOW}Git status:${NC}"
git status

# Confirm with user before committing
echo -e "${BLUE}Review the files above. Are you sure you want to commit these files? (y/n)${NC}"
read -r CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo -e "${RED}Commit aborted by user.${NC}"
    exit 1
fi

# Commit
echo -e "${YELLOW}Committing changes...${NC}"
git commit -m "Initial commit of Agentforce MCP Server"

# Push to GitHub
echo -e "${YELLOW}Pushing to GitHub...${NC}"
git push -u origin master || git push -u origin main

# Final message
echo -e "${GREEN}Push completed! Your code should now be on GitHub.${NC}"
echo -e "${BLUE}=====================================================${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Ensure your .env file is not published (it should be in .gitignore)"
echo -e "2. Share the .env.example file with users so they know what environment variables to set"
echo -e "3. Update the README.md if needed with specific instructions for your repository"
echo -e "${BLUE}=====================================================${NC}"
