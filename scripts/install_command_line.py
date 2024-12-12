import os
import stat
import shutil

def find_script(script_name, search_dir="."):
    for root, dirs, files in os.walk(search_dir):
        if script_name in files:
            return os.path.join(root, script_name)
    return None

def prepare_script(script_name, search_dir=".", destination_dir="/usr/local/bin"):
    script_path = find_script(script_name, search_dir)
    if not script_path:
        print(f"Script {script_name} not found in {search_dir}")
        return
    
    # Add shebang line if not present
    with open(script_path, 'r') as file:
        lines = file.readlines()
    
    if not lines[0].startswith("#!"):
        lines.insert(0, "#!/usr/bin/env python3\n")
        with open(script_path, 'w') as file:
            file.writelines(lines)
    
    # Make the script executable
    st = os.stat(script_path)
    os.chmod(script_path, st.st_mode | stat.S_IEXEC)
    
    # Copy the script to the destination directory
    script_name = os.path.basename(script_path)
    destination_path = os.path.join(destination_dir, script_name)
    shutil.copy(script_path, destination_path)
    os.chmod(destination_path, st.st_mode | stat.S_IEXEC)
    print(f"Script copied to {destination_path} and is now executable.")

# Usage
prepare_script("sip_message_command.py")