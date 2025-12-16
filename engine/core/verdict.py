def verdict(found_on: int, total_checked: int) -> str:
    VU = "Very Unlikely"
    U  = "Unlikely"
    L  = "Likely"
    VL = "Very Likely"

    if found_on == 0:
        return VU
    elif found_on == total_checked:
        return VL
    elif found_on > 0:
        return L