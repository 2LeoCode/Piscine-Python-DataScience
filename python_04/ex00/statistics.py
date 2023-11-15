from typing import Literal

StatisticOperation = Literal["mean", "median", "quartile", "std", "var"]


def ft_mean(*args: float):
    """
    Get the mean of a set of numbers.

    :param args: The numbers to get the mean of.
    :return: The mean of the numbers.
    """
    if not (length := len(args)):
        raise ValueError("mean of empty array")
    return sum(args) / length


def ft_median(*args: float):
    """
    Get the median of a set of numbers.

    :param args: The numbers to get the median of.
    :return: The median of the numbers.
    """
    data = sorted(args)
    if not (length := len(data)):
        raise ValueError("median of empty array")
    median = data[length // 2]
    if length % 2 == 0:
        median = (median + data[length // 2 - 1]) / 2
    return median


def ft_quartile(*args: float):
    """
    Get the quartile of a set of numbers.

    :param args: The numbers to get the quartile of.
    :return: The quartile of the numbers.
    """
    data = sorted(args)
    if not (length := len(data)):
        raise ValueError("quartile of empty array")
    if length % 2 == 0:
        return (ft_median(*data[:length // 2]), ft_median(*data[length // 2:]))
    else:
        return (
            ft_median(*data[:length // 2 + 1]),
            ft_median(*data[length // 2:]),
        )


def ft_stddev(*args: float):
    """
    Get the standard deviation of a set of numbers.

    :param args: The numbers to get the standard deviation of.
    :return: The standard deviation of the numbers.
    """
    mean = ft_mean(*args)
    return (sum([(x - mean) ** 2 for x in args]) / len(args)) ** 0.5


def ft_variance(*args: float):
    """
    Get the variance of a set of numbers.

    :param args: The numbers to get the variance of.
    :return: The variance of the numbers.
    """
    return ft_stddev(*args) ** 2


def ft_statistics(*args: float, **kwargs: StatisticOperation):
    """
    Display the statistics of a set of numbers.

    :param args: The numbers to get the statistics of.
    :param kwargs: The statistics to get (names of keyword arguments
        are ignored, only their value matters):
        - mean: The mean of the numbers.
        - median: The median of the numbers.
        - quartile: The quartile of the numbers.
        - std: The standard deviation of the numbers.
        - var: The variance of the numbers.
        Any other keyword argument value displays "ERROR".
    """
    operations = {
        "mean": ft_mean,
        "median": ft_median,
        "quartile": ft_quartile,
        "std": ft_stddev,
        "var": ft_variance
    }
    for val in kwargs.values():
        if val in operations:
            try:
                print(f"{val}: {operations[val](*args)}")
            except ValueError:
                print("ERROR")


__all__ = "ft_statistics",
