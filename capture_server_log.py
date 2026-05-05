import subprocess, time, sys, threading, queue, sys

# Start uvicorn as a subprocess
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=r"C:\Users\U S E R\Desktop\claud_sc",
    bufsize=1,
)

# Read for a few seconds
output = []
def reader():
    for line in proc.stdout:
        output.append(line)
        if len(output) % 50 == 0:
            print(f"Read {len(output)} lines...")
t = threading.Thread(target=reader, daemon=True)
t.start()
time.sleep(10)
proc.terminate()
proc.wait()

# Write full output for reference
with open('server_startup_log.txt', 'w', encoding='utf-8') as f:
    f.writelines(output)

# Filter for SAWarnings/overlapping
print("\n=== SAWarnings/overlapping related lines ===")
for line in output:
    if 'SAWarning' in line or 'overlapping' in line.lower() or ('warning' in line.lower() and ('mapper' in line.lower() or 'relationship' in line.lower())):
        print(line.strip())
