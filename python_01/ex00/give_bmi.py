def give_bmi(height: list[int | float], weight: list[int | float]):
    """
    Return a list of the BMI of each person.

    :param height: the height of each person.
    :param weight: the weight of each person.
    """
    if (
        not isinstance(height, list) or not isinstance(weight, list)
        or not all(
            isinstance(h, (int, float)) and isinstance(w, (int, float))
            for h, w in zip(height, weight)
        )
    ):
        raise TypeError("height and weight must be lists of ints or floats")
    return [w / h**2 for h, w in zip(height, weight)]


def apply_limit(bmi: list[int | float], limit: int):
    """
    Return a list of whether each person is overweight.

    :param bmi: the BMI of each person.
    :param limit: the upper limit of BMI.
    """
    if (
        not isinstance(bmi, list)
        or not all(isinstance(x, (int, float)) for x in bmi)
    ):
        raise TypeError("bmi must be a list of ints or floats")
    if not isinstance(limit, int):
        raise TypeError("limit must be an int")
    return [x > limit for x in bmi]


__all__ = "give_bmi", "apply_limit"
