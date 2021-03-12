from datetime import datetime

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_current_datetime_with_format_as_string(date_format: str):
    return datetime.now().strftime(date_format)


def convert_datetime_to_timestamp(date_time: datetime):
    return date_time.timestamp()


def convert_timestamp_to_datetime(time_stamp):
    return datetime.fromtimestamp(time_stamp)


def convert_timestamp_to_str_with_format(time_stamp, date_format=DEFAULT_DATE_FORMAT):
    if type(time_stamp) != float:
        time_stamp = float(time_stamp)
    return datetime.fromtimestamp(time_stamp).strftime(date_format)
