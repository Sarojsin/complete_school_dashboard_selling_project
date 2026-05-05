import subprocess, time, sys, signal

# Start uvicorn as a subprocess, capturing stdout and stderr
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=r"C:\Users\U S E R\Desktop\claud_sc"
)

# Wait for 5 seconds to let server start
time.sleep(5)

# Terminate
proc.terminate()
out, _ = proc.communicate()

# Filter for warnings
lines = out.splitlines()
warning_lines = [line for line in lines if "SAWarning" in line or "overlapping" in line.lower() or "Mapper" in line]
print("\n".join(warning_lines[:50]))  # print first 50 warning lines
