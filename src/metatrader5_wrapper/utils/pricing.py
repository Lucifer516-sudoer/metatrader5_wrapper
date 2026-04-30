def pip_size_from_symbol(point: float, digits: int) -> float:
    return point * 10 if digits in (3, 5) else point
