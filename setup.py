import ctypes
import os
import shutil
import subprocess
import sys


SYSTEM_PATH = "C:\windows\system32" 
MAKE_BAT_FILE_NAME = "make.bat"
MAKEFILE_TARGETS_NAME = "make_targets.py"
AUTOCOMPLETE_PS_NAME = "make_autocomplete.ps1"


def is_admin_shell() -> bool:
    """
    Ensure the shell running this script is an admin shell.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False


def has_mingw32_make() -> bool:
    """
    Ensure mingw32 is already installed on this device.
    """
    try:
        result = subprocess.run(["mingw32-make", "--version"], capture_output=True, text=True, check=True)        
        print(f"mingw32-make is installed. Version info: {result.stdout}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

    
def copy_makefile_target_file(file_name: str) -> bool:
    """
    Copy the source files to the system path.

    Args:
        file_name (str): File to be copied.
    """
    current_dir = os.getcwd()
    all_files = os.listdir(current_dir)
    if not any(f for f in all_files if os.path.isfile(os.path.join(current_dir, f)) and f == file_name):
        print(f"{file_name} was not found in the current directory")
        return False
    try:
        shutil.copy(file_name, SYSTEM_PATH)        
        print(f"Copied {file_name} to {SYSTEM_PATH}")
        return True
    except (shutil.Error, FileNotFoundError):
        return False


def update_powershell_profile() -> bool:
    """
    Update the Powershell profile to include AUTOCOMPLETE_PS_NAME.

    """
    try:
        result = subprocess.run(["powershell", "$PROFILE"], capture_output=True, text=True)
        profile = result.stdout.strip().split("\n")[-1]
        with open(profile, "a") as f:
            f.write(f"\n. {SYSTEM_PATH}\{AUTOCOMPLETE_PS_NAME}")   
        return True
    except Exception as e:
        print(e)
        return False
    

def install():
    """
    Install the nessesary files to allow make autocomplete to function properly.
    """
    if os.name != "nt":
        print("Machine must be Windows")
        return    
    if not is_admin_shell():
        print("Must run script with admin rights")
        return
    if not has_mingw32_make():
        print("mingw32-make is not installed or not in the system PATH.")
        print("Install using: https://sourceforge.net/projects/mingw/files/MinGW/Extension/make/mingw32-make-3.80-3/mingw32-make-3.80.0-3.exe/download?use_mirror=versaweb&download=")
        return
    for file in [MAKE_BAT_FILE_NAME, MAKEFILE_TARGETS_NAME, AUTOCOMPLETE_PS_NAME]:    
        if not copy_makefile_target_file(file):
            print(f"Failed to create {file} file")
            return
    if not update_powershell_profile():
        print("Failed to update powershell profile")
        return
    
    print("Make autocomplete setup done!")
    print("run '. $PROFILE' to finish the setup process")
    
    
def uninstall():
    """
    Uninstall make autocomplete.
    """
    # remove files
    for file in [MAKE_BAT_FILE_NAME, MAKEFILE_TARGETS_NAME, AUTOCOMPLETE_PS_NAME]:    
        os.remove(f"{SYSTEM_PATH}\{file}")
    
    # update profile
    result = subprocess.run(["powershell", "$PROFILE"], capture_output=True, text=True)
    profile = result.stdout.strip().split("\n")[-1]
    try:
        with open(profile, 'r') as file:
            lines = file.readlines()

        lines = [line for line in lines if line.strip() != f". {SYSTEM_PATH}\{AUTOCOMPLETE_PS_NAME}"]
        with open(profile, 'w') as file:
            file.writelines(lines)
        print("Uninstall done!")
    except Exception as e:
        print("Failed to uninstall")

    
if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        install()
    elif len(sys.argv) >= 2:
        if sys.argv[1] == "uninstall":
            uninstall()
        else:
            print("Unknown first argument. Arument can only be 'uninstall'")
    else:
        print("Too many arguments")