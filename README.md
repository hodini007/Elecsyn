🤖 AI Multisim Automation Agent
This project automates the process of circuit design and simulation by combining the intelligence of the Gemini 2.5 Pro model with Windows Desktop Automation (using pywinauto).

The script accepts a natural language description of a circuit (the "prelab sheet") and automatically generates the necessary SPICE netlist (.cir file), launches NI Multisim, and runs the simulation.

🛠️ Requirements & Setup
You must have the following software installed and configured:

1. Software Requirements
Python 3.x: (Used to run the script.)

NI Multisim: (Installed on your Windows PC.)

Windows Operating System: (Desktop automation is Windows-specific.)

2. Environment Setup
A. Install Python Libraries
Open your terminal (or VS Code terminal, with your virtual environment activated) and run:

pip install google-genai pywinauto python-dotenv

B. Set Your API Key (Crucial)
The script requires secure access to the Gemini API. Create a file named .env in the same directory as multisim_agent.py and add your API key:

GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

C. Configure Script Paths
Open multisim_agent.py and ensure the following line reflects the exact path to your Multisim executable:

# In multisim_agent.py, update this line:
MULTISIM_EXE = r"C:\Program Files (x86)\National Instruments\Circuit Design Suite 14.3\multisim.exe"

🚀 How to Run the Agent
Run the Script:
Open your terminal in the project directory and execute the file:

python multisim_agent.py

Enter Prompt:
The script will immediately pause and prompt you:

Enter your circuit design prompt: 

Type your full circuit description here.

Example Prompt:
Design a passive RC low-pass filter with a 5 kHz cutoff. Use a 1V AC source and run an AC Sweep analysis from 100 Hz to 1 MHz.

Automation Sequence:
The script will execute the following steps automatically:

Netlist Generation: Calls Gemini 2.5 Pro to create the SPICE netlist.

File Save: Saves the output to ai_generated_circuit.cir.

Launch Multisim: Uses the command line to launch Multisim and simultaneously load the generated .cir file.

Simulation: Uses pywinauto to connect to the Multisim window and press the {F5} key to start the simulation.

💡 Troubleshooting & Notes
Inaccurate Results: If the simulation results are incorrect, the issue is likely with the AI's interpretation of the circuit. Modify your input prompt to be more explicit about required SPICE directives (e.g., "Use a 1N4148 diode model," or "Run a Transient Analysis for 10ms"). The Gemini 2.5 Pro model is chosen to minimize these errors.

Multisim Fails to Launch: If you see a timeout error before the script connects, verify the MULTISIM_EXE path is correct. If the path is correct, your Windows installation may require a longer time.sleep() delay (currently 10 seconds) after the subprocess.Popen call to ensure Multisim is fully initialized.

503 UNAVAILABLE Error: This is a temporary server overload error. The script is programmed with exponential backoff and will automatically retry the AI call up to four times.
