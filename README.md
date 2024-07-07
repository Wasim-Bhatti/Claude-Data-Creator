# Claude Data Creator

Claude Data Creator is a powerful tool that generates new CSV datasets based on sample data. It uses AI to analyze the structure and content of your input CSV and creates new, similar data. This tool is available both as a Python application with a GUI and as a Docker container for CLI usage.

## Table of Contents

1. [Using the Application from GitHub](#using-the-application-from-github)
2. [Using the Docker Image](#using-the-docker-image)
3. [Configuration](#configuration)
4. [Troubleshooting](#troubleshooting)

## Using the Application from GitHub

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/wasim-bhatti/claude-data-creator.git
   cd claude-data-creator
   ```

2. Install the required packages:

   a. Install Anthropic:
      ```
      pip install anthropic
      ```

   b. Install Tkinter:
      - On most Python installations, Tkinter comes pre-installed. If it's not available, you can install it as follows:
        
        For Ubuntu/Debian:
        ```
        sudo apt-get install python3-tk
        ```
        
        For Fedora:
        ```
        sudo dnf install python3-tkinter
        ```
        
        For macOS (using Homebrew):
        ```
        brew install python-tk
        ```
        
        For Windows:
        Tkinter is typically included with Python installations on Windows. If it's missing, consider reinstalling Python and make sure to check the option to install Tkinter during the installation process.

   Alternatively, if you prefer to use the requirements file:
   ```
   pip install -r requirements.txt
   ```

### Usage

1. Run the application:
   ```
   python csv_generator.py
   ```

2. The GUI will open. Follow these steps:
   - Enter your Anthropic API key and click "Save API Key".
   - Click "Browse" to select your input CSV file.
   - Enter the number of rows you want to generate.
   - Click "Generate CSV".

3. The generated CSV will be saved in the same directory as your input file.

## Using the Docker Image

### Prerequisites

- Docker installed on your system

### Pulling the Docker Image

Pull the Docker image from Docker Hub:

```
docker pull wasimirl/claude-data-creator:latest
```

### Usage

1. Create a directory on your local machine to store your CSV files:
   ```
   mkdir csv_data
   ```

2. Run the Docker container:
   ```
   docker run -it --rm -v "/path/to/your/csv_data:/app/data" wasimirl/claude-data-creator:latest
   ```
   Replace `/path/to/your/csv_data` with the actual path to the directory you created.

3. Follow the interactive prompts:
   - Enter your Anthropic API key when prompted.
   - When asked for the file path, enter `/app/data/your_input_file.csv`, replacing `your_input_file.csv` with your actual input file name.
   - Enter the number of rows you want to generate.

4. The generated CSV will be saved in the same directory as your input file.

## Configuration

- The application saves your API key and last used settings in a `config.json` file.
- To clear saved data, use the "Clear Saved Data" button in the GUI or delete the `config.json` file.

## Troubleshooting

- If you encounter file path issues in Docker, ensure you're using the correct path format: `/app/data/your_file.csv`.
- For GUI issues, ensure you have tkinter installed (`sudo apt-get install python3-tk` on Linux).
- If you face any other issues, please check the `csv_generator.log` file for error messages.

For more information or to report issues, please visit the [GitHub repository](https://github.com/wasim-bhatti/claude-data-creator).