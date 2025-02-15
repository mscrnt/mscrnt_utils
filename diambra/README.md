# DIAMBRA Utilities

Welcome to the DIAMBRA utilities package—a collection of tools and modules designed to support DIAMBRA Arena workflows. This folder contains several modules for different purposes, including training, submission, monitoring, and custom wrappers.

## Folder Structure

```
mscrnt_utils/
└── diambra/
    ├── custom_wrappers/   # Custom Gymnasium wrappers (e.g., ComboInjector) for DIAMBRA Arena
    ├── monitoring/        # Docker container log monitor for DIAMBRA training environments
    ├── submission/        # Submission agent package for DIAMBRA Arena
    └── training/          # Training module using PPO from Stable-Baselines3
```

---

## Modules Overview

### 1. Custom Wrappers (ComboInjector)

**Overview:**  
The ComboInjector module is a custom Gymnasium wrapper designed for DIAMBRA Arena. It enables automated combo injection, allowing agents to execute predefined combos and super arts during training.

**Key Files:**
- `ComboInjector/__init__.py`: Initializes the module and defines base mappings.
- `action_utils.py`: Utilities for parsing and processing action strings.
- `combo_injector.py`: Core combo injection logic.
- `combo_wrapper.py`: Gymnasium wrapper that integrates ComboInjector into the environment.

**Features:**
- Automated combo execution with configurable action modes.
- Decay mechanism to simulate skill progression.
- Easy integration with Stable-Baselines3 PPO and DIAMBRA Arena.

**Installation & Usage:**

1. Navigate to the ComboInjector folder:
   ```bash
   cd custom_wrappers/ComboInjector
   pip install -r requirements.txt
   ```
2. Wrap your environment:
   ```python
   from diambra.arena import make_sb3_env, EnvironmentSettings, WrappersSettings
   from ComboInjector.combo_wrapper import ComboWrapper

   env_settings = EnvironmentSettings(game_id="sfiii3n", characters=["Ken"], super_art=[2])
   wrappers_settings = WrappersSettings()

   injector_kwargs = {
       "environment_name": env_settings.game_id,
       "frame_skip": 4,
       "mode": "multi_discrete",
       "total_decay_steps": 32000000,
   }

   wrappers_settings.wrappers.append([ComboWrapper, {"injector_kwargs": injector_kwargs, "characters": ["Ken"], "super_arts": [2]}])
   env, num_envs = make_sb3_env(env_settings.game_id, env_settings, wrappers_settings)
   print(f"Activated {num_envs} environment(s)")
   ```

---

### 2. Monitoring

**Overview:**  
The Docker Container Log Monitor script tracks Docker container logs in real-time for DIAMBRA Arena training environments. It detects stage progressions and game completion logs, providing color-coded output and file logging.

**Key Files:**
- `monitor.py`: Main monitoring script.
- `requirements.txt`: Lists dependencies for monitoring.

**Features:**
- Real-time log monitoring.
- Filters logs based on a specified minimum stage.
- Automatic log rotation and threaded execution for concurrent monitoring.

**Installation & Usage:**

1. Navigate to the monitoring folder:
   ```bash
   cd monitoring
   pip install -r requirements.txt
   ```
2. Run the monitor:
   ```bash
   python monitor.py -m 3
   ```
   (This example starts monitoring logs from stage 3 onward.)

---

### 3. Submission

**Overview:**  
The Submission Agent package contains all files necessary to deploy your DIAMBRA Arena agent. It is designed to load a pre-trained PPO agent and run it in the DIAMBRA environment.

**Key Files:**
- `agent.py`: Loads your pre-trained agent and runs an evaluation loop.
- `Dockerfile`: Defines the container image for your agent.
- `requirements.txt`: Lists the Python dependencies.
- `filter_keys.py`: Generates game-specific observation keys.

**Submission Instructions:**

1. **Customize `agent.py`:**  
   Modify the script to point to your trained model (update `MODEL_PATH` and `GAME_ID`).

   ```python
   import diambra.arena
   from stable_baselines3 import PPO

   MODEL_PATH = "./model.zip"
   GAME_ID = "doapp"

   agent = PPO.load(MODEL_PATH)
   env = diambra.arena.make(GAME_ID)

   obs, info = env.reset()
   while True:
       action, _ = agent.predict(obs, deterministic=True)
       obs, reward, terminated, truncated, info = env.step(action.tolist())
       if terminated or truncated:
           obs, info = env.reset()
           if info["env_done"]:
               break

   env.close()
   ```

2. **Update Dependencies:**  
   Edit `requirements.txt` and the `Dockerfile` as needed if you require additional packages.

3. **Submit Your Agent:**  
   Use the DIAMBRA CLI from the submission directory:
   ```bash
   diambra agent submit .
   ```
   To set the submission difficulty (e.g., Hard):
   ```bash
   diambra agent --submission.difficulty Hard submit .
   ```

---

### 4. Training

**Overview:**  
The Training module uses PPO from Stable-Baselines3 to train DIAMBRA Arena agents. It includes all scripts and configuration files required to set up your training environment.

**Key Files:**
- `train.py`: Main training script.
- `eval.py`: Evaluation script to test a trained agent.
- `config.py`: Configuration for environment settings, game settings, wrappers, and PPO hyperparameters.
- `filter_keys.py`: Provides game-specific observation keys.

**Features:**
- Customizable training parameters (parallel environments, steps, autosave, etc.).
- Automatic checkpointing and Tensorboard logging.
- Integration with DIAMBRA Arena’s environment and wrappers.

**Installation & Usage:**

1. Navigate to the training folder:
   ```bash
   cd training
   pip install -r requirements.txt
   ```
2. To train your agent:
   ```bash
   python train.py
   ```
3. For evaluation:
   ```bash
   python eval.py
   ```

---

## Usage Across Modules

Each module can be used independently or as part of your DIAMBRA Arena workflow. For example, you can run the monitoring tool while training, or integrate the custom wrapper into your training setup.

---

## Contributing

Feel free to open issues or submit pull requests for enhancements or bug fixes.

---
