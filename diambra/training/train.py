import os
import glob
import torch
import config
import argparse
from diambra.arena import load_settings_flat_dict
from diambra.arena.stable_baselines3.make_sb3_env import make_sb3_env, EnvironmentSettings, WrappersSettings
from diambra.arena.stable_baselines3.sb3_utils import linear_schedule, AutoSave
from stable_baselines3 import PPO

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Train PPO agent for DIAMBRA Arena."
    )
    return parser.parse_args()

def main():
    args = parse_args()

    # Load environment and wrapper settings from config
    env_settings = load_settings_flat_dict(EnvironmentSettings, config.settings)
    wrappers_settings = load_settings_flat_dict(WrappersSettings, config.wrappers_settings)

    total_steps = config.env_settings["time_steps"]

    # Create the environment with the modified settings.
    env, num_envs = make_sb3_env(env_settings.game_id, env_settings, wrappers_settings)
    print(f"Activated {num_envs} environment(s)")

    # Check for existing checkpoints.
    checkpoint_files = glob.glob(os.path.join(config.model_path, "*.zip"))
    if checkpoint_files:
        latest_checkpoint = max(checkpoint_files, key=os.path.getmtime)
        print(f"Loading latest checkpoint: {latest_checkpoint}")

        completed_steps = int(latest_checkpoint.split("_")[-1].split(".")[0])
        remaining_steps = total_steps - completed_steps
        print(f"Resuming from {completed_steps} steps")

        learning_rate_schedule = linear_schedule(config.ppo_settings["learning_rate_start"],
                                                 config.ppo_settings["learning_rate_end"])
        clip_range_schedule = linear_schedule(config.ppo_settings["clip_range_start"],
                                              config.ppo_settings["clip_range_end"])

        agent = PPO.load(latest_checkpoint, env,
                         learning_rate=learning_rate_schedule,
                         clip_range=clip_range_schedule)
    else:
        print("No checkpoint found. Starting new training session.")

        agent = PPO("MultiInputPolicy", env, verbose=1,
                    gamma=config.ppo_settings["gamma"],
                    batch_size=config.ppo_settings["batch_size"],
                    n_epochs=config.ppo_settings["n_epochs"],
                    n_steps=config.ppo_settings["n_steps"],
                    learning_rate=linear_schedule(config.ppo_settings["learning_rate_start"],
                                                  config.ppo_settings["learning_rate_end"]),
                    clip_range=linear_schedule(config.ppo_settings["clip_range_start"],
                                               config.ppo_settings["clip_range_end"]),
                    policy_kwargs=config.ppo_settings["policy_kwargs"],
                    tensorboard_log=config.tensorboard_log_path,
                    seed=config.ppo_settings["seed"],
                    device="cuda" if torch.cuda.is_available() else "cpu")

    autosave_freq = config.env_settings["check_freq"]
    auto_save_callback = AutoSave(check_freq=autosave_freq, num_envs=num_envs, save_path=config.model_path)

    print("Starting Training...")
    try:
        agent.learn(total_timesteps=total_steps, callback=auto_save_callback)
        print("Training Completed!")
    except KeyboardInterrupt:
        print("Training interrupted. Saving model before exit.")

    agent.save(config.model_path)
    print(f"Model saved at {config.model_path}")

    env.close()
    print("Environment Closed.")

if __name__ == "__main__":
    main()
