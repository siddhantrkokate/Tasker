# Tasker

An intelligent task automation tool that uses AI to generate and execute Python code based on user descriptions. Tasker leverages the Gemini API to understand user requests, create step-by-step algorithms, generate code, and handle Windows system-level tasks.

## Features

- AI-Powered Task Generation: Describe what you want to do, and Tasker generates Python code using Gemini AI
- Automatic Dependency Management: Detects required dependencies and installs them automatically
- Windows System Automation: Full support for Windows-specific operations and administrator privileges
- Error Handling: Robust error handling and retry mechanisms
- Asynchronous Execution: Runs tasks in separate processes with status monitoring
- Audio Support: Includes speech recognition and text-to-speech capabilities

## Requirements

- Python 3.7 or higher
- Windows OS (for full functionality)
- Gemini API key

## Installation

1. Clone the repository:
```
git clone https://github.com/siddhantrkokate/Tasker.git
cd Tasker
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up your Gemini API key in the modules/gemini.py configuration

## Dependencies

The project requires the following Python packages:

- sounddevice - Audio input/output
- numpy - Numerical computing
- SpeechRecognition - Speech recognition capabilities
- pyttsx3 - Text-to-speech synthesis
- pywin32 - Windows system integration
- requests - HTTP library

## Project Structure

```
Tasker/
├── main.py                 # Core automation engine
├── run.py                  # Entry point for running tasks
├── requirements.txt        # Python package dependencies
├── modules/
│   └── gemini.py          # Gemini API integration
└── data/                  # Data storage directory
```

## Usage

Run the task automation tool:

```
python run.py
```

Then describe the task you want to automate. Tasker will:

1. Generate a step-by-step algorithm for your task
2. Create Python code based on the algorithm
3. Check for required dependencies and install them if needed
4. Execute the generated code
5. Return the results

### Example Tasks

- File operations and management
- Data processing and analysis
- System maintenance tasks
- Windows automation scripts
- Installation and configuration management

## How It Works

### Task Processing Flow

1. **Algorithm Generation**: User input is sent to Gemini AI to create a detailed algorithm
2. **Code Generation**: The algorithm is converted into executable Python code
3. **Dependency Check**: The generated code is scanned for required packages
4. **Installation**: Missing dependencies are installed via pip
5. **Execution**: Code runs with appropriate privileges (standard or admin)
6. **Output Collection**: Results are captured and returned to the user

### Key Functions

- `automate_task(user_message)` - Main function to process and execute user requests
- `install_dependency_task(dependency_name)` - Handles dependency installation
- `run_generated_code(as_admin)` - Executes generated code with optional admin privileges

## Configuration

Ensure the Gemini API key is properly configured in `modules/gemini.py` for the AI features to work correctly.

## Notes

- The tool is designed for Windows environments
- Administrator privileges may be required for certain system-level operations
- All generated code and temporary files are stored in the project directory
- Review generated code before execution if possible

## License

This project is open source and available on GitHub.

## Author

Created by siddhantrkokate
