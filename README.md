# AI Multisim Automation Agent

An intelligent automation tool that generates SPICE netlists using Google's Gemini AI and automatically imports and runs them in NI Multisim.

## Overview

This Python script bridges the gap between natural language circuit descriptions and executable circuit simulations. Simply describe your circuit design in plain English, and the AI agent will:

1. Generate a proper SPICE netlist using Gemini 2.5 Pro
2. Launch NI Multisim with the generated circuit
3. Automatically run the simulation

## Features

- **AI-Powered Netlist Generation**: Leverages Google Gemini 2.5 Pro to create accurate SPICE netlists from text descriptions
- **Automatic Multisim Integration**: Seamlessly launches and controls Multisim
- **Robust Error Handling**: Includes retry logic for API calls and detailed error messages
- **Zero Manual Intervention**: From prompt to simulation with a single command

## Prerequisites

### Software Requirements

- **Python 3.7+**
- **NI Multisim 14.3** (Circuit Design Suite)
- **Windows OS** (required for pywinauto automation)

### Python Dependencies

```bash
pip install google-genai pywinauto python-dotenv
```

## Installation

1. **Clone or download this repository**

2. **Install required Python packages:**
   ```bash
   pip install google-genai pywinauto python-dotenv
   ```

3. **Set up your Gemini API key:**
   - Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a `.env` file in the project directory:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

4. **Verify Multisim installation path:**
   - Default path: `C:\Program Files (x86)\National Instruments\Circuit Design Suite 14.3\multisim.exe`
   - If your installation differs, update the `MULTISIM_EXE` variable in the script

## Usage

1. **Run the script:**
   ```bash
   python multisim_ai_agent.py
   ```

2. **Enter your circuit design prompt when prompted:**
   ```
   Enter your circuit design prompt: Design a simple RC low-pass filter with 1kHz cutoff frequency
   ```

3. **Wait for the automation to complete:**
   - The AI generates the netlist
   - Multisim launches automatically
   - The simulation runs (F5 is triggered)

## Example Prompts

- "Create a voltage divider circuit with two 10k resistors and a 12V source"
- "Design a simple RC low-pass filter with 1kHz cutoff frequency"
- "Build a BJT common emitter amplifier with proper biasing"
- "Create a full-wave bridge rectifier with smoothing capacitor"

## Configuration

### Customizable Variables

```python
MULTISIM_EXE = r"C:\Program Files (x86)\National Instruments\Circuit Design Suite 14.3\multisim.exe"
NETLIST_FILE = "ai_generated_circuit.cir"
MULTISIM_WINDOW_TITLE = "Multisim"
```

### Timeout Settings

Adjust these in the `automate_multisim_import_and_run()` function if needed:
- `window_find_timeout`: Time to wait for Multisim window (default: 20s)
- Initial launch delay: 10 seconds

## How It Works

### 1. AI Netlist Generation
The script connects to Google's Gemini 2.5 Pro API with a specialized system prompt that ensures:
- Pure SPICE netlist output (no markdown formatting)
- Proper analysis commands (.AC, .TRAN, .OP)
- Standard SPICE conventions
- Correct component models

### 2. Multisim Automation
Uses `pywinauto` to:
- Launch Multisim with the netlist file as a command-line argument
- Connect to the application window
- Send F5 keystroke to run the simulation

### 3. Error Handling
- Automatic retries for API 503 errors (with exponential backoff)
- Comprehensive error messages
- Empty response validation

## Troubleshooting

### Common Issues

**"GEMINI_API_KEY environment variable not set"**
- Ensure your `.env` file exists in the script directory
- Verify the API key is correct and has no extra spaces

**"Multisim Automation Failed"**
- Check that Multisim is properly installed
- Verify the executable path matches your installation
- Close any existing Multisim instances before running
- Disable startup dialogs in Multisim settings

**Simulation doesn't run automatically**
- The script waits 10 seconds after launch; increase this if your system is slow
- Ensure no dialog boxes are blocking the main window
- Check if F5 is the correct shortcut in your Multisim version

**API Connection Issues**
- Verify your internet connection
- Check if the Gemini API is experiencing downtime
- Ensure your API key has not expired

## Limitations

- Currently supports Windows only (due to pywinauto)
- Requires NI Multisim to be installed
- Netlist quality depends on AI interpretation
- Complex circuits may require manual refinement

## Security Notes

- Keep your `.env` file private and never commit it to version control
- Add `.env` to your `.gitignore` file
- Rotate your API keys periodically

## License

This project is provided as-is for educational and research purposes.

## Contributing

Suggestions and improvements are welcome! Consider:
- Support for other SPICE simulators
- Enhanced error detection
- Circuit validation before simulation
- Results extraction and analysis

## Acknowledgments

- Google Gemini AI for netlist generation
- NI Multisim for circuit simulation
- pywinauto for Windows automation

---

**Note**: This tool is designed to accelerate circuit prototyping and learning. Always verify AI-generated circuits before use in production environments.
