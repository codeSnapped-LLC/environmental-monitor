#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
VENV_NAME=".venv"
REQUIREMENTS="requirements.txt"
PYTHON_CMD="python3"
FIRMWARE_VERSION=$(dotnet-gitversion | jq -r '.SemVer')

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to create virtual environment
create_venv() {
    echo -e "${YELLOW}Creating UV virtual environment...${NC}"
    if ! $PYTHON_CMD -m venv $VENV_NAME; then
        echo -e "${RED}Failed to create virtual environment${NC}"
        exit 1
    fi
}

# Function to activate virtual environment
activate_venv() {
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    if [ -f "$VENV_NAME/bin/activate" ]; then
        source "$VENV_NAME/bin/activate"
    else
        echo -e "${RED}Virtual environment activation file not found${NC}"
        exit 1
    fi
}

# Function to install requirements
install_requirements() {
    echo -e "${YELLOW}Installing requirements...${NC}"
    if ! pip install -r $REQUIREMENTS; then
        echo -e "${RED}Failed to install requirements${NC}"
        exit 1
    fi
}

# Main execution
main() {
    # Check for Python
    if ! command_exists $PYTHON_CMD; then
        echo -e "${RED}Python3 is required but not installed${NC}"
        exit 1
    fi

    # Check for pip and jq
    if ! command_exists pip; then
        echo -e "${RED}pip is required but not installed${NC}"
        exit 1
    fi
    
    if ! command_exists jq; then
        echo -e "${YELLOW}Installing jq for JSON parsing...${NC}"
        sudo apt-get install -y jq
    fi
    
    if ! command_exists dotnet-gitversion; then
        echo -e "${YELLOW}Installing GitVersion...${NC}"
        dotnet tool install -g GitVersion.Tool
    fi

    # Create virtual environment
    if [ ! -d "$VENV_NAME" ]; then
        create_venv
    else
        echo -e "${GREEN}Virtual environment already exists${NC}"
    fi

    # Activate and install requirements
    activate_venv
    install_requirements

    echo -e "${GREEN}Setup completed successfully!${NC}"
    echo -e "To activate the environment manually, run:"
    echo -e "source $VENV_NAME/bin/activate"
}

# Run main function
main
