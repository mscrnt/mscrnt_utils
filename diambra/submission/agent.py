from diambra.arena import SpaceTypes
from diambra.arena.stable_baselines3.make_sb3_env import EnvironmentSettings, WrappersSettings
from stable_baselines3 import PPO
import diambra
from filter_keys import get_filter_keys

if __name__ == "__main__":


    # Settings
    settings = EnvironmentSettings()
    settings.difficulty = 8
    settings.characters = "Ken"
    settings.action_space = SpaceTypes.MULTI_DISCRETE
    settings.step_ratio = 1
    settings.super_art = 3
    settings.game_id = "sfiii3n"

    # Wrappers Settings
    wrappers_settings = WrappersSettings()
    wrappers_settings.frame_shape = (84, 84, 1)
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
