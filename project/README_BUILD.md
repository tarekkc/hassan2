# Building Executable for Client Management Application

This guide will help you create a standalone executable (.exe) file for the Client Management Application.

## Prerequisites

1. **Python 3.7+** installed on your system
2. **MySQL Server** installed and running
3. All application files in the correct directory structure

## Quick Build Process

### Option 1: Automated Build (Recommended)

1. Run the automated build script:
```bash
python build_exe.py
```

This will:
- Install all required dependencies
- Clean previous builds
- Create the executable
- Generate an installer script

### Option 2: Manual Build

1. **Install PyInstaller and dependencies:**
```bash
pip install -r requirements.txt
```

2. **Build the executable:**
```bash
pyinstaller client_manager.spec
```

3. **Find your executable:**
The executable will be created in the `dist/` folder as `ClientManager.exe`

## Distribution

### For End Users

1. **Copy the executable** (`dist/ClientManager.exe`) to the target machine
2. **Ensure MySQL is installed** and running on the target machine
3. **Create the database** using the SQL schema (see Database Setup below)
4. **Run the executable** - it should work without Python installed

### Using the Installer

1. Copy both `ClientManager.exe` and `install.bat` to the target machine
2. Run `install.bat` as Administrator
3. This will:
   - Install the application to `C:\Program Files\ClientManager\`
   - Create a desktop shortcut
   - Set up the application for easy access

## Database Setup

The target machine needs MySQL with the following database structure:

```sql
CREATE DATABASE client_management;
USE client_management;

-- Create tables
CREATE TABLE type_declaration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE regime_fiscal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    company VARCHAR(255),
    address TEXT,
    montant DECIMAL(10,2) DEFAULT 0.00,
    type VARCHAR(255),
    type_declaration_id INT,
    regime_fiscal_id INT,
    FOREIGN KEY (type_declaration_id) REFERENCES type_declaration(id),
    FOREIGN KEY (regime_fiscal_id) REFERENCES regime_fiscal(id)
);

CREATE TABLE versement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    montant DECIMAL(10,2) NOT NULL,
    type VARCHAR(255) NOT NULL,
    date_paiement DATE NOT NULL,
    annee_concernee INT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);
```

## Configuration

Update `config.py` if needed to match the target machine's MySQL configuration:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'client_management'
}
```

## Troubleshooting

### Common Issues:

1. **"MySQL not found" error:**
   - Ensure MySQL is installed and running
   - Check database credentials in `config.py`

2. **"Module not found" error:**
   - Rebuild with: `pyinstaller --clean client_manager.spec`

3. **Executable won't start:**
   - Run from command line to see error messages
   - Check if all dependencies are included

4. **Large file size:**
   - This is normal for PyInstaller executables
   - Consider using `--onedir` instead of `--onefile` for faster startup

### Build Options:

- **Smaller file size:** Use `--onedir` instead of `--onefile`
- **Debug mode:** Add `--debug=all` to see detailed startup information
- **Console window:** Remove `--windowed` to see console output for debugging

## File Structure After Build

```
your_project/
├── dist/
│   ├── ClientManager.exe    # Your executable
│   └── install.bat         # Installer script
├── build/                  # Build files (can be deleted)
└── ClientManager.spec      # PyInstaller specification
```

## Notes

- The executable is self-contained and doesn't require Python on the target machine
- MySQL must still be installed separately on each target machine
- The first run might be slower as the executable extracts files
- Consider creating an installer using tools like NSIS or Inno Setup for professional distribution