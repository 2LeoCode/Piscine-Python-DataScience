from tqdm import tqdm
from time import sleep
from Loading import ft_tqdm


def ft_tqdm_test(lst: range, interval: float):
    """
    Test the ft_tqdm function.
    """
    for _ in tqdm(lst):
        sleep(interval)

    for _ in ft_tqdm(lst):
        sleep(interval)


ft_tqdm_test(range(100), 0.1)
ft_tqdm_test(range(5), 2)
ft_tqdm_test(range(10000), 0.001)
