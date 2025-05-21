import subprocess
import time


# Command 2 & 3: Start agents and game in parallel
cmd1 = ["python3", "main.py"]
p1 = subprocess.Popen(cmd1)
time.sleep(2)
cmd2 = ["python3", "dummy_agents/stupid_agent.py"]
cmd3 = ["python3", "dummy_agents/spinning_agent.py"]

p2 = subprocess.Popen(cmd2)
p3 = subprocess.Popen(cmd3)

# Optional: Wait for all to complete (CTRL+C will interrupt)
try:
    p1.wait()
    p2.wait()
    p3.wait()
except KeyboardInterrupt:
    print("\nStopping all processes...")
    for p in [p1, p2, p3]:
        p.terminate()

