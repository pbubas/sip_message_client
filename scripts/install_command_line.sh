#!/bin/bash

COMMAND_NAME="sip_message"
SCRIPT_NAME="sip_message.py"
SEARCH_DIR="./cmd"
DESTINATION_DIR="/usr/local/bin"

# Function to find the script
find_script() {
    local script_name=$1
    local search_dir=$2
    find "$search_dir" -name "$script_name" -print -quit
}

# Function to prepare the script
prepare_script() {
    local script_name=$1
    local search_dir=$2
    local destination_dir=$3
    local command_name=$4

    local script_path
    script_path=$(find_script "$script_name" "$search_dir")

    if [ -z "$script_path" ]; then
        echo "Script $script_name not found in $search_dir"
        return 1
    fi

    # Add shebang line if not present
    if ! head -n 1 "$script_path" | grep -q "^#!"; then
        sed -i '1i#!/usr/bin/env python3' "$script_path"
    fi

    # Make the script executable
    chmod +x "$script_path"

    local destination_path="$destination_dir/$command_name"
    sudo cp "$script_path" "$destination_path"
    sudo chmod +x "$destination_path"

    echo "Script copied to $destination_path and is now executable."
}

# Run the prepare_script function
prepare_script "$SCRIPT_NAME" "$SEARCH_DIR" "$DESTINATION_DIR" "$COMMAND_NAME"