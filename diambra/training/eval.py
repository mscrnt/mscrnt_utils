from diambra.arena import SpaceTypes
from diambra.arena.stable_baselines3.make_sb3_env import EnvironmentSettings, WrappersSettings
from stable_baselines3 import PPO
import diambra
from filter_keys import get_filter_keys


if __name__ == "__main__":

    # ✅ Environment Settings
    settings = EnvironmentSettings()
    settings.difficulty = 8 # Hardest difficulty
    settings.characters = "" # "ken"
    settings.action_space = SpaceTypes.MULTI_DISCRETE
    settings.step_ratio = 1
    settings.super_art = 3
    settings.game_id = "" #sfiii3n                 

    # ✅ Wrappers Settings
    wrappers_settings = WrappersSettings()
    wrappers_settings.frame_shape = (84, 84, 1) # resize to match training 
    wrappers_settings.stack_frames = 4
    wrappers_settings.dilation = 1
    wrappers_settings.no_attack_buttons_combinations = False
    wrappers_settings.normalize_reward = False
    wrappers_settings.stack_actions = 4
    wrappers_settings.scale = True
    wrappers_settings.exclude_image_scaling = True
    wrappers_settings.flatten = True
    wrappers_settings.process_discrete_binary = True
    wrappers_settings.role_relative = True
    wrappers_settings.add_last_action = True
    wrappers_settings.filter_keys = get_filter_keys(settings.game_id, wrappers_settings.flatten)

    # ✅ Create environment with render_mode="rgb_array"
    env = diambra.arena.make(settings.game_id, settings, wrappers_settings, render_mode="human")

    model_path = "" # Path to your trained model

    # ✅ Load agent
    agent = PPO.load(model_path, env)

    # ✅ Start evaluation loop
    obs, info = env.reset()
    while True:
        env.render()  # native rendering

        action, _ = agent.predict(obs, deterministic=False)
        obs, reward, terminated, truncated, info = env.step(action.tolist())

        if terminated or truncated:
            print(f"🧠 Episode finished. Reward: {reward}")
            obs, info = env.reset()
            if info.get("env_done", False):
                break

    env.close()
    print("✅ Evaluation complete.")

