# __init__.py

import numpy as np

# Base movement definitions (multi-discrete format)
BASE_MOVEMENTS = {
    "":   np.array([0, 0]),
    "l":  np.array([1, 0]),
    "ul": np.array([2, 0]),
    "u":  np.array([3, 0]),
    "ur": np.array([4, 0]),
    "r":  np.array([5, 0]),
    "dr": np.array([6, 0]),
    "d":  np.array([7, 0]),
    "dl": np.array([8, 0]),
}

# Base attack definitions (multi-discrete format)
BASE_ATTACKS = {
    "":   np.array([0, 0]),
    "lp": np.array([0, 1]),
    "mp": np.array([0, 2]),
    "hp": np.array([0, 3]),
    "lk": np.array([0, 4]),
    "mk": np.array([0, 5]),
    "hk": np.array([0, 6]),
}

# Character-specific moves and combos
CHARACTER_MOVES = {
    'sfiii3n': {
        "Alex" : {'power_bomb' : {'prob': 0.15, 'combo_str' : 'comb_bhc_p'},
                    'spiral_ddt' : {'prob' : 0.15, 'combo_str' : 'comb_bhc_k'},
                    'flash_chop' : {'prob' : 0.15, 'combo_str' : 'comb_fqc_p'},
                    'air_knee_smash' : {'prob' : 0.15, 'combo_str' : 'comb_fdp_k'},
                    'air_stampede' : {'prob' : 0.15, 'combo_str' : 'hold_d_16_64_k'},
                    'slash_elbow' : {'prob' : 0.15, 'combo_str' : 'hold_b_16_64_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_ffc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Twelve" : {'ndl' : {'prob': 0.3, 'combo_str' : 'comb_fqc_p'},
                    'axe' : {'prob': 0.3, 'combo_str' : 'comb_bqc_p/rep_p_3_12_t'},
                    'dra' : {'prob' : 0.3, 'combo_str' : 'comb_bqc_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mk',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Hugo" : {'shootdown_backbreaker' : {'prob': 0.15, 'combo_str' : 'comb_fdp_k'},
                    'ultra_throw' : {'prob': 0.15, 'combo_str' : 'comb_bhc_k'},
                    'moonsault_press' : {'prob' : 0.15, 'combo_str' : 'comb_ffc_p'},
                    'meat_squasher' : {'prob' : 0.15, 'combo_str' : 'comb_ffc_k'},
                    'giant_palm_bomber' : {'prob' : 0.15, 'combo_str' : 'comb_bqc_p'},
                    'monster_lariat' : {'prob' : 0.15, 'combo_str' : 'comb_fqc_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2ffc_mp',
                                    'combo_str_2' : 'comb_2fqc_mk',
                                    'combo_str_3' : 'comb_2fqc_mp/rep_mp_0_8_',}
                    },
        "Sean" : {'zenten' : {'prob': 0.18, 'combo_str' : 'comb_bqc_p'},
                    'sean_tackle' : {'prob' : 0.18, 'combo_str' : 'comb_fhc_p/rep_p_0_8_'},
                    'dragon_smash' : {'prob' : 0.18, 'combo_str' : 'comb_fdp_p'},
                    'tornado' : {'prob' : 0.18, 'combo_str' : 'comb_bqc_k'},
                    'ryuubi_kyaku' : {'prob' : 0.18, 'combo_str' : 'comb_fqc_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp/rep_mp_0_12_t',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Makoto" : {'karakusa' : {'prob': 0.18, 'combo_str' : 'comb_bhc_k'},
                    'hayate' : {'prob' : 0.18, 'combo_str' : 'comb_fqc_p/rep_p_0_8_'},
                    'fukiage' : {'prob' : 0.18, 'combo_str' : 'comb_fdp_p'},
                    'oroshi' : {'prob' : 0.18, 'combo_str' : 'comb_bqc_p'},
                    'tsurugi' : {'prob' : 0.18, 'combo_str' : 'comb_bqc_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mk',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Elena" : {'rhino_horn' : {'prob': 0.18, 'combo_str' : 'comb_fhc_k'},
                    'mallet_smash' : {'prob' : 0.18, 'combo_str' : 'comb_bhc_p'},
                    'spin_scythe' : {'prob' : 0.18, 'combo_str' : 'comb_bqc_k'},
                    'scratch_wheel' : {'prob' : 0.18, 'combo_str' : 'comb_fdp_k'},
                    'lynx_tail' : {'prob' : 0.18, 'combo_str' : 'comb_bdp_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mk',
                                    'combo_str_2' : 'comb_2fqc_mk',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Ibuki" : {'raida' : {'prob': 0.13, 'combo_str' : 'comb_bhc_p'},
                    'kasumi_gake' : {'prob' : 0.13, 'combo_str' : 'comb_fqc_k'},
                    'tsumuji' : {'prob' : 0.12, 'combo_str' : 'comb_bqc_k'},
                    'tsuji_goe' : {'prob' : 0.13, 'combo_str' : 'comb_fdp_p'},
                    'kunai_kubi_ori' : {'prob' : 0.13, 'combo_str' : 'comb_fqc_p'},
                    'kazekiri' : {'prob' : 0.13, 'combo_str' : 'comb_fdp_k'},
                    'hien' : {'prob' : 0.13, 'combo_str' : 'comb_bdp_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp/rep_mp_0_16_t',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Chun-Li" : {'kikoken' : {'prob': 0.225, 'combo_str' : 'comb_fhc_p'},
                    'hazanshu' : {'prob' : 0.225, 'combo_str' : 'comb_bhc_k'},
                    'spinning_bird_kick' : {'prob' : 0.225, 'combo_str' : 'hold_d_22_64_k'},
                    'hyakuretsu_kyaku' : {'prob' : 0.225, 'combo_str' : 'rep_k_3_16_t'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mk',
                                    'combo_str_3' : 'comb_2fqc_mk',}
                    },
        "Dudley" : {'ducking_straight' : {'prob': 0.15, 'combo_str' : 'comb_fhc_k/rep_p_0_4_t'},
                    'ducking_upper' : {'prob': 0.15, 'combo_str' : 'comb_fhc_k/rep_k_0_4_t'},
                    'machine_gun_blow' : {'prob' : 0.15, 'combo_str' : 'comb_fhc_p'},
                    'cross_counter' : {'prob' : 0.15, 'combo_str' : 'comb_bhc_p'},
                    'jet_upper' : {'prob' : 0.15, 'combo_str' : 'comb_fdp_p'},
                    'short_swing_blow' : {'prob': 0.15, 'combo_str' : 'comb_bhc_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp/rep_mp_6_18_t',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Necro" : {'snake_fang' : {'prob': 0.18, 'combo_str' : 'comb_fhc_k'},
                    'denji_blast' : {'prob' : 0.18, 'combo_str' : 'comb_fdp_p/rep_p_0_12_t'},
                    'flying_viper' : {'prob' : 0.18, 'combo_str' : 'comb_bqc_p'},
                    'rising_kobra' : {'prob' : 0.18, 'combo_str' : 'comb_bqc_k'},
                    'tornado_hook' : {'prob' : 0.18, 'combo_str' : 'comb_fhc_p'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp/rep_mp_0_16_t',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Q" : {'capture_deadly_blow' : {'prob': 0.225, 'combo_str' : 'comb_bhc_k'},
                    'dashing_head' : {'prob' : 0.225, 'combo_str' : 'hold_b_22_64_p/rep_p_0_8_'},
                    'dashing_leg' : {'prob' : 0.225, 'combo_str' : 'hold_b_22_64_k'},
                    'high_speed_barage' : {'prob' : 0.225, 'combo_str' : 'comb_bqc_p'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Oro" : {'niu_riki' : {'prob': 0.225, 'combo_str' : 'comb_bhc_p'},
                    'nichirin_shou' : {'prob' : 0.225, 'combo_str' : 'hold_b_16_64_p'},
                    'oni_yanma' : {'prob' : 0.225, 'combo_str' : 'hold_d_16_64_p'},
                    'jinchuu_watari_hitobashira_nobori' : {'prob' : 0.225, 'combo_str' : 'comb_fqc_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Urien" : {'metallic_sphere' : {'prob': 0.225, 'combo_str' : 'comb_fqc_p/rep_p_0_12_'},
                    'chariot_tackle' : {'prob' : 0.225, 'combo_str' : 'hold_b_16_64_k'},
                    'dangerous_headbutt' : {'prob' : 0.225, 'combo_str' : 'hold_d_16_64_p'},
                    'violence_knee_drop' : {'prob' : 0.225, 'combo_str' : 'hold_d_16_64_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Remy" : {'light_of_virtue' : {'prob': 0.225, 'combo_str' : 'hold_b_22_64_p'},
                    'light_of_virtue_low' : {'prob' : 0.225, 'combo_str' : 'hold_b_22_64_k'},
                    'rising_rage_flash' : {'prob' : 0.225, 'combo_str' : 'hold_d_22_128_k'},
                    'cold_blue_kick' : {'prob' : 0.225, 'combo_str' : 'comb_bqc_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mk',
                                    'combo_str_3' : 'comb_2fqc_mk',}
                    },
        "Ryu" : {'hadouken' : {'prob': 0.225, 'combo_str' : 'comb_fqc_p'},
                    'shoryuken' : {'prob' : 0.225, 'combo_str' : 'comb_fdp_p'},
                    'tatsumaki_senpukyaku' : {'prob' : 0.225, 'combo_str' : 'comb_bqc_k'},
                    'joudan_sokutou_geri' : {'prob' : 0.225, 'combo_str' : 'comb_fhc_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mp/rep_mp_0_16_',}
                    },
        "Gouki" : {'go_zankuu_hadouken' : {'prob': 0.15, 'combo_str' : 'comb_fqc_p'},
                    'shakenutsu-hadouken' : {'prob' : 0.15, 'combo_str' : 'comb_bhc_p'},
                    'go_shoryuken' : {'prob' : 0.15, 'combo_str' : 'comb_fdp_p'},
                    'tatsumaki_senpukyaku' : {'prob' : 0.15, 'combo_str' : 'comb_bqc_k'},
                    'hyakkishu_go' : {'prob' : 0.075, 'combo_str' : 'comb_fdp_k/rep_p_0_2_t'},
                    'hyakkishu_sho' : {'prob' : 0.075, 'combo_str' : 'comb_fdp_k/rep_k_0_2_t'},
                    'hyakkishu_sho_sai' : {'prob' : 0.075, 'combo_str' : 'comb_fdp_k/rep_mpk_0_2_t'},
                    'shungokusatsu' : {'prob' : 0.055, 'combo_str' : 'raw_+lp_+_+lp/comb_f_/raw_+lk_+_+hp'},
                    'target_combo_1' : {'prob' : 0.02, 'combo_str' : 'rep_mp_5_5_t/raw_+/rep_hp_5_5_t'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mk',}
                    },
        "Yun" : {'zenpou_tenshin' : {'prob': 0.18, 'combo_str' : 'comb_bhc_k'},
                    'kobokushi' : {'prob' : 0.18, 'combo_str' : 'comb_bqc_p'},
                    'zesshou_hohou' : {'prob' : 0.18, 'combo_str' : 'comb_fqc_p'},
                    'tetsuzanko' : {'prob' : 0.18, 'combo_str' : 'comb_fdp_p'},
                    'nishoukyaku' : {'prob' : 0.18, 'combo_str' : 'comb_fdp_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mp',
                                    'combo_str_3' : 'comb_2fqc_mk',}
                    },
        "Yang" : {'tourou_zan' : {'prob': 0.18, 'combo_str' : 'comb_fqc_p'},
                    'byakko_soushouda' : {'prob': 0.18, 'combo_str' : 'comb_bqc_p'},
                    'senkyuutai' : {'prob' : 0.18, 'combo_str' : 'comb_fqc_k'},
                    'zenpou_tenshin' : {'prob' : 0.18, 'combo_str' : 'comb_bhc_k'},
                    'kaihou' : {'prob' : 0.18, 'combo_str' : 'comb_fdp_k'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mk',
                                    'combo_str_3' : 'comb_2fqc_mp',}
                    },
        "Ken" : {'hadouken' : {'prob': 0.25, 'combo_str' : 'comb_fqc_p'},
                    'shoryuken' : {'prob' : 0.25, 'combo_str' : 'comb_fdp_p'},
                    'tatsumaki_senpukyaku' : {'prob' : 0.25, 'combo_str' : 'comb_bqc_k'},
                    'grab' : {'prob' : 0.15, 'combo_str' : 'rep_lpk_1_8_t'},
                    'super_art' : {'prob' : 0.1, 'combo_str_1' : 'comb_2fqc_mp',
                                    'combo_str_2' : 'comb_2fqc_mk/rep_mk_0_16_t',
                                    'combo_str_3' : 'comb_2fqc_mk',}
                    },
    },
}

# Lookup table for quick indexing of combined move+attack actions
BASE_ACTION_LOOKUP = {
    f"{move}+{attack}": i
    for i, (move, attack) in enumerate(
        (m, a) for m in BASE_MOVEMENTS.keys() for a in BASE_ATTACKS.keys()
    )
}

# Reverse mapping: index -> multi-discrete array.
BASE_INPUT_LOOKUP = {}
for combo_str, idx in BASE_ACTION_LOOKUP.items():
    move_part, attack_part = combo_str.split('+')
    movement_arr = BASE_MOVEMENTS[move_part]
    attack_arr = BASE_ATTACKS[attack_part]
    BASE_INPUT_LOOKUP[idx] = (movement_arr + attack_arr).tolist()

__all__ = [
    "BASE_MOVEMENTS",
    "BASE_ATTACKS",
    "CHARACTER_MOVES",
    "BASE_ACTION_LOOKUP",
    "BASE_INPUT_LOOKUP",
    "ComboInjector",
]
  
from .combo_injector import ComboInjector