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
- **OpenCV** (for evaluation, install with `pip install opencv-python`)
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


```bash
pip install -r requirements.txt
```

---

## **Usage**

### **Training**

The training script (`train.py`) leverages PPO to train agents in the DIAMBRA Arena environment. It automatically loads configuration settings from `config.py` and utilizes the custom filter keys from `filter_keys.py`.

#### **Run Training**

```bash
python train.py
```

**Notes:**

- The script checks for existing model checkpoints in the `./trained_models` directory and resumes training if a checkpoint is found.
- Training logs and tensorboard logs are saved in `./tensorboard_logs` and `./output/logs` respectively.
- Modify `config.py` to tailor training parameters (e.g., total training steps, game settings, wrapper configurations) as needed.

---

## **Evaluation**

The evaluation script (`eval.py`) is designed to load a trained PPO model and run an evaluation session in the DIAMBRA Arena environment, rendering the gameplay in an OpenCV window.

### **Configuration**

Before running the evaluation script, make sure to update the following in `eval.py`:
- **Game Settings**: Set `settings.game_id` to your desired game (e.g., `"sfiii3n"`).
- **Model Path**: Specify the path to your trained model checkpoint by setting `model_path`.

### **Running Evaluation**

Run the evaluation script with:

```bash
python eval.py
```

The evaluation script will:
- Create the DIAMBRA Arena environment with `render_mode="rgb_array"`.
- Load the PPO agent from the specified `model_path`.
- Render the game frames using OpenCV (the window title will be "Game").
- Continuously predict actions using the trained agent.
- Reset the environment when an episode is terminated, and exit when the environment signals completion.

**To exit evaluation:**  
Press `CTRL+C` in the terminal or close the OpenCV window. The script includes cleanup commands to close the environment and destroy the OpenCV window.

---

## **Configuration Overview**

### **Environment & Game Settings (`config.py` and within eval.py)**

- **env_settings**: Sets the number of parallel environments, autosave frequency, and total training steps.
- **settings (Game Settings)**: Defines parameters such as game id, difficulty, characters, and action space.
- **wrappers_settings**: Configures environment wrappers (frame stacking, scaling, action processing, etc.) and applies game-specific filter keys.
- **ppo_settings**: Contains PPO hyperparameters including gamma, number of epochs, batch size (dynamically calculated), learning rate scheduling, and policy architecture.
- **Paths**: Directories for saving models (`./trained_models`), Tensorboard logs (`./tensorboard_logs`), and monitor logs (`./output/logs`).

### **Filter Keys (`filter_keys.py`)**

- Provides the `get_filter_keys` function to generate a list of observation filter keys based on the game id and flatten setting.
- Helps standardize the observation space across different games by including both global keys and game-specific keys.

---

## **How It Works**

1. **Configuration Loading**: The scripts load all necessary configurations from `config.py` and `filter_keys.py`.
2. **Environment Creation**: Uses `make_sb3_env` (for training) or `diambra.arena.make` (for evaluation) to create the DIAMBRA Arena environment with custom settings.
3. **Checkpoint Handling** (Training): Checks for existing checkpoints to resume training or starts a new session.
4. **PPO Training and Evaluation**: Initializes the PPO agent for training or evaluation.
5. **Rendering (Evaluation Only)**: During evaluation, frames are rendered and displayed in an OpenCV window.
6. **Logging & Autosave**: Periodically saves training progress and logs metrics for Tensorboard visualization.
7. **Cleanup**: Saves the final model and gracefully closes the environment once training completes or evaluation is stopped.

---

## **Example Output**

### **Training:**

```bash
Activated 32 environment(s)
No checkpoint found. Starting new training session.
Starting Training...
...
Training Completed!
Model saved at ./trained_models
Environment Closed.
```

### **Evaluation:**

An OpenCV window will display the game frames. The terminal will continuously log the evaluation process. Ensure you exit the evaluation session gracefully using `CTRL+C` or by closing the window.

---

## **Troubleshooting**

- **Batch Size Issues**: Ensure that the total batch size is evenly divisible by the number of minibatches. Adjust `nminibatches` or `n_steps` in `config.py` if necessary.
- **Checkpoint Problems**: Verify that the `./trained_models` directory exists and is writable.
- **Dependency Errors**: Double-check that all required packages are installed and correctly imported.
- **Evaluation Issues**: If the OpenCV window fails to open, ensure `opencv-python` is installed and no other processes are blocking window creation.
