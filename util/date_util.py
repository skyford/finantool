# date, time related
from datetime import datetime

def diff_dates(date1, date2):
    return abs(date2-date1).days

def extract_time(datestr):
    return datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")

def earlier_than(date1_str, date2_str):
    date1 = extract_time(date1_str)
    date2 = extract_time(date2_str)
    return date1 < date2

def is_in_range(date_str, start_str, end_str):
    date = extract_time(date_str)
    start = extract_time(start_str)
    end = extract_time(end_str)
    return (date >= start) and (date <= end)
