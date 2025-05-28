import subprocess
import sys

# Start all processes
main_process = subprocess.Popen([sys.executable, "main.py"])
agent1_process = subprocess.Popen([sys.executable, "dummy_agents/stupid_agent.py"])
agent2_process = subprocess.Popen([sys.executable, "dummy_agents/spinning_agent.py"])
agent3_process = subprocess.Popen([sys.executable, "dummy_agents/rotating_agent.py"])


try:
    main_process.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    main_process.terminate()
    agent1_process.terminate()
    agent2_process.terminate()
    agent3_process.terminate()