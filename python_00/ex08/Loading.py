from time import time


def format_minutes(seconds: float):
    """
    Transform a number of seconds into a string of the form `mm:ss`.

    :param seconds: the number of seconds.
    :return: a string of the form `mm:ss`.
    """
    return f"{int(seconds // 60):02}:{int(seconds % 60):02}"


def ft_tqdm(lst: range):
    """
    Simple reimplementation of the tqdm class.
    Print the progress bar of a range while yielding an iterator.
    Give information about the speed of the iteration.

    :param lst: the range to go through.
    """
    begin = time()
    it_sec = 0
    elapsed = .0
    print(
        "  0%|                                                             | "
        " {num:{width}}/{total} [0<?, ?it/s]".format(
                num=0,
                width=len(str(len(lst))),
                total=len(lst),
            ), end="", flush=True)
    for e in lst:
        yield e
        last_time = elapsed
        remaining = len(lst) - e
        percent = (e + 1) * 100 // len(lst)
        num_full = int(percent * 60 // 100)
        elapsed = time() - begin
        interval = elapsed - last_time
        estimated = (remaining - 1) * interval
        it_sec = (it_sec + 1 / interval) / 2
        print(
            "\033[2K\r{percent:>3}%|{equals}>{spaces}| "
            "{num:{width}}/{total} [{elapsed}<{estimated},"
            " {it_sec}]".format(
                percent=percent,
                equals="=" * num_full,
                spaces=" " * (60 - num_full),
                num=e + 1,
                width=len(str(len(lst))),
                total=len(lst),
                elapsed=format_minutes(elapsed),
                estimated=format_minutes(estimated),
                it_sec=(
                    f"{it_sec:.2f}it/s" if interval < 1
                    else f"{1 / it_sec:.2f}s/it"
                ),
            ),
            end="\b",
            flush=True
        )
    print()


__all__ = "ft_tqdm",
