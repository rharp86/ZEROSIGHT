import subprocess

def execute_tool(command, timeout=30):
    """
    Execute an external tool with a timeout and return its output and errors.
    """
    try:
        # Run the subprocess with a timeout
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(timeout=timeout)
        return stdout.strip(), stderr.strip()
    except subprocess.TimeoutExpired:
        process.kill()  # Ensure the process is terminated
        return "", f"ERROR: Command timed out after {timeout} seconds."
    except FileNotFoundError:
        return "", f"ERROR: Command not found: {' '.join(command)}"
    except Exception as e:
        return "", f"ERROR: {str(e)}"

