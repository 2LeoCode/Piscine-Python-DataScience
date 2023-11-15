from datetime import datetime


def format_ft_time():
    """
    Display the following:
      - Number of seconds since January 1, 1970.
      - Current date.
    """
    now = datetime.now()
    print(
        "Seconds since january 1, 1970: {timestamp:,.14} "
        "or {timestamp:.2e} in scientific notation\n{date}".format(
            timestamp=now.timestamp(),
            date=now.strftime("%b %d %Y"),
        )
    )


if __name__ == "__main__":
    format_ft_time()

__all__ = "format_ft_time",
