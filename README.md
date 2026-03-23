# Pygame Moving Dot

A simple pygame project with a controllable dot that moves around the screen using arrow keys.

## Requirements

- Python 3.10 or higher (Python 3.14 recommended)
- pip (Python package installer)

## Installing Python

If you don't have Python installed on your system:

### macOS

1. Visit https://www.python.org/downloads/
2. Download the latest Python 3.14 installer for macOS
3. Run the installer and follow the instructions

### Windows

1. Visit https://www.python.org/downloads/
2. Download the latest Python 3.14 installer for Windows
3. Run the installer
4. **Important**: Check "Add Python to PATH" during installation
5. Click "Install Now"

### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.14 python3.14-venv python3-pip
```

**Fedora:**
```bash
sudo dnf install python3.14
```

**Arch Linux:**
```bash
sudo pacman -S python
```

### Verify Installation

After installation, verify Python is installed:
```bash
python3 --version
```
You should see Python 3.10 or higher.

## Setup Instructions

After cloning this repository, follow these steps:

### 1. Create a virtual environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the game

```bash
python main.py
```

## Controls

- **Arrow Keys**: Move the dot up, down, left, or right
- **Close Window** or press the X button: Quit the game

## How It Works

The game runs a standard pygame loop at 60 FPS:
1. Handles user input (keyboard events)
2. Updates the dot position based on velocity
3. Wraps the dot around screen edges
4. Renders the dot on screen
