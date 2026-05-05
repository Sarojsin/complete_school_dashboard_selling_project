import subprocess, time, sys, threading, os

# Start uvicorn server
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=r"C:\Users\U S E R\Desktop\claud_sc",
    bufsize=1,
)

# Read output for a few seconds
output = []
def reader():
    for line in proc.stdout:
        output.append(line)
        if 'ERROR' in line or 'Traceback' in line:
            print(line, end='')
t = threading.Thread(target=reader, daemon=True)
t.start()
time.sleep(8)
proc.terminate()
proc.wait()

# Write full log
with open('test_run_log.txt', 'w', encoding='utf-8') as f:
    f.writelines(output)
print(f"Captured {len(output)} lines, see test_run_log.txt")
