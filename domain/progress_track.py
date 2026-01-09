"""
module containig utility functions that are used to work with 
proggress track functionality, primarily converting ticks into progresse squares
"""
TICKS_PER_PROGRESS = 4


def ticks_to_progress(ticks: int) -> tuple[int, int]:
    """takes the number of ticks and returns tuple containing the 
    number of filled progressed and remaining ticks"""
    return (ticks//TICKS_PER_PROGRESS, ticks%TICKS_PER_PROGRESS)

def progress_to_ticks(filled_proggress: int) -> int:
    """Returns the number of ticks in filled proggress sqiares"""
    return filled_proggress*TICKS_PER_PROGRESS