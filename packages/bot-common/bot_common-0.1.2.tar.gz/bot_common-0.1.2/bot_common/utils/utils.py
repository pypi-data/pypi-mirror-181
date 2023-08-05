from datetime import datetime, timezone
import re


def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            out = func(*args, **kwargs)
            return out
        except Exception as e:
            f_name = func.__name__
            exc = f'{f_name} --> {str(e)}'
            raise Exception(exc)
    return wrapper


@catch_exception
def clean_string(txt):
    out = txt.replace(r"\n", " ").replace("'", " ")
    out = re.sub(r"\s+", " ", out)
    return out.strip()


@catch_exception
def get_time_now():
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")


@catch_exception
def str_to_datetime(tmp_str):
    tmp_str1 = tmp_str.split('.')[0]
    tmp = datetime.strptime(tmp_str1, "%Y-%m-%d %H:%M:%S")
    return tmp


@catch_exception
def datetime_to_str(dt):
    out_str = dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    return out_str


@catch_exception
def validate_time(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        return True
    except ValueError:
        return False


@catch_exception
def remove_special_characters(txt):
    out = txt.replace(r"\n", " ")
    out = out.translate({ord(c): " " for c in r"""!@#$%^&*()'[]{};:,./<>?\|`"~-=_+"""})
    out = re.sub(r"\s+", " ", out)
    return out.strip()
