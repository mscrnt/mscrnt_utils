import os
from filter_keys import get_filter_keys
from diambra.arena import SpaceTypes

# ✅ Environment Settings
env_settings = {
    "env_num": 32,  # Number of parallel environments
    "check_freq": 100000,  # Autosave frequency
    "time_steps": 32000000,  # Total training steps
}

# ✅ Game Settings
settings = {
    "game_id": "sfiii3n",
    "difficulty": 8,
    "characters": "Ken",
    "action_space": SpaceTypes.MULTI_DISCRETE,
    "step_ratio": 1,
    "frame_shape": (84, 84, 1),
    "super_art": 3,
}

# ✅ Extract game_id
game_id = settings["game_id"]

# ✅ Wrappers Settings
flatten = True
wrappers_settings = {
    "wrappers": [],  # Custom wrappers (e.g., InjectComboWrapper) will be added in train.py
    "stack_frames": 4,
    "dilation": 1,
    "no_attack_buttons_combinations": False,
    "normalize_reward": False,
    "normalization_factor": 1.0,
    "stack_actions": 4,
    "scale": True,
    "exclude_image_scaling": True,
    "flatten": flatten,
    "process_discrete_binary": True,
    "role_relative": True,
    "add_last_action": True,
    "filter_keys": get_filter_keys(game_id, flatten),
}

# ✅ PPO Training Settings
n_steps = 128  # Steps per rollout
n_envs = env_settings["env_num"]  # Parallel environments
nminibatches = 8  # Number of mini-batches (adjustable)

# ✅ Dynamically calculated batch size
batch_size = (n_steps * n_envs) // nminibatches
if (n_steps * n_envs) % nminibatches != 0:
    raise ValueError("Batch size must be evenly divisible! Adjust `nminibatches` or `n_steps`.")

policy_kwargs = {"net_arch": {"pi": [128, 128], "vf": [64, 64]}}

ppo_settings = {
    "gamma": 0.94,
    "n_epochs": 4,
    "n_steps": n_steps,
    "batch_size": batch_size,  # ✅ Dynamic batch size
    "learning_rate_start": 5.0e-5,
    "learning_rate_end": 2.5e-6,
    "clip_range_start": 0.075,
    "clip_range_end": 0.025,
    "seed": 42,
    "policy_kwargs": policy_kwargs,
}

# ✅ Model Save Paths
model_path = "./trained_models"
tensorboard_log_path = "./tensorboard_logs"
monitor_logs_path = "./output/logs"

# ✅ Ensure paths exist
os.makedirs(model_path, exist_ok=True)
os.makedirs(tensorboard_log_path, exist_ok=True)
os.makedirs(monitor_logs_path, exist_ok=True)
