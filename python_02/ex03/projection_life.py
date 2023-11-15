import load_csv as csv
from matplotlib import pyplot as plt
import numpy as np


def projection_life():
    """
    Display a graph showing the correlation between
    the gross domestic product and the life expectancy
    across the years.
    """
    expectancy = csv.load("life_expectancy_years.csv")
    gross_product = csv.load(
        "income_per_person_gdppercapita_ppp_inflation_adjusted.csv"
    )

    a = np.asarray(expectancy.loc[:, "1900"].values, dtype=np.float32)
    b = np.asarray(gross_product.loc[:, "1900"].values, dtype=np.int32)

    plt.scatter(b, a)
    plt.title("1900")
    plt.xlabel("Gross domestic Product")
    plt.ylabel("Life Expectancy")
    plt.xscale('log')
    plt.xticks([300, 1000, 10000], ["300", "1k", "10k"])
    plt.show()


if __name__ == "__main__":
    projection_life()

__all__ = "projection_life",
