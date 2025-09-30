import os
import time
import subprocess
import sys
from google import genai 
from pywinauto.application import Application
from pywinauto import timings
from dotenv import load_dotenv

load_dotenv() 

MULTISIM_EXE = r"C:\Program Files (x86)\National Instruments\Circuit Design Suite 14.3\multisim.exe"

NETLIST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_generated_circuit.cir")

MULTISIM_WINDOW_TITLE = "Multisim" 


def generate_netlist_with_gemini(prelab_description: str, filename: str):
    """
    Connects to the Gemini 2.5 Pro API to generate the SPICE netlist,
    including robust analysis commands for accurate simulation.
    """
    print("\n--- 1. Starting AI Netlist Generation ---")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY environment variable not set. Please check your .env file.")
        return None
        
    system_prompt = (
        "You are an expert circuit engineer specializing in SPICE netlist generation. "
        "Your output must be the raw, executable SPICE Netlist (.cir format) only. "
        "CRITICAL: Always include all necessary analysis commands (.AC, .TRAN, .OP) "
        "and correct component model definitions for the circuit requested. "
        "Use standard SPICE conventions and '.END' as the final line. "
        "DO NOT include any explanation or markdown code fences (```)."
    )

    client = genai.Client(api_key=api_key)
    max_retries = 4
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-pro',
                contents=prelab_description,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                ),
            )
            
            netlist_content = response.text.strip()
            
            if not netlist_content:
                raise ValueError("AI returned an empty netlist.")

            # Save to .cir file
            with open(filename, 'w') as f:
                f.write(netlist_content)

            print(f"✅ Netlist saved successfully to: {os.path.abspath(filename)}")
            return os.path.abspath(filename)

        except Exception as e:
            if "503 UNAVAILABLE" in str(e) and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"⚠️ Server overload (503). Retrying in {wait_time} seconds (Attempt {attempt + 2}/{max_retries}).")
                time.sleep(wait_time)
            else:
                print(f"❌ ERROR in AI Generation: {e}")
                return None
    return None


def automate_multisim_import_and_run(netlist_path: str, multisim_exe_path: str, window_title: str):
    """
    Uses the direct command line launch to open the .cir file automatically,
    then uses pywinauto to connect and run the simulation.
    """
    print(f"\n--- 2. Starting Multisim Direct Launch & Automation ---")
    
    timings.Timings.window_find_timeout = 20  

    try:
        subprocess.Popen(f'"{multisim_exe_path}" "{netlist_path}"', shell=True)
        print("✅ Launched Multisim and passed netlist file path.")
        time.sleep(10)     

        app = Application(backend="uia").connect(path=multisim_exe_path, timeout=15)
        
        main_window = app.window(title_re=f".*{window_title}.*")
        main_window.wait('visible ready', timeout=10)
        print(f"Connected to main window: {main_window.texts()[0]}")

        main_window.set_focus()
        main_window.type_keys('{F5}') 
        print("✅ F5 key sent. Simulation should now be running.")

    except Exception as e:
        print(f"❌ Multisim Automation Failed: {e}")
        print("\n*** TROUBLESHOOTING TIP ***")
        print("If the script failed, ensure Multisim is installed correctly and the executable path is accurate.")
        print("Also check for any lingering startup dialogs that might be blocking the main window.")


if __name__ == "__main__":
    
    print("------------------------------------------------------------------")
    print("🟢 AI Multisim Agent Ready")
    print("------------------------------------------------------------------")
    
    user_prompt = input("Enter your circuit design prompt: ")
    
    if not user_prompt.strip():
        print("Operation cancelled: No prompt entered.")
        sys.exit(0)
    
    netlist_full_path = generate_netlist_with_gemini(user_prompt, NETLIST_FILE)
    
    if netlist_full_path:
        automate_multisim_import_and_run(netlist_full_path, MULTISIM_EXE, MULTISIM_WINDOW_TITLE)
        
    print("\n--- Automation Process Finished ---")