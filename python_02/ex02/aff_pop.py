import load_csv as csv
from matplotlib import pyplot as plt
import numpy as np


def aff_pop():
    '''
    Plot the population projections for France and Germany
    '''
    if (data := csv.load("population_total.csv")) is None:
        exit(1)

    print(data)

    x = data.columns.values[1:].astype(np.int16)
    y_raw: list[list[str]] = data.query(
        "country == 'France' or country == 'Germany'"
    ).values[:, 1:].tolist()

    for row in y_raw:
        for i, cell in enumerate(row):
            row[i] = \
                cell.replace(",", "").replace("M", "e6").replace("k", "e3")
    y = np.asanyarray(np.array(y_raw, dtype=np.float32).T, dtype=np.int32)

    plt.plot(x, y)
    plt.legend(["Germany", "France"])
    plt.title("Population Projections")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.yscale("linear")
    plt.yticks([2e7, 4e7, 6e7, 8e7], ["20M", "40M", "60M", "80M"])
    plt.show()


if __name__ == "__main__":
    aff_pop()

__all__ = "aff_pop",
