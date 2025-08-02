#!/usr/bin/env python3
"""
Build script to create executable for Client Management Application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_directories():
    """Clean previous build directories"""
    directories_to_clean = ['build', 'dist', '__pycache__']
    
    for directory in directories_to_clean:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"Cleaned {directory} directory")
    
    # Clean .spec files
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"Removed {spec_file}")

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # PyInstaller command with options
    cmd = [
        'pyinstaller',
        '--onefile',                    # Create a single executable file
        '--windowed',                   # Hide console window (for GUI apps)
        '--name=ClientManager',         # Name of the executable
        '--icon=icon.ico',             # Application icon (if exists)
        '--add-data=config.py;.',      # Include config file
        '--hidden-import=customtkinter',
        '--hidden-import=mysql.connector',
        '--hidden-import=tkinter',
        '--hidden-import=decimal',
        '--hidden-import=datetime',
        '--collect-all=customtkinter',  # Collect all customtkinter files
        'main.py'
    ]
    
    # Remove icon parameter if icon file doesn't exist
    if not os.path.exists('icon.ico'):
        cmd = [item for item in cmd if not item.startswith('--icon')]
    
    try:
        subprocess.check_call(cmd)
        print("Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

def create_installer_script():
    """Create a simple installer script"""
    installer_content = '''
@echo off
echo Installing Client Management Application...

REM Create application directory
if not exist "C:\\Program Files\\ClientManager" mkdir "C:\\Program Files\\ClientManager"

REM Copy executable
copy "ClientManager.exe" "C:\\Program Files\\ClientManager\\ClientManager.exe"

REM Create desktop shortcut (optional)
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Client Manager.lnk'); $Shortcut.TargetPath = 'C:\\Program Files\\ClientManager\\ClientManager.exe'; $Shortcut.Save()"

echo Installation completed!
echo You can now run Client Manager from your desktop or from:
echo C:\\Program Files\\ClientManager\\ClientManager.exe
pause
'''
    
    with open('dist/install.bat', 'w') as f:
        f.write(installer_content)
    
    print("Installer script created: dist/install.bat")

def main():
    """Main build process"""
    print("=== Client Management Application - Build Process ===")
    
    # Step 1: Clean previous builds
    clean_build_directories()
    
    # Step 2: Install requirements
    if not install_requirements():
        print("Failed to install requirements. Exiting.")
        return
    
    # Step 3: Build executable
    if not build_executable():
        print("Failed to build executable. Exiting.")
        return
    
    # Step 4: Create installer script
    create_installer_script()
    
    print("\n=== Build Process Completed Successfully! ===")
    print("Your executable is located in: dist/ClientManager.exe")
    print("To install the application, run: dist/install.bat")
    print("\nNote: Make sure MySQL is installed and running on the target machine.")

if __name__ == '__main__':
    main()