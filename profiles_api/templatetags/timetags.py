from django import template
import datetime
register = template.Library()

def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(ts)
    # return datetime.datetime.strftime("%d %b %Y %H:%M:%S")

register.filter(print_timestamp)
