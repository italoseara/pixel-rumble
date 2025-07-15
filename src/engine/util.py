from pygame.math import Vector2
from .constants import PIVOT_POINTS


def validate_pivot(pivot) -> Vector2:
    """Validate and assign the pivot value."""
    
    if isinstance(pivot, str):
        if pivot not in PIVOT_POINTS:
            raise ValueError(f"Invalid pivot string: {pivot}. Must be one of {list(PIVOT_POINTS.keys())}.")
        return Vector2(PIVOT_POINTS[pivot])
    elif isinstance(pivot, tuple):
        if len(pivot) != 2:
            raise ValueError("Pivot tuple must be of length 2.")
        return Vector2(pivot)
    elif isinstance(pivot, Vector2):
        return pivot
    else:
        raise TypeError("Pivot must be a Vector2, tuple of two floats, or a valid pivot string.")