"""Helpers for the easy_opera wrapper"""


def format_endpoints_input(endpoints: list) -> str:
    """Converts list of input endpoints into command line inputs.

    Args:
        endpoints (list): list of endpoints requested

    Returns:
        list: endpoints with dashes that could be used on a CLI
    """
    return [f"-{endpoint}" for endpoint in endpoints]
