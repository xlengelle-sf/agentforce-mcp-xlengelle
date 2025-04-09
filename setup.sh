#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}        Agentforce MCP Server - Setup Script        ${NC}"
echo -e "${BLUE}======================================================${NC}"
echo

# Update Homebrew if it exists
if command -v brew &> /dev/null; then
    echo -e "${YELLOW}Updating Homebrew...${NC}"
    brew update
    echo -e "${GREEN}Homebrew updated successfully.${NC}"

    # Check if Python is installed via Homebrew
    if ! brew list python@3.10 &> /dev/null; then
        echo -e "${YELLOW}Installing Python 3.10 via Homebrew...${NC}"
        brew install python@3.10
        echo -e "${GREEN}Python 3.10 installed successfully.${NC}"
    else
        echo -e "${GREEN}Python 3.10 is already installed.${NC}"
    fi
fi

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Python not found. Please install Python 3.10 or higher and try again.${NC}"
    exit 1
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_CMD --version | cut -d " " -f 2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"

# Check Python version is at least 3.10
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${RED}Python 3.10 or higher is required. You have Python $PYTHON_VERSION.${NC}"
    echo -e "${RED}Please install a newer version of Python and try again.${NC}"
    exit 1
fi

# Create and activate virtual environment
VENV_DIR=".venv"
echo -e "${YELLOW}Creating virtual environment in $VENV_DIR...${NC}"

# Remove existing venv if it exists
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Removing existing virtual environment...${NC}"
    rm -rf "$VENV_DIR"
fi

# Create a new virtual environment
$PYTHON_CMD -m venv "$VENV_DIR"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create virtual environment. Please check if you have venv module installed.${NC}"
    echo -e "${YELLOW}You can install it with: pip install --user virtualenv${NC}"
    exit 1
fi

echo -e "${GREEN}Virtual environment created successfully.${NC}"

# Activate the virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment.${NC}"
    exit 1
fi

echo -e "${GREEN}Virtual environment activated successfully.${NC}"

# Upgrade pip in the virtual environment
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to upgrade pip. Continuing anyway...${NC}"
fi

# Install dependencies
echo -e "${YELLOW}Installing required dependencies...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install dependencies. Please check the error message above and try again.${NC}"
    exit 1
fi
echo -e "${GREEN}Dependencies installed successfully.${NC}"

# Make the server script executable
chmod +x agentforce_mcp_server.py

# Check if .env file already exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}An .env file already exists.${NC}"
    read -p "Do you want to overwrite it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Keeping existing .env file.${NC}"
        echo -e "${YELLOW}If you encounter issues, you can run this script again to recreate the file.${NC}"
    else
        # We'll create a new .env file below
        echo -e "${YELLOW}Creating new .env file...${NC}"
    fi
else
    # Create .env file
    echo -e "${YELLOW}Setting up your environment variables...${NC}"
fi

if [[ ! -f ".env" || $REPLY =~ ^[Yy]$ ]]; then
    # Get Salesforce credentials
    echo -e "${CYAN}Please enter your Salesforce credentials:${NC}"
    echo -e "${YELLOW}(Press Enter to skip any field and use empty value)${NC}"
    
    read -p "Salesforce Org ID: " ORG_ID
    read -p "Salesforce Agent ID: " AGENT_ID
    read -p "Salesforce Client ID (Consumer Key): " CLIENT_ID
    read -p "Salesforce Client Secret (Consumer Secret): " CLIENT_SECRET
    read -p "Salesforce Server URL (e.g., example.my.salesforce.com): " SERVER_URL
    
    # Create .env file
    cat > .env << EOF
SALESFORCE_ORG_ID="${ORG_ID}"
SALESFORCE_AGENT_ID="${AGENT_ID}"
SALESFORCE_CLIENT_ID="${CLIENT_ID}"
SALESFORCE_CLIENT_SECRET="${CLIENT_SECRET}"
SALESFORCE_SERVER_URL="${SERVER_URL}"
EOF
    
    echo -e "${GREEN}.env file created successfully.${NC}"
fi

# Check if we want to test the setup
echo
read -p "Do you want to test the setup now? (y/n): " -n 1 -r TEST_SETUP
echo

if [[ $TEST_SETUP =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Testing Agentforce connection...${NC}"
    echo -e "${YELLOW}This will attempt to authenticate and create a session.${NC}"
    
    python test_agentforce.py
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Test failed. Please check your credentials and try again.${NC}"
    else
        echo -e "${GREEN}Test completed. Your setup is working!${NC}"
    fi
fi

# Check if we want to start the server
echo
read -p "Do you want to start the MCP server now? (y/n): " -n 1 -r START_SERVER
echo

if [[ $START_SERVER =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Starting Agentforce MCP Server...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop the server.${NC}"
    
    python agentforce_mcp_server.py
else
    # Provide instructions for setting up Claude Desktop
    echo -e "${BLUE}======================================================${NC}"
    echo -e "${BLUE}          Claude Desktop Configuration Guide           ${NC}"
    echo -e "${BLUE}======================================================${NC}"
    echo
    echo -e "${CYAN}To use this server with Claude Desktop:${NC}"
    echo
    echo -e "1. Locate your Claude Desktop configuration file:"
    echo -e "   ${YELLOW}macOS:${NC} ~/Library/Application Support/Claude/claude_desktop_config.json"
    echo -e "   ${YELLOW}Windows:${NC} %APPDATA%\\Claude\\claude_desktop_config.json"
    echo
    echo -e "2. Add the following to your configuration:"
    echo
    echo -e "${YELLOW}```json"
    echo -e "{"
    echo -e "  \"mcpServers\": {"
    echo -e "    \"agentforce\": {"
    echo -e "      \"command\": \"$(pwd)/$VENV_DIR/bin/python\","
    echo -e "      \"args\": ["
    echo -e "        \"$(pwd)/agentforce_mcp_server.py\""
    echo -e "      ]"
    echo -e "    }"
    echo -e "  }"
    echo -e "}"
    echo -e "```${NC}"
    echo
    echo -e "3. Restart Claude Desktop"
    echo
    echo -e "4. Start a conversation with Claude and look for the hammer icon in the input box"
    echo -e "   This indicates that MCP tools are available."
    echo
    echo -e "${GREEN}You can start the server at any time by running:${NC}"
    echo -e "${YELLOW}source .venv/bin/activate && python agentforce_mcp_server.py${NC}"
    echo
    echo -e "${BLUE}======================================================${NC}"
fi

echo -e "\n${GREEN}Setup complete!${NC}"

# Deactivate virtual environment if we're not starting the server
if [[ ! $START_SERVER =~ ^[Yy]$ ]]; then
    deactivate 2>/dev/null || true
fi
