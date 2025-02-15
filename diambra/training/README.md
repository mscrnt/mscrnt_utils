Hey Kenneth, here's a README for the `diambra/training` folder based on your files and the provided template:

---

# **DIAMBRA Arena Training**

A **training module** that uses **PPO (Proximal Policy Optimization)** from **stable-baselines3** to train agents for **DIAMBRA Arena**. This folder contains all the necessary scripts and configuration files to set up the training environment, customize game-specific filter keys, and configure PPO training parameters.

📌 **Part of the [`mscrnt_utils`](https://github.com/mscrnt/mscrnt_utils) repository.**

---

## **Features**

- **Customizable Environment Settings**: Configure parallel environments, training steps, autosave frequency, and more.
- **Game-Specific Configuration**: Set up game settings (e.g., game id, difficulty, characters) and environment wrappers.
- **Dynamic Filter Keys**: Generate game-specific observation filter keys to standardize inputs across games.
- **PPO Training Integration**: Leverage stable-baselines3’s PPO with dynamic learning rate and clip range schedules.
- **Automatic Checkpointing**: Resume training from the latest checkpoint found in the `./trained_models` folder.
- **Tensorboard Logging**: Log training metrics for visualization in Tensorboard.

---

## **Installation**

Ensure you have the following installed:

- **Python 3.10+**
- **PyTorch**
- **Stable-Baselines3**
- **DIAMBRA Arena** (and associated dependencies)
- Other required Python packages (see `requirements.txt` if available)

### **1. Clone the Repository**

To get the entire **mscrnt_utils** repository:

```bash
git clone https://github.com/mscrnt/mscrnt_utils.git
cd mscrnt_utils/diambra/training
```

#### **OR**: Clone only the training module using sparse-checkout:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/mscrnt/mscrnt_utils.git
cd mscrnt_utils
git sparse-checkout set diambra/training
cd diambra/training
```

### **2. Install Dependencies**

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, ensure you install the following packages:

- torch
- stable-baselines3
- diambra.arena
- argparse (Python standard library)

---

## **Usage**

The training script (`train.py`) leverages PPO to train agents in the DIAMBRA Arena environment. It automatically loads configuration settings from `config.py` and utilizes the custom filter keys from `filter_keys.py`.

### **Run Training**

```bash
python train.py
```

**Notes:**

- The script checks for existing model checkpoints in the `./trained_models` directory and resumes training if a checkpoint is found.
- Training logs and tensorboard logs are saved in `./tensorboard_logs` and `./output/logs` respectively.
- Modify `config.py` to tailor training parameters (e.g., total training steps, game settings, wrapper configurations) as needed.

---

## **Configuration Overview**

### **Environment & Game Settings (`config.py`)**

- **env_settings**: Sets the number of parallel environments, autosave frequency, and total training steps.
- **settings**: Defines game-specific parameters such as game id, difficulty, character selections, and frame shape.
- **wrappers_settings**: Configures additional environment wrappers (frame stacking, action processing, reward normalization, etc.) and applies game-specific filter keys.
- **ppo_settings**: Contains PPO hyperparameters including gamma, number of epochs, batch size (dynamically calculated), learning rate scheduling, and policy architecture.
- **Paths**: Directories for saving models (`./trained_models`), Tensorboard logs (`./tensorboard_logs`), and monitor logs (`./output/logs`).

### **Filter Keys (`filter_keys.py`)**

- Provides the `get_filter_keys` function to generate a list of observation filter keys based on the game id and flatten setting.
- Helps standardize the observation space across different games by including both global keys and game-specific keys.

---

## **How It Works**

1. **Configuration Loading**: The training script loads all necessary configurations from `config.py` and `filter_keys.py`.
2. **Environment Creation**: Uses `make_sb3_env` to create the DIAMBRA Arena environment with customized settings.
3. **Checkpoint Handling**: Checks for existing checkpoints in the model directory to resume training, or starts a new session if none are found.
4. **PPO Training**: Initializes the PPO agent and begins training using dynamic learning rate and clip range schedules.
5. **Logging & Autosave**: Periodically saves training progress and logs metrics for visualization in Tensorboard.
6. **Cleanup**: Saves the final model and gracefully closes the environment once training completes or is interrupted.

---

## **Example Output**

```bash
Activated 32 environment(s)
No checkpoint found. Starting new training session.
Starting Training...
...
Training Completed!
Model saved at ./trained_models
Environment Closed.
```

---

## **Troubleshooting**

- **Batch Size Issues**: Ensure that the total batch size is evenly divisible by the number of minibatches. Adjust `nminibatches` or `n_steps` in `config.py` if necessary.
- **Checkpoint Problems**: Verify that the `./trained_models` directory exists and is writable.
- **Dependency Errors**: Double-check that all required packages are installed and correctly imported.
