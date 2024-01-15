from datetime import datetime, timedelta

def m2m(s):
    if s.startswith('0'):
        return int(s[1:])
    else:
        return int(s)
    
def y2y(s):
    return int('20'+s)

def get_now():
    return datetime.now().strftime('%d.%m.%y %H:%M')

def get_new_time(date, minutes):
    dt = datetime(y2y(date[6:8]), m2m(date[3:5]), m2m(date[:2]), hour=int(date[9:11]), minute=int(date[12:]))
    dt += timedelta(minutes=minutes)
    return dt.strftime('%d.%m.%y %H:%M')

def get_datetime(date):
    return datetime(y2y(date[6:8]), m2m(date[3:5]), m2m(date[:2]), hour=int(date[9:11]), minute=int(date[12:]))