import pandas as pd


def load(path: str):
    """
    Load a csv file from a given path, print its shape
    and return it as a `pandas.DataFrame`.

    :param path: the path to the csv file.
    :return: the csv data.
    """
    data_frame = pd.read_csv(path)
    print(f'Loading dataset of dimensions {data_frame.shape}')
    return data_frame


__all__ = 'load',
