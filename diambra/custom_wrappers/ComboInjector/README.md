# ComboInjector - Custom Wrapper for DIAMBRA Arena

## Overview

The **ComboInjector** module is a custom **Gymnasium** wrapper designed for **DIAMBRA Arena** environments. It enables **automated combo injection** for fighting game agents, allowing them to execute **predefined special moves and super arts** as part of their reinforcement learning training.

This project is a **fork and extension** of [Nebraskinator/ComboInjector](https://github.com/Nebraskinator/ComboInjector), modified to integrate seamlessly with **Stable-Baselines3 PPO** and DIAMBRA's environment handling.

### Module Components

The module consists of the following files:

- `ComboInjector/__init__.py` - Initializes the module and defines base movement/attack mappings.
- `ComboInjector/action_utils.py` - Contains utilities for parsing and processing action strings.
- `ComboInjector/combo_injector.py` - Implements the **ComboInjector** class, which injects combo actions into the environment.
- `ComboInjector/combo_wrapper.py` - Implements **ComboWrapper**, a Gymnasium wrapper that integrates ComboInjector into an environment.

---

## Features

✔ **Automated combo execution** - Allows agents to execute **predefined character-specific combos**.  
✔ **Configurable action modes** - Supports **multi_discrete** action spaces.  
✔ **Decay Mechanism** - Injection probability can **decay over time**, simulating skill progression.  
✔ **Custom environment support** - Works with **DIAMBRA Arena** environments.  
✔ **Seamless RL training integration** - Easily integrates with **Stable-Baselines3 PPO** training.  

---

## Installation

### Clone the Entire Repository

```bash
git clone https://github.com/your-repo/diambra-combo-injector.git
cd diambra-combo-injector
pip install -r requirements.txt
```

### OR: Clone Only the `ComboInjector` Folder (Sparse Checkout)

If you only need the `ComboInjector` module and not the entire repository:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/your-repo/diambra-combo-injector.git
cd diambra-combo-injector
git sparse-checkout set ComboInjector
cd ComboInjector
```

---

## Usage

### 1️⃣ Wrapping an Environment with `ComboWrapper`

To use **ComboWrapper**, simply wrap your environment:

```python
from diambra.arena import make_sb3_env, EnvironmentSettings, WrappersSettings
from ComboInjector.combo_wrapper import ComboWrapper

# Define environment settings
env_settings = EnvironmentSettings(game_id="sfiii3n", characters=["Ken"], super_art=[2])
wrappers_settings = WrappersSettings()

# Define ComboInjector settings
injector_kwargs = {
    "environment_name": env_settings.game_id,
    "frame_skip": 4,
    "mode": "multi_discrete",
    "total_decay_steps": 32000000,  # Set to 0 to disable decay
}

# Add ComboWrapper to the environment
wrappers_settings.wrappers.append([
    ComboWrapper, {"injector_kwargs": injector_kwargs, "characters": ["Ken"], "super_arts": [2]}
])

# Create the wrapped environment
env, num_envs = make_sb3_env(env_settings.game_id, env_settings, wrappers_settings)
print(f"Activated {num_envs} environment(s)")
```

---

### 3️⃣ Disabling Decay

By default, **combo injection probability decays over time**. To disable this feature and ensure that **combos are always injected**, set `total_decay_steps=0` when initializing the **ComboInjector**:

```python
injector_kwargs = {
    "environment_name": "sfiii3n",
    "frame_skip": 4,
    "mode": "multi_discrete",
    "total_decay_steps": 0,  # No decay, combos always active
}
```

---

## File Structure

```
ComboInjector/
├── __init__.py         # Base mappings and module initialization
├── action_utils.py     # Action processing utilities
├── combo_injector.py   # Core combo injection logic
└── combo_wrapper.py    # Gymnasium wrapper
```

---

## Configuration Options

### `ComboInjector` Parameters

| Parameter           | Type  | Default            | Description                                                                      |
| ------------------- | ----- | ------------------ | -------------------------------------------------------------------------------- |
| `environment_name`  | `str` | `'sfiii3n'`        | Environment ID                                                                   |
| `mode`              | `str` | `'multi_discrete'` | Action mode                                                                      |
| `frame_skip`        | `int` | `4`                | Frame skipping for hold/charge moves                                             |
| `total_decay_steps` | `int` | `16000000`         | Steps over which injection probability decays to 0. Set to `0` to disable decay. |

---

## License

This project is licensed under the **MIT License**.

---

## Acknowledgments

This project was **forked from** [Nebraskinator/ComboInjector](https://github.com/Nebraskinator/ComboInjector) and customized for DIAMBRA Arena.

- **DIAMBRA Arena** - For providing a flexible RL framework for fighting games.  
  - Documentation: [https://docs.diambra.ai/](https://docs.diambra.ai/)  
  - GitHub: [https://github.com/diambra/](https://github.com/diambra/)  
  - Website: [https://diambra.ai/](https://diambra.ai/)  
- **Stable-Baselines3** - For robust RL implementations.
- **Gymnasium** - For providing standardized RL environments.
---

## Contact

For questions, issues, or contributions, please open an **issue** or submit a **pull request** on GitHub.