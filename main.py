import subprocess
import time
import os
from modules import gemini as ai

def install_dependency_task(dependency_name):
    # Generate install command using GPT
    prompt = (
        f"Write Python code that installs the dependency '{dependency_name}' using pip. "
        "The code should run the pip install command, catch any errors, and write 'success' or the error message to 'dependency_status.txt'. "
        "Do not include any explanations or formatting, only the code."
    )
    generated_code = ai.gpt_curl(prompt)

    # Save generated code to file
    with open("generated_code.py", "w", encoding="utf-8") as f:
        f.write(generated_code)

    # Remove previous status
    with open("dependency_status.txt", "w", encoding="utf-8") as f:
        f.write("pending")

    # Open new CMD and run the generated code
    subprocess.Popen('start cmd /c python generated_code.py', shell=True)

    # Wait for status update
    while True:
        try:
            with open("dependency_status.txt", "r", encoding="utf-8") as f:
                status = f.read().strip()
        except FileNotFoundError:
            status = "pending"
        if status != "pending":
            break
        time.sleep(1)

    if status == "success":
        print(f"Dependency '{dependency_name}' installed successfully.")
    else:
        print(f"Error installing '{dependency_name}': {status}")
        # Optionally, ask user what to do next or retry
        retry = input("Retry installation? (y/n): ")
        if retry.lower() == "y":
            install_dependency_task(dependency_name)
        else:
            print("Installation aborted.")

def run_generated_code(as_admin=False):
    with open("programm_running_status.txt", "w", encoding="utf-8") as f:
        f.write("running")

    if as_admin:
        # Create a batch file to run as administrator and keep window open
        with open("run_admin.bat", "w", encoding="utf-8") as f:
            f.write(
                'powershell -Command "Start-Process python -ArgumentList \"generated_code.py\" -Verb RunAs"\n'
                'pause\n'
            )
        subprocess.Popen('start cmd /c run_admin.bat', shell=True)
    else:
        subprocess.Popen('start cmd /c python generated_code.py', shell=True)

    while True:
        try:
            with open("programm_running_status.txt", "r", encoding="utf-8") as f:
                status = f.read().strip()
        except FileNotFoundError:
            status = "running"
        if status == "done":
            break
        time.sleep(1)

    try:
        with open("final_output.txt", "r", encoding="utf-8") as f:
            output = f.read()
    except FileNotFoundError:
        output = ""
    # user_message should be passed as an argument
    return output

# Example




def automate_task(user_message):
    # Ensure required files and directories exist
    import pathlib
    pathlib.Path("data").mkdir(exist_ok=True)
    for fname in ["generated_code.py", "algorithm.txt", "programm_running_status.txt", "final_output.txt", "dependency_status.txt", "install_dep.bat", "run_admin.bat"]:
        if not pathlib.Path(fname).exists():
            with open(fname, "w", encoding="utf-8") as f:
                f.write("")
    if user_message.strip().lower() == "exit":
        return None
    # ...existing code...
    print("Generating algorithm...")
    system_prompt = (
        "You are an expert Python developer and Windows automation specialist. "
        "Given the user's request, provide a clear, step-by-step algorithm in plain text for accomplishing the task in Python. "
        "Include any necessary dependency installations, error handling, and best practices for Windows environments. "
        "Do not write code, only the algorithm. Be concise and logical."
        "In from /modules/gemini.py  there gpt_curl(input text, system instruction) in some cases where the something from analysis or ai required use this function to call ai like to get data or anything"
        "you have complete right to create new python files and work in those for running and for it you can use ai"
        "print everystep you are doing"
    )

    response = ai.gpt_curl(user_message, system_prompt)

    with open("algorithm.txt", "w", encoding="utf-8") as f:
        f.write(response)

    print("Generating code from algorithm...")
    with open("algorithm.txt", "r", encoding="utf-8") as f:
        algorithm = f.read()

    code_prompt = (
        "Write Python code that implements the following algorithm for Windows. "
        "If any dependency is required, write the pip install command as a string variable named 'dependency_command'. "
        "At the end, write the main output/result to a file named 'final_output.txt'. "
        "After finishing all tasks, write 'done' to 'programm_running_status.txt'. "
        "Do not include any explanations, markdown formatting, or extra text—just the code."
        "If anything as an argument required ask to user for it else use default values and if something really not require to user then take decisions on yours do not give user confusions to enter take more decisions not from input."
        "In from /modules/gemini.py  there gpt_curl(input text, system instruction) in some cases where the something from analysis or ai required use this function to call ai like to get data or anything"
        "you have complete right to create new python files and work in those for running and for it you can use ai"
        "Algorithm:\n" + algorithm
    )

    generated_code = ai.gpt_curl(user_message, code_prompt)

    with open("generated_code.py", "w", encoding="utf-8") as f:
        f.write(generated_code)

    print("Checking for dependencies...")
    dependency_command = None
    with open("generated_code.py", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("dependency_command"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    dependency_command = parts[1].strip().strip('"').strip("'")

    if dependency_command:
        print("Dependency detected. Installing...")
        with open("dependency_status.txt", "w", encoding="utf-8") as f:
            f.write("pending")

        install_script = f"""
@echo off
echo Installing dependency: {dependency_command}
{dependency_command}
if %errorlevel%==0 (
    echo success > dependency_status.txt
) else (
    echo error > dependency_status.txt
)
exit
"""
        with open("install_dep.bat", "w", encoding="utf-8") as f:
            f.write(install_script)

        subprocess.Popen('start cmd /c install_dep.bat', shell=True)

        print("Waiting for dependency installation to complete...")
        while True:
            try:
                with open("dependency_status.txt", "r", encoding="utf-8") as f:
                    status = f.read().strip()
            except FileNotFoundError:
                status = "pending"
            if status != "pending":
                break
            time.sleep(1)

        if status == "success":
            print("Dependencies installed. Running generated code...")
            # Detect if admin is required from the algorithm or generated code
            admin_required = False
            try:
                with open("algorithm.txt", "r", encoding="utf-8") as f:
                    alg_text = f.read().lower()
                    if "administrator" in alg_text or "admin privileges" in alg_text or "run as admin" in alg_text:
                        admin_required = True
            except FileNotFoundError:
                admin_required = False

            run_generated_code(as_admin=admin_required)
        else:
            print(f"Error installing dependency: {status}")
            # Retry installation or abort
            retry = input("Retry installation? (y/n): ")
            if retry.lower() == "y":
                # Fix: Pass dependency name, not command
                install_dependency_task(dependency_command.split()[-1])
            else:
                print("Installation aborted.")
    else:
        print("No dependencies required. Running generated code...")
        # Detect if admin is required from the algorithm or generated code
        admin_required = False
        try:
            with open("algorithm.txt", "r", encoding="utf-8") as f:
                alg_text = f.read().lower()
                if "administrator" in alg_text or "admin privileges" in alg_text or "run as admin" in alg_text:
                    admin_required = True
        except FileNotFoundError:
            admin_required = False

        run_generated_code(as_admin=admin_required)
    print("Task completed.\nResponse: \n")

    # Return the output from final_output.txt
    try:
        with open("final_output.txt", "r", encoding="utf-8") as f:
            output = f.read()
    except FileNotFoundError:
        output = ""
    return output