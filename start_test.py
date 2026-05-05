import subprocess, time, sys, threading

output = []
def read_output(pipe):
    for line in iter(pipe.readline, ''):
        output.append(line)
        if 'error' in line.lower() or 'traceback' in line.lower():
            print(line, end='')
    pipe.close()

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001", "--log-level", "warning"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=r"C:\Users\U S E R\Desktop\claud_sc",
    bufsize=1,
)

t = threading.Thread(target=read_output, args=(proc.stdout,), daemon=True)
t.start()
time.sleep(8)
proc.terminate()
proc.wait()

# Check for errors
errors = [line for line in output if 'error' in line.lower() or 'traceback' in line.lower() or 'importerror' in line.lower()]
if errors:
    print("ERRORS FOUND:")
    for e in errors:
        print(e)
else:
    print("Server started cleanly, no errors or missing imports.")
print(f"Total startup lines captured: {len(output)}")
