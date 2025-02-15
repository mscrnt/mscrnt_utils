# DIAMBRA Arena Submission Agent

This repository contains the necessary files for submitting your DIAMBRA Arena agent. It includes:

- **agent.py**: Loads your pre-trained PPO agent and runs it in the DIAMBRA Arena environment.
- **Dockerfile**: Builds a Docker container for your agent.
- **requirements.txt**: Lists the Python dependencies.
- **filter_keys.py**: Provides helper functions for generating game-specific observation keys.

---

## Submission Instructions

Follow these steps to submit your agent using the DIAMBRA CLI:

### 1. Customize the `agent.py` Script

Replace the sample logic in `agent.py` with your own pre-trained agent logic. Below is an example structure:

```python
import diambra.arena
from stable_baselines3 import PPO  # Import your RL framework

# Model path and game ID
MODEL_PATH = "./model.zip"
GAME_ID = "doapp"

# Load the trained agent
agent = PPO.load(MODEL_PATH)

# Environment settings setup and environment creation
env = diambra.arena.make(GAME_ID)

# Agent-Environment loop
obs, info = env.reset()
while True:
    # Predict the next action using the trained agent
    action, _ = agent.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action.tolist())

    if terminated or truncated:
        obs, info = env.reset()
        if info["env_done"]:
            break

# Close the environment
env.close()
```

Modify the settings (such as `GAME_ID` and `MODEL_PATH`) and the logic as required for your agent.

---

### 2. Update the Dockerfile and `requirements.txt` (If Necessary)

If your agent requires additional dependencies or custom setups, update the following files:

- **requirements.txt**: Add any extra Python packages your agent depends on. For example:

  ```txt
  diambra-arena
  stable_baselines3
  diambra
  ```

- **Dockerfile**: Ensure the Dockerfile installs all required dependencies. For example:

  ```dockerfile
  FROM ghcr.io/diambra/arena-base-on3.10-bullseye:main

  RUN apt-get -qy update && \
      apt-get -qy install libgl1 && \
      rm -rf /var/lib/apt/lists/*

  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt

  COPY . .
  ENTRYPOINT [ "python", "/app/agent.py" ]
  ```

---

### 3. Submit Your Agent

Submit your agent directly from the directory where your files are located. The DIAMBRA CLI will build and push your agent to DIAMBRA’s registry automatically.

```bash
diambra agent submit .
```

To set the submission difficulty (e.g., Hard), use:

```bash
diambra agent --submission.difficulty Hard submit .
```

---

## Tracking Your Submission

After submission, you'll receive a link to monitor your agent's evaluation progress and results. The CLI output might look like:

```
🖥️  logged in
...
🖥️  (####) Agent submitted: https://diambra.ai/submission/####
```

Visit the provided link to review your agent’s progress.

