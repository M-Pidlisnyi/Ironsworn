from random import randint


RESULTS = {
    "strong_hit": "Strong Hit",
    "weak_hit": "Weak Hit",
    "miss": "Miss"
}


def action_roll(stat: int, adds: int = 0) -> tuple[str, bool]:
    """Roll action die vs two challenge dice. Returns result and match status."""
    
    action_score = randint(1, 6) + stat + adds
    challenge_dice_1 = randint(1, 10)
    challenge_dice_2 = randint(1, 10)
    
    # Strong hit: action score beats both challenge dice
    if action_score > challenge_dice_1 and action_score > challenge_dice_2:
        result = "strong_hit"
    # Miss: both challenge dice beat action score
    elif challenge_dice_1 > action_score and challenge_dice_2 > action_score:
        result = "miss"
    # Weak hit: action score beats one but not both
    else:
        result = "weak_hit"

    match = challenge_dice_1 == challenge_dice_2
    
    return RESULTS[result], match

def proggress_roll(progress_score: int) -> tuple[str, bool]:
    """Roll two challenge dice vs progress score. Returns result and match status."""
    
    challenge_dice_1 = randint(1, 10)
    challenge_dice_2 = randint(1, 10)
    
    # Strong hit: progress score beats both challenge dice
    if progress_score > challenge_dice_1 and progress_score > challenge_dice_2:
        result = "strong_hit"
    # Miss: both challenge dice beat progress score
    elif challenge_dice_1 > progress_score and challenge_dice_2 > progress_score:
        result = "miss"
    # Weak hit: progress score beats one but not both
    else:
        result = "weak_hit"
    
    match = challenge_dice_1 == challenge_dice_2

    return RESULTS[result], match