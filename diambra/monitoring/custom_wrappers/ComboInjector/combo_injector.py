"""
combo_injector.py

Revised ComboInjector class that uses shared base definitions and action utilities.
Supports setting an environment name so that it works for more than just Street Fighter.
Also implements a decay mechanism so that the injected combo probability decreases over time.
"""

from collections import deque
import numpy as np
from . import BASE_MOVEMENTS, BASE_ATTACKS, CHARACTER_MOVES, BASE_ACTION_LOOKUP, BASE_INPUT_LOOKUP
from .action_utils import decode_action_string, string_to_idx

class ComboInjector:
    def __init__(self, environment_name: str = 'sfiii3n', mode: str = 'multi_discrete',
                 frame_skip: int = 4, total_decay_steps: int = 16000000):
        """
        Initialize the ComboInjector.

        Parameters
        ----------
        environment_name : str, optional
            Name of the environment (default 'sfiii3n'). Used to select the correct character move definitions.
        mode : str, optional
            Action mode (currently only 'multi_discrete' is supported).
        frame_skip : int, optional
            Frame skip value that affects the duration of hold/charge combos (default 4).
        total_decay_steps : int, optional
            Total number of steps over which injection probability decays from 1.0 to 0.0.
            If set to 0, decay is disabled and injection always occurs.
        """
        #print(f"[ComboInjector] Initializing with environment_name = {environment_name}, mode = {mode}, frame_skip = {frame_skip}")
        self.environment_name = environment_name
        self.mode = mode
        self.frame_skip = frame_skip

        if self.mode != 'multi_discrete':
            raise ValueError("Only 'multi_discrete' mode is currently supported.")

        # Variables for injection decay.
        self.total_decay_steps = total_decay_steps
        self.current_step = 0

        # Per-agent state dictionary.
        self.agent_state = {}

        # Copy base definitions.
        self.base_movement_names = BASE_MOVEMENTS.copy()
        self.base_attack_names = BASE_ATTACKS.copy()

        # Build a flattened list of all possible "movement+attack" combos.
        self._base_actions = []
        for move in self.base_movement_names:
            for attack in self.base_attack_names:
                self._base_actions.append(f"{move}+{attack}")
        #print(f"[ComboInjector] Built _base_actions with {len(self._base_actions)} entries.")

        # Mapping: combo string -> index.
        self.action_idx_lookup = {combo: i for i, combo in enumerate(self._base_actions)}
        #print(f"[ComboInjector] Action mappings built. Total action space size: {len(self.action_idx_lookup)}")

        # Reverse mapping: index -> multi-discrete array.
        self.input_lookup = {}
        for combo_str, idx in self.action_idx_lookup.items():
            move_part, attack_part = combo_str.split('+')
            self.input_lookup[idx] = (self.base_movement_names[move_part] + self.base_attack_names[attack_part]).tolist()
        #print("[ComboInjector] Movement patterns initialized.")

        # Additional attributes for movement patterns.
        self.move_pattern_names = {
            'rqc': ['d', 'dr', 'r'],
            'lqc': ['d', 'dl', 'l'],
            'rhc': ['l', 'dl', 'd', 'dr', 'r'],
            'lhc': ['r', 'dr', 'd', 'dl', 'l'],
            'rdp': ['r', 'd', 'dr'],
            'ldp': ['l', 'd', 'dl'],
            'rfc': ['r', 'dr', 'd', 'dl', 'l', 'ul', 'u', 'ur'],
            'lfc': ['l', 'dl', 'd', 'dr', 'r', 'ur', 'u', 'ul'],
            'sr':  ['r', '', 'r'],
            'sl':  ['l', '', 'l'],
            'sjr': ['d', 'ur'],
            'sj':  ['d', 'u'],
            'sjl': ['d', 'ul'],
        }
        self.direction_move_patterns = {
            'fqc': [['rqc'], ['lqc'], ['rqc', 'lqc']],
            'bqc': [['lqc'], ['rqc'], ['rqc', 'lqc']],
            'fhc': [['rhc'], ['lhc'], ['rhc', 'lhc']],
            'bhc': [['lhc'], ['rhc'], ['rhc', 'lhc']],
            'fdp': [['rdp'], ['ldp'], ['rdp', 'ldp']],
            'bdp': [['ldp'], ['rdp'], ['rdp', 'ldp']],
            'ffc': [['rfc'], ['lfc'], ['rfc', 'lfc']],
            'bfc': [['lfc'], ['rfc'], ['rfc', 'lfc']],
            'sf': [['sr'], ['sl'], ['sr', 'sl']],
            'sb': [['sl'], ['sr'], ['sr', 'sl']],
        }

    def reset(self, characters, super_arts):
        """
        Reset or initialize agent states.
        
        Parameters
        ----------
        characters : list of str
            List of character names for each agent (e.g. ['Alex', 'Gouki']).
        super_arts : list of int
            List of super art indices for each agent (e.g. [1, 2]).
        """
        #print("[ComboInjector] Resetting agent states...")
        self.agent_state = {}
        for i, (character, super_art) in enumerate(zip(characters, super_arts)):
            if character not in CHARACTER_MOVES[self.environment_name]:
                raise NotImplementedError(f"Character '{character}' not supported for environment '{self.environment_name}'.")
            if super_art not in [1, 2, 3]:
                raise NotImplementedError(f"Super art '{super_art}' not supported.")
            self.agent_state[f'agent_{i}'] = {
                'move_sequence': deque(),
                'character': character,
                'super_art': super_art
            }
            #print(f"[ComboInjector] Agent_{i} set to character '{character}' with super_art {super_art}.")

    def in_sequence(self, player: str) -> bool:
        """Return True if the specified agent has queued moves."""
        return len(self.agent_state[player]['move_sequence']) > 0

    def sample_character_special(self, player: str) -> list:
        """
        Generate a special or super-art combo for the given agent.
        
        Parameters
        ----------
        player : str
            The agent ID (e.g. 'agent_0').
        
        Returns
        -------
        list of str
            A list of combo tokens (e.g. ['d+lp', 'dr+lp', 'r+lp']).
        """
        #print(f"[ComboInjector] Sampling special combo for {player}.")
        character = self.agent_state[player]['character']
        super_art = self.agent_state[player]['super_art']

        if character not in CHARACTER_MOVES[self.environment_name]:
            raise NotImplementedError(f"Character '{character}' not supported for environment '{self.environment_name}'.")
        roll = np.random.rand()
        moves_dict = CHARACTER_MOVES[self.environment_name][character]
        prob_acc = 0.0
        for move_name, params in moves_dict.items():
            prob_acc += params['prob']
            if roll <= prob_acc:
                if move_name == 'super_art':
                    combo_key = f'combo_str_{super_art}'
                    action_str = params[combo_key]
                else:
                    action_str = params['combo_str']
                decoded = decode_action_string(action_str)
                #print(f"[ComboInjector] Selected special combo: {decoded}")
                return decoded
        fallback = [np.random.choice(list(BASE_ACTION_LOOKUP.keys()))]
        #print(f"[ComboInjector] No combo selected; falling back to: {fallback}")
        return fallback

    def sample(self, prob_jump=0.05, prob_basic=0.40, prob_combo=0.30,
               prob_cancel=0.2, prob_movement=0.25) -> dict:
        """
        Generate the next action(s) for all agents.
        Returns a dictionary with:
          - 'discrete': mapping from agent ID to an integer action index.
          - 'multi_discrete': mapping from agent ID to the corresponding multi-discrete action array.
        If the injection has decayed (based on the step count), returns None.
        """
        # Compute injection probability (linearly decaying)
        if self.total_decay_steps > 0:
            injection_prob = max(0.0, 1.0 - self.current_step / self.total_decay_steps)
        else:
            injection_prob = 1.0

        self.current_step += 1

        # If the random number is above the current injection probability, skip injection.
        if np.random.rand() >= injection_prob:
            return None

        actions = {'discrete': {}, 'multi_discrete': {}}
        raw_probs = np.array([prob_jump, prob_basic, prob_combo, prob_movement])
        raw_probs /= raw_probs.sum()
        cdfs = np.cumsum(raw_probs)
        #print("[ComboInjector] Action category CDFs:", cdfs)

        for i, agent_id in enumerate(self.agent_state):
            if not self.in_sequence(agent_id):
                roll = np.random.rand()
                side = -1  # Default side; extend as needed.
                #print(f"[ComboInjector] Agent '{agent_id}' move_sequence empty. Roll = {roll}")
                if roll < cdfs[0]:
                    seq_str = [np.random.choice(['ul+', 'u+', 'ur+'])]
                    #print(f"[ComboInjector] Jump action chosen: {seq_str}")
                elif roll < cdfs[1]:
                    seq_str = [np.random.choice(list(BASE_ACTION_LOOKUP.keys()))]
                    #print(f"[ComboInjector] Basic action chosen: {seq_str}")
                elif roll < cdfs[2]:
                    seq_str = self.sample_character_special(agent_id)
                    if np.random.rand() < prob_cancel:
                        cutoff = np.random.randint(1, len(seq_str) + 1)
                        seq_str = seq_str[:cutoff]
                        #print(f"[ComboInjector] Combo cancelled early. New sequence: {seq_str}")
                else:
                    seq_str = [np.random.choice(['l+', 'dl+', 'd+', 'dr+', 'r+'])]
                    num_repeats = np.random.randint(12, 64)
                    seq_str = seq_str * num_repeats
                    #print(f"[ComboInjector] Movement-based action chosen: {seq_str}")
                seq_idx = string_to_idx(seq_str)
                #print(f"[ComboInjector] Converted tokens {seq_str} to indices {seq_idx}")
                self.agent_state[agent_id]['move_sequence'] = deque(seq_idx)
            a_idx = self.agent_state[agent_id]['move_sequence'].popleft()
            a_multi = BASE_INPUT_LOOKUP[a_idx]
            #print(f"[ComboInjector] Agent '{agent_id}' action: index={a_idx}, multi_discrete={a_multi}")
            actions['discrete'][agent_id] = a_idx
            actions['multi_discrete'][agent_id] = a_multi

        return actions

    def string_to_idx(self, string_list: list) -> list:
        """Convert each token in the list (e.g. 'd+lp') into its integer index."""
        return string_to_idx(string_list)
