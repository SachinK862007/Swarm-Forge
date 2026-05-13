def get_action(state):
    attack_type = state[0]
    attempts = state[1]
    if attack_type == 2:   # injection
        return 1            # ISOLATE
    if attempts > 5:
        return 2            # SPAWN
    return 0                # ENGAGE