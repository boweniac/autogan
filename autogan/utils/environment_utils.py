from datetime import datetime


def environment_info() -> str:
    """Current environment information

    :return: --current_time: Y.m.d H:M:S week:%w
    """
    info = f'{get_time()}'

    return info


def get_time() -> str:
    """Get the current date and time

    Returns:
        str: Y.m.d H:M:S week:%w
    """

    now = datetime.now()

    formatted_now = now.strftime("%Y.%m.%d %H:%M:%S week:%w")
    week_dict = {"0": "Sunday", "1": "Monday", "2": "Tuesday", "3": "Wednesday", "4": "Thursday", "5": "Friday",
                 "6": "Saturday"}
    weekday = formatted_now[-1]
    formatted_now = formatted_now.replace("week:" + weekday, "week:" + week_dict[weekday])

    return formatted_now
