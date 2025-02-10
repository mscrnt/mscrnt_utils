"""
action_utils.py

Contains utility functions for processing, encoding, and generating
actions (combo strings) for fighting game environments.

Author: ruhe (modified with debug prints)
"""

import numpy as np
from . import BASE_ACTION_LOOKUP

# Mirroring table for reversing left/right movement inputs when needed.
MIRROR_MAP = {
    'r': 'l', 'l': 'r', 'dr': 'dl', 'dl': 'dr',
    'ur': 'ul', 'ul': 'ur', 'sr': 'sl', 'sl': 'sr'
}

def string_to_idx(string_list: list) -> list:
    """
    Convert each 'dir+attack' token into an integer action index.
    
    Parameters
    ----------
    string_list : list of str
        e.g. ['d+lp', 'dr+lp', 'r+lp'].
    
    Returns
    -------
    list of int
        The integer indices corresponding to each token.
    """
    #print("[action_utils.string_to_idx] Converting tokens:", string_list)
    indices = [BASE_ACTION_LOOKUP.get(s, np.random.randint(0, len(BASE_ACTION_LOOKUP)))
               for s in string_list]
    #print("[action_utils.string_to_idx] Converted indices:", indices)
    return indices

def combine_actions(move_string: str, attack_string: str, side: int = 0) -> list:
    """
    Helper function to stitch together a movement pattern with an attack.
    
    Parameters
    ----------
    move_string : str
        A short code for a movement pattern (e.g., 'qc', 'dp') or a literal direction.
    attack_string : str
        A code for the type of attack (e.g., 'p', 'k', 'lp').
    side : int, optional
        Side indicator (default -1).
    
    Returns
    -------
    list of str
        A list of combined tokens, e.g. ['d+lp', 'dr+lp', 'r+lp'].
    """
    #print(f"[action_utils.combine_actions] Called with move_string='{move_string}', attack_string='{attack_string}', side={side}")
    move_patterns = {
        'qc': ['d', 'dr', 'r'],
        'dp': ['r', 'd', 'dr'],
        'hc': ['l', 'dl', 'd', 'dr', 'r']
    }
    if move_string in move_patterns:
        m_seq = move_patterns[move_string]
    else:
        m_seq = [move_string]
    #print(f"[action_utils.combine_actions] Movement sequence: {m_seq}")

    if side == 1:
        m_seq = [MIRROR_MAP.get(m, m) for m in m_seq]

    
    if attack_string == 'p':
        attack = np.random.choice(['lp', 'mp', 'hp'])
    elif attack_string == 'k':
        attack = np.random.choice(['lk', 'mk', 'hk'])
    else:
        attack = attack_string
    #print(f"[action_utils.combine_actions] Selected attack: {attack}")

    a_seq = [''] * (len(m_seq) - 1) + [attack]
    combined = [f"{m}+{a}" for m, a in zip(m_seq, a_seq)]
    #print(f"[action_utils.combine_actions] Combined tokens: {combined}")
    return combined

def hold_direction(direction: str, min_frame: str, max_frame: str, release: str = '') -> list:
    """
    Helper function for charge moves, where a direction is held for a randomized
    duration and then (optionally) released with an attack.
    
    Parameters
    ----------
    direction : str
        The direction to hold (e.g., 'd').
    min_frame : str
        Minimum frames to hold.
    max_frame : str
        Maximum frames to hold.
    release : str, optional
        If 'p' or 'k', a random punch/kick is chosen upon release.
    
    Returns
    -------
    list of str
        A sequence like ['d+', 'd+', 'd+', 'u+lk'].
    """
    #print(f"[action_utils.hold_direction] Called with direction='{direction}', min_frame='{min_frame}', max_frame='{max_frame}', release='{release}'")
    min_f = int(min_frame)
    max_f = int(max_frame)
    hold_duration = np.random.randint(min_f, max_f + 1)
    num_steps = hold_duration // 4
    #print(f"[action_utils.hold_direction] Hold duration: {hold_duration}, num_steps: {num_steps}")

    if release in ['p', 'k']:
        if release == 'p':
            attack = np.random.choice(['lp', 'mp', 'hp'])
        else:
            attack = np.random.choice(['lk', 'mk', 'hk'])
    else:
        attack = release
    #print(f"[action_utils.hold_direction] Selected release attack: {attack}")

    sequence = [f"{direction}+"] * num_steps
    if release:
        sequence.append(f"u+{attack}")
    #print(f"[action_utils.hold_direction] Sequence: {sequence}")
    return sequence

def repeat_attack(attack_string: str, min_repeats: str, max_repeats: str, tap: str = '') -> list:
    """
    Helper function for generating repeated attack sequences.
    
    Parameters
    ----------
    attack_string : str
        e.g., 'p', 'k', 'lp', 'mk'
    min_repeats : str
        Minimum number of repeats.
    max_repeats : str
        Maximum number of repeats.
    tap : str
        If non-empty, indicates that a tap (a '+' token) should be inserted.
    
    Returns
    -------
    list of str
        Example: ['+lp', '+', '+lp', '+', '+lp'].
    """
    #print(f"[action_utils.repeat_attack] Called with attack_string='{attack_string}', min_repeats='{min_repeats}', max_repeats='{max_repeats}', tap='{tap}'")
    min_r = int(min_repeats)
    max_r = int(max_repeats)
    reps = np.random.randint(min_r, max_r + 1)
    #print(f"[action_utils.repeat_attack] Number of repeats: {reps}")

    if attack_string in ['p', 'k']:
        if attack_string == 'p':
            attack = np.random.choice(['lp', 'mp', 'hp'])
        else:
            attack = np.random.choice(['lk', 'mk', 'hk'])
    else:
        attack = attack_string
    #print(f"[action_utils.repeat_attack] Selected attack: {attack}")

    if tap:
        result = [f"+{attack}" for _ in range(reps)]
    else:
        result = [attack] * reps
    #print(f"[action_utils.repeat_attack] Resulting sequence: {result}")
    return result

def decode_action_string(action_string: str, side: int = -1) -> list:
    """
    Parse the custom combo syntax into a list of final 'dir+attack' tokens.
    
    The combo string can contain multiple segments separated by '/'.
    Each segment can be of types:
      - 'comb_<move>_<attack>' for standard combos,
      - 'hold_<dir>_<min>_<max>_<release>' for charge moves,
      - 'rep_<attack>_<min>_<max>_<tap>' for repeated attacks,
      - 'raw_<token>' for literal tokens.
    
    Parameters
    ----------
    action_string : str
        e.g. 'comb_qc_p/rep_p_0_8_t'
    side : int, optional
        Side indicator (default -1).
    
    Returns
    -------
    list of str
        Final list, e.g. ['d+lp', 'dr+lp', 'r+lp'].
    """
    #print(f"[action_utils.decode_action_string] Called with action_string='{action_string}', side={side}")
    action_sequence = []
    segments = action_string.split('/')
    #print(f"[action_utils.decode_action_string] Segments: {segments}")
    for segment in segments:
        parts = segment.split('_')
        #print(f"[action_utils.decode_action_string] Processing segment: '{segment}' -> parts: {parts}")
        if parts[0] == 'comb':
            move_str, attack_str = parts[1], parts[2]
            combined = combine_actions(move_str, attack_str, side)
            #print(f"[action_utils.decode_action_string] Decoded 'comb' segment: {combined}")
            action_sequence += combined
        elif parts[0] == 'hold':
            direction, min_frame, max_frame, release = parts[1:]
            held = hold_direction(direction, min_frame, max_frame, release)
            #print(f"[action_utils.decode_action_string] Decoded 'hold' segment: {held}")
            action_sequence += held
        elif parts[0] == 'rep':
            attack_str, min_r, max_r, tap_str = parts[1:]
            repeated = repeat_attack(attack_str, min_r, max_r, tap_str)
            #print(f"[action_utils.decode_action_string] Decoded 'rep' segment: {repeated}")
            action_sequence += repeated
        elif parts[0] == 'raw':
            raw_tokens = parts[1:]
            #print(f"[action_utils.decode_action_string] Decoded 'raw' segment: {raw_tokens}")
            action_sequence += raw_tokens
    #print(f"[action_utils.decode_action_string] Final decoded action sequence: {action_sequence}")
    return action_sequence
