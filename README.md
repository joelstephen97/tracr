# Tracr Tool

Tracer is a Python tool that follows a given URL, scrapes images from the website along with their metadata (EXIF), and organizes them into a folder tree reflecting the link hierarchy. If the link contains further links, Tracer will recursively follow them up to a specified depth (default is 5, configurable via command-line arguments).

## Features

- **Recursive Traversal:** Follow links up to a configurable maximum depth.
- **Image Downloading:** Downloads all images found on each page.
- **Metadata Extraction:** Saves image metadata (format, size, mode, and EXIF data if available) into a corresponding text file.
- **Folder Organization:** Creates a folder structure that mirrors the link hierarchy.

## Requirements

- Python 3.x
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [Pillow](https://pypi.org/project/Pillow/)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd tracr
   ```

2. **Create a Virtual Environment:**
   On Windows, open PowerShell and run:
   ```powershell
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - **Using PowerShell:**  
     If you encounter an execution policy error, open PowerShell as Administrator and run:
     ```powershell
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
     Then activate the virtual environment:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

   - **Using Command Prompt:**  
     ```cmd
     venv\Scripts\activate
     ```

   Once activated, you should see `(venv)` prefixed on your command line.

4. **Install Dependencies:**
   With the virtual environment activated, install all required packages using:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Tracer tool with the following command:
```bash
python tracer.py <starting_url> --depth <max_depth> --output <output_folder>
```
- `<starting_url>`: The URL where the tracer begins.
- `--depth <max_depth>`: (Optional) The maximum depth to traverse. Default is 5.
- `--output <output_folder>`: (Optional) The folder where output will be stored. Default is `output`.

Example:
```bash
python tracer.py https://example.com --depth 5 --output tracer_output
```

## Virtual Environment Management

### Activating the Virtual Environment
- **PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Command Prompt:**
  ```cmd
  venv\Scripts\activate
  ```

### Deactivating the Virtual Environment

To deactivate the virtual environment, simply run:
```bash
deactivate
```
