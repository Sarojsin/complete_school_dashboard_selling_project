import subprocess, time, sys, threading, queue

# Start uvicorn
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=r"C:\Users\U S E R\Desktop\claud_sc",
    bufsize=1,
)

# Read output in background thread to avoid deadlock
output_lines = []
def reader():
    for line in proc.stdout:
        output_lines.append(line)
        print(line, end='')  # also echo

t = threading.Thread(target=reader, daemon=True)
t.start()

# Wait for 8 seconds
time.sleep(8)

# Terminate
proc.terminate()
proc.wait()

# Filter warnings
print("\n=== Filtered SAWarnings ===")
for line in output_lines:
    if "SAWarning" in line or "overlapping" in line.lower() or "Mapper" in line:
        print(line.strip())
