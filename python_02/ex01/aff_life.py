import load_csv as csv
from matplotlib import pyplot as plt
import numpy as np


def start():
    """
    Plot the life expectancy projections for France.
    """
    if (data := csv.load("life_expectancy_years.csv")) is None:
        exit(1)

    x = data.columns.values[1:].astype(np.int16)
    y = data.query("country == 'France'").values[0, 1:].astype(np.float32)

    plt.plot(x, y)
    plt.title("France Life expectancy Projections")
    plt.xlabel("Year")
    plt.ylabel("Life expectancy")
    plt.show()


if __name__ == "__main__":
    start()

__all__ = "aff_life",
