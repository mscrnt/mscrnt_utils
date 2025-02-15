def get_filter_keys(game_id, flatten):
    # Global keys available for all games
    global_keys = {
        "stage",
        "timer",
        "action",
        "frame",
    }

    # Player-specific keys for each game
    game_specific_keys = {
        "doapp": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character": ["own_character", "opp_character"] if flatten else ["P1.character", "P2.character"],
            "health": ["own_health", "opp_health"] if flatten else ["P1.health", "P2.health"]
        },
        "sfiii3n": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character": ["own_character", "opp_character"] if flatten else ["P1.character", "P2.character"],
            "health": ["own_health", "opp_health"] if flatten else ["P1.health", "P2.health"],
            "super_bar": ["own_super_bar", "opp_super_bar"] if flatten else ["P1.super_bar", "P2.super_bar"],
            "stun_bar": ["own_stun_bar", "opp_stun_bar"] if flatten else ["P1.stun_bar", "P2.stun_bar"],
            "super_count": ["own_super_count", "opp_super_count"] if flatten else ["P1.super_count", "P2.super_count"],
            "stunned": ["own_stunned", "opp_stunned"] if flatten else ["P1.stunned", "P2.stunned"],
            "super_type": ["own_super_type", "opp_super_type"] if flatten else ["P1.super_type", "P2.super_type"],
            "super_max": ["own_super_max_count", "opp_super_max_count"] if flatten else ["P1.super_max_count", "P2.super_max_count"]
        },
        "tektagt": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character_1": ["own_character_1", "opp_character_1"] if flatten else ["P1.character_1", "P2.character_1"],
            "character_2": ["own_character_2", "opp_character_2"] if flatten else ["P1.character_2", "P2.character_2"],
            "health_1": ["own_health_1", "opp_health_1"] if flatten else ["P1.health_1", "P2.health_1"],
            "health_2": ["own_health_2", "opp_health_2"] if flatten else ["P1.health_2", "P2.health_2"],
            "active_character": ["own_active_character", "opp_active_character"] if flatten else ["P1.active_character", "P2.active_character"]
        },
        "umk3": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character": ["own_character", "opp_character"] if flatten else ["P1.character", "P2.character"],
            "health": ["own_health", "opp_health"] if flatten else ["P1.health", "P2.health"],
            "aggressor_bar": ["own_aggressor_bar", "opp_aggressor_bar"] if flatten else ["P1.aggressor_bar", "P2.aggressor_bar"]
        },
        "samsh5sp": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character": ["own_character", "opp_character"] if flatten else ["P1.character", "P2.character"],
            "health": ["own_health", "opp_health"] if flatten else ["P1.health", "P2.health"],
            "rage_bar": ["own_rage_bar", "opp_rage_bar"] if flatten else ["P1.rage_bar", "P2.rage_bar"],
            "weapon_bar": ["own_weapon_bar", "opp_weapon_bar"] if flatten else ["P1.weapon_bar", "P2.weapon_bar"],
            "power_bar": ["own_power_bar", "opp_power_bar"] if flatten else ["P1.power_bar", "P2.power_bar"]
        },
        "kof98umh": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character_1": ["own_character_1", "opp_character_1"] if flatten else ["P1.character_1", "P2.character_1"],
            "character_2": ["own_character_2", "opp_character_2"] if flatten else ["P1.character_2", "P2.character_2"],
            "character_3": ["own_character_3", "opp_character_3"] if flatten else ["P1.character_3", "P2.character_3"],
            "health": ["own_health", "opp_health"] if flatten else ["P1.health", "P2.health"],
            "power_bar": ["own_power_bar", "opp_power_bar"] if flatten else ["P1.power_bar", "P2.power_bar"]
        },
        "mvsc": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character_1": ["own_character_1", "opp_character_1"] if flatten else ["P1.character_1", "P2.character_1"],
            "character_2": ["own_character_2", "opp_character_2"] if flatten else ["P1.character_2", "P2.character_2"],
            "health_1": ["own_health_1", "opp_health_1"] if flatten else ["P1.health_1", "P2.health_1"],
            "health_2": ["own_health_2", "opp_health_2"] if flatten else ["P1.health_2", "P2.health_2"],
            "super_bar": ["own_super_bar", "opp_super_bar"] if flatten else ["P1.super_bar", "P2.super_bar"],
            "active_character": ["own_active_character", "opp_active_character"] if flatten else ["P1.active_character", "P2.active_character"]
        },
        "xmvsf": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character_1": ["own_character_1", "opp_character_1"] if flatten else ["P1.character_1", "P2.character_1"],
            "character_2": ["own_character_2", "opp_character_2"] if flatten else ["P1.character_2", "P2.character_2"],
            "health_1": ["own_health_1", "opp_health_1"] if flatten else ["P1.health_1", "P2.health_1"],
            "health_2": ["own_health_2", "opp_health_2"] if flatten else ["P1.health_2", "P2.health_2"],
            "super_bar": ["own_super_bar", "opp_super_bar"] if flatten else ["P1.super_bar", "P2.super_bar"],
            "active_character": ["own_active_character", "opp_active_character"] if flatten else ["P1.active_character", "P2.active_character"]
        },
        "soulclbr": {
            "side": ["own_side", "opp_side"] if flatten else ["P1.side", "P2.side"],
            "wins": ["own_wins", "opp_wins"] if flatten else ["P1.wins", "P2.wins"],
            "character": ["own_character", "opp_character"] if flatten else ["P1.character", "P2.character"],
            "health": ["own_health", "opp_health"] if flatten else ["P1.health", "P2.health"]
        }
    }

    # Collect keys
    keys = list(global_keys)
    game_keys = game_specific_keys.get(game_id, {})
    for key in game_keys.values():
        keys.extend(key)

    return keys
