from datetime import datetime

def str2float(text):
    try:
        number = float(text)
    except:
        number = float("nan")

    return number


def smartfact_time2datetime(fact_time_stamp):
    return datetime.utcfromtimestamp(
        str2float(fact_time_stamp) / 1000.0
    )
