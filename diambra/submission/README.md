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
from diambra.arena import SpaceTypes
from diambra.arena.stable_baselines3.make_sb3_env import EnvironmentSettings, WrappersSettings
from stable_baselines3 import PPO
import diambra

if __name__ == "__main__":


    # Settings
    settings = EnvironmentSettings()
    settings.difficulty = 8
    settings.characters = "Ken"
    settings.action_space = SpaceTypes.MULTI_DISCRETE
    ...

    # Wrappers Settings
    wrappers_settings = WrappersSettings()
    wrappers_settings.frame_shape = (84, 84, 1)
    wrappers_settings.stack_frames = 4
    ...



    # Create environment
    env = diambra.arena.make(settings.game_id, settings, wrappers_settings)

    model_path = "./model.zip"

    # Load agent
    agent = PPO.load(model_path, env)

    # Begin evaluation
    observation, info = env.reset()
    while True:
        action, _ = agent.predict(observation, deterministic=True)
        observation, reward, terminated, truncated, info = env.step(action.tolist())

        if terminated or truncated:
            observation, info = env.reset()
            if info["env_done"] is True:
                break

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

